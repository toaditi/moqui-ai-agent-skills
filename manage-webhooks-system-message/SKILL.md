---
name: manage-webhooks-system-message
description: Implement reliable and decoupled integration patterns using Moqui System Messages.
---

# Skill: manage-webhooks-system-message

## Goal
Implement reliable messaging for inbound and outbound integrations using Moqui's System Message framework, ensuring data delivery even in the presence of temporary system failures.

## Triggers
**ALWAYS** read this skill when:
- Designing "Fire and Forget" or "Eventually Consistent" integration patterns.
- Handling inbound webhooks from external systems (e.g., Shopify, Stripe).
- Implementing outbound messages that require a guaranteed delivery attempt (retries).

## Use when
- Creating `SystemMessageType` definitions for specific external systems.
- Moving brittle direct REST calls into a queued/reliable message flow.
- Handling complex multi-step data transformations for external consumption.

## Don't use when
- Low-latency, synchronous responses are strictly required by the client.
- Simple, one-off API calls with no need for reliability tracking.

## Inputs
- Integration requirements (inbound/outbound).
- Data structure (JSON/XML).
- Reliable delivery/retry requirements.

## Outputs
- `SystemMessageType` and `SystemMessage` configurations in XML data.
- Implementation logic for `send` or `receive` services.

## Rules & Guardrails
1. **Reliability Chain**:
    - **Outbound**: Service logic creates a `SystemMessage` record -> Background job triggers the `send` service.
    - **Inbound**: Webhook/REST endpoint creates a `SystemMessage` record -> Background job triggers the `receive` service.
2. **Status Tracking**: Monitor statuses like `SmsgPending`, `SmsgSent`, `SmsgError`, and `SmsgConsumed`.
3. **Mapping**:
    - `SystemMessage`: The instance record. PK: `systemMessageId`.
    - `SystemMessageType`: Defines *how* to process (e.g., `sendServiceName`, `consumeServiceName`).
    - `SystemMessageRemote`: Defines *where* to send/receive (e.g., `sendUrl`, `username`, `password`).
4. **Status Lifecycle**:
    - Outbound: `SmsgProduced` -> `SmsgSending` -> `SmsgSent` (or `SmsgError`).
    - Inbound: `SmsgReceived` -> `SmsgConsuming` -> `SmsgConsumed`.
5. **Payload**: `messageText` is suitable for most JSON/XML payloads. Use `messageTextLong` for very large data if custom fields are added.
6. **Reliability**: Use the `SystemMessageScan` job (configured in `ServiceJob`) to automatically pick up `SmsgProduced` or `SmsgReceived` messages.
7. **SystemMessageRemote**: Links a `SystemMessageType` to a specific destination via `systemMessageRemoteId`.

## Failure handling
- **Retries**: Use Moqui's built-in retry logic configured on the `SystemMessageType` or via background jobs.
- **Dead Letter**: If a message fails after multiple retries, it stays in `SmsgError` for manual intervention.

## Minimal example
**Requirement**: Queue an outbound order notification as a System Message.

**Good Output (XML Data)**:
```xml
<moqui.service.message.SystemMessage systemMessageId="SM123" 
    systemMessageTypeId="OutboundOrderSync" 
    statusId="SmsgPending" 
    messageText='{"orderId": "10001", "action": "CREATE"}'/>
```

**Workflow**: 
1. Service creates the record above.
2. A background `ServiceJob` calls Moqui's `org.moqui.impl.SystemMessageServices.send#SystemMessage` for all `SmsgPending` messages.
