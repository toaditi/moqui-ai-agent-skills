---
name: manage-eca
description: Implement Moqui event-driven logic using SECAs (Service ECA) and EECAs (Entity ECA).
---

# Skill: manage-eca

## Goal
Implement event-driven logic patterns in Moqui using Service Event Control Actions (SECA) and Entity Event Control Actions (EECA) to decouple processes and ensure consistency.

## Triggers
**ALWAYS** read this skill when:
- Creating or modifying `*.secas.xml` or `*.eecas.xml` files.
- Adding side effects to existing services or entity lifecycle events (e.g., logging, notifications, or indexing).
- Designing asynchronous or transactional event flows in Moqui.

## Use when
- Triggering indexing (ElasticSearch/Solr) after a service commit.
- Sending emails after specific data changes.
- Syncing data to external systems when an entity is created or updated.

## Don't use when
- The logic should be part of the main service flow (use `manage-logic` inside the service).

## Inputs
- Trigger event (service call or entity operation).
- Conditions for execution.
- Actions to perform.

## Outputs
- SECA definitions in `service/*.secas.xml`.
- EECA definitions in `entity/*.eecas.xml`.

## Rules & Guardrails
1. **SECA (Service ECA)**:
    - **Trigger Points**: `pre-auth`, `pre-validate`, `pre-service`, `post-service`, `tx-commit`, `tx-rollback`, `post-commit`.
    - `post-service`: Runs immediately after the service logic, but BEFORE the database transaction is committed.
    - `tx-commit`: Runs AFTER the database transaction has successfully committed. Use this for reliable side effects like search indexing.
    - `post-commit`: Runs after the transaction is complete, outside the main request context if async.
2. **EECA (Entity ECA)**:
    - **Trigger Points**: `on-create`, `on-update`, `on-delete`, `on-find`.
    - Use sparingly as they run for EVERY instance of an entity operation across the entire system.
3. **Execution Order**: Use the `priority` attribute to control the sequence of multiple ECAs triggering on the same event (lower numbers run first).
4. **Conditions**: Use `<condition><expression>...</expression></condition>` to filter triggers.
    - Example: `statusChanged` is a special variable available in many Moqui ECAs when a status field is updated.
5. **Recursion Warning**: Avoid ECAs that trigger the same service/entity operation, leading to infinite loops.

## Failure handling
- **Ignore Error**: Use `ignore-error="true"` on `<service-call>` if the ECA action is non-critical.
- **Transaction Impact**: Be aware that `pre-*` and `post-service` hooks run within the main transaction. Failures here will rollback the main operation.

## Minimal example
**Requirement**: Index an Order for search only after it is successfully committed, with high priority.

**Good Output (SECA)**:
```xml
<secas xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-eca-3.xsd">
    <seca id="IndexOrderOnCommit" service="update#OrderHeader" when="tx-commit" priority="1">
        <condition><expression>statusChanged</expression></condition>
        <actions>
            <service-call name="co.hotwax.oms.search.SearchServices.index#OrderHeader" 
                          in-map="[orderId:orderId]" ignore-error="true" async="true"/>
        </actions>
    </seca>
</secas>
```
