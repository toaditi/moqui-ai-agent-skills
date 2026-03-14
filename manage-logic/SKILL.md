---
name: manage-logic
description: Implement Moqui business logic using Groovy or XML actions, managing execution context and transactions.
---

# Skill: manage-logic

## Goal
Implement robust Moqui business logic using expressive Groovy scripts or declarative XML actions, leveraging the `ExecutionContext` for entity operations, service calls, and transaction management.

## Triggers
**ALWAYS** read this skill when:
- Writing logic inside `<actions>` tags in services, screens, or ECAs.
- Creating or modifying Groovy script files (`script/**/*.groovy`).
- Designing complex workflows requiring conditional execution and loops in Moqui.

## Use when
- Implementing domain logic for a service.
- Performing data transformations or calculations.
- Coordinating multiple entity operations in a single unit of work.

## Don't use when
- Defining the service interface (use `manage-services`).
- Simple CRUD logic is enough (use `type="entity-auto"` in `manage-services`).

## Inputs
- Service context (parameters in/out).
- Entity definitions and relationship structure.

## Outputs
- Groovy scripts (`.groovy`) or XML action blocks.

## Rules & Guardrails
1. **ExecutionContext (`ec`)**: Use `ec` as the entry point for everything:
    - `ec.entity`: Database operations (`find()`, `makeValue()`).
    - `ec.service`: Service calls (`sync().name("name").call()`).
    - `ec.logger`: Logging (`info()`, `warn()`, `error()`).
    - `ec.message`: User messages (`addMessage()`) and error handling (`addError()`).
2. **Advanced Entity Fetching**:
    - Use `oneMaster("name")` to fetch an entity along with its related child entities according to a master-detail definition.
    - Use `useCache(true)` for static configuration data.
    - Use `disableAuthz()` for internal logic that should bypass automatic security checks.
3. **Web & UI Context**:
    - `ec.web`: Access web-specific context (parameters, session).
    - `ec.web.sendJsonResponse(data)`: Common in transitions for sending raw JSON to the client.
    - `ec.web.parameters`: Map of merged URL and form parameters.
4. **Groovy Performance**: Prefer `@CompileStatic` for utility classes.
4. **XML Actions**: Use for high-level orchestration:
    - `<set field="..." from="..." type="..." default-value="..." />`
    - `<if>`, `<else-if>`, `<else>` for branching.
    - `<iterate list="..." entry="..." />` for loops.
    - `<service-call name="..." in-map="..." out-map="..." transaction="force-new" ignore-error="true"/>` for loop reliability.
5. **API Integration**: Use `ec.service.rest()` in Groovy for calling external REST APIs with built-in retry and timeout support.
6. **Error Handling**: Use `ec.message.addError()` to trigger rollbacks in standard service flows. Use `ec.message.addPublicMessage()` for messages that must be displayed to the user even if technical details are hidden.

## Failure handling
- **NPE Prevention**: Use Groovy's safe navigation operator `?.` (e.g., `orderHeader?.statusId`).
- **Entity Not Found**: Always check if `find().one()` returns null before accessing fields.

## Minimal example
**Requirement**: Fetch a Sales Order and all its items using a master-detail definition, then call an external API.

**Good Output (Groovy)**:
```groovy
// Fetch order with its items graph
EntityValue order = ec.entity.find("org.apache.ofbiz.order.order.OrderHeader")
    .condition("orderId", orderId).oneMaster("default")

if (order == null) {
    ec.message.addError("Order ${orderId} not found")
    return
}

// Call external API via RestClient
def restClient = ec.service.rest().method("POST").uri("https://api.example.com/sync")
    .jsonObject([orderId: order.orderId, items: order.items])
def response = restClient.call()

if (response.statusCode != 200) {
    ec.logger.error("Order [ID: ${orderId}] - Sync failed with error: ${response.error}")
}
```
