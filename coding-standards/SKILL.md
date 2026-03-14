---
name: coding-standards
description: Moqui-specific guidelines for clean code, naming conventions, and log message patterns.
---

# Skill: coding-standards

## Goal
Enforce Moqui-specific production-quality code standards, ensuring clarity, maintainability, and alignment with framework paradigms.

## Triggers
**ALWAYS** read this skill when:
- Writing or refactoring any Moqui artifacts (Java, Groovy, XML Screens/Services/Entities).
- The user requests "clean code" or "Moqui best practices".
- Reviewing implementation patterns for consistency.

## Use when
- Documenting business logic in Groovy or XML.
- Naming new context variables, fields, or artifacts.
- Implementing logging to track execution flows.

## Don't use when
- Writing temporary scratchpad scripts in `/tmp`.
- Doing high-level architectural research (use `project-structure` for that).

## Inputs
- Moqui artifact source code (XML, Groovy, Java).
- Business requirements for the logic being implemented.

## Outputs
- Clean, professional, Moqui-compliant code.
- Descriptive and professional log messages.

## Rules & Guardrails
1. **Explain the WHY**: Code shows *what* happens. Comments must explain *why* (e.g., explaining a workaround for a specific data state).
2. **NO Internal Monologue**: Never leave "thinking out loud" or "maybe this works" comments.
3. **Moqui Naming Patterns**:
    - **Services**: `verb#Noun` (e.g., `update#Example`).
    - **Entities**: `UpperCamelCase` (e.g., `ExampleType`).
    - **Screens**: `UpperCamelCase` for file names (e.g., `EditExample.xml`).
    - **Transitions**: `lowerCamelCase` (e.g., `updateExample`, `getFeatures`).
    - **Variables/Fields**: `lowerCamelCase`.
4. **AVOID the verb `process`**: Never use `process` in names (services, transitions, variables, documents, files). Use more descriptive alternatives like `handle`, `execute`, `run`, `apply`, `perform`, `analyze`, or `sync`.
5. **User Feedback**:
    - Use `ec.message` to add messages for the user.
    - `ec.message.addMessage("Success message")` for standard feedback.
    - `ec.message.addError("Error message")` for validation failures.
5. **Moqui Logging**:
    - ALWAYS use `ec.logger`. NEVER use `println` or `System.out`.
    - **Pattern**: `[Entity] [Context] - [Action/Outcome/Issue]`
    - **Rules**:
        - **Entity**: Clearly specify the primary object (e.g., `Order`, `Shipment`, `Inventory`).
        - **Context**: Include specific IDs or key data (e.g., `ID: ${orderId}`, `Facility: ${facilityId}`).
        - **Action/Outcome/Issue**: Concise description of what happened, failed, or was adjusted.
        - **NO Redundant Prefixes**: Don't add `[Error]` or `[Warning]` manually; log levels handle this.
        - **Standard Levels**: `info` (operations), `warn` (risks), `error` (failures).
        - **Performance**: Track elapsed time for long-running processes (e.g., `Completed in ${elapsedTime}s`).
    - **Examples by Category**:
        - *Validation*: `ec.logger.info("Order [ID: ${orderId}] - Validation failed for missing productId")`
        - *Operational*: `ec.logger.info("Shipment [ID: ${shipmentId}] - Updated status to SHIPPED")`
        - *Error*: `ec.logger.error("Inventory [Product: ${productId}] - Insufficient stock at Facility ${facilityId}")`
        - *Inventory*: `ec.logger.info("Inventory [Product: ${productId}] - ATP adjusted by ${adj}, new ATP: ${newAtp}")`
        - *Asset Reservation*: `ec.logger.warn("Asset [ID: ${assetId}] - Locked for reservation, remaining ATP: ${atpTotal}")`
        - *User Action*: `ec.logger.info("User [ID: ${userLoginId}] - Approved Order ${orderId}")`
        - *System/Job*: `ec.logger.info("System [Job: ${jobId}] - Scheduled execution completed successfully")`
        - *Performance*: `ec.logger.info("Address [Validated: ${count}] - Completed in ${elapsedTime} minutes")`
6. **No Placeholders**: Avoid `TODO` without a tracking reference.
7. **Documentation**: Every service and entity MUST have a `<description>`.

## Failure handling
- **Self-Correction**: If you catch yourself using OFBiz patterns (like `UtilValidate`) in a Moqui context, immediately switch to Moqui equivalents (`ec.message`, etc.).
- **Consistency**: If existing code in a component follows a different standard, prioritize framework-wide Moqui standards while maintaining local style consistency.

## Minimal example
**Input**:
Need to update an example status and log it.

**Bad Output**:
```groovy
// I think we need to update status here
// Hopefully this works...
if (id) {
    println "Updating " + id
    ec.entity.makeValue("moqui.example.Example").setAll([exampleId:id, statusId:s]).update()
}
```

**Good Output**:
```groovy
// Ensure example ID is present before updating status to avoid runtime errors
if (exampleId) {
    ec.logger.info("Example [ID: ${exampleId}] - Updating status to ${statusId}")
    ec.entity.makeValue("moqui.example.Example").setAll([exampleId:exampleId, statusId:statusId]).update()
}
```
