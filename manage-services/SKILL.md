---
name: manage-services
description: Define Moqui services in services.xml, covering naming conventions, attributes, and parameters.
---

# Skill: manage-services

## Goal
Efficiently define Moqui service interfaces, ensuring clear naming conventions, robust parameter validation, and appropriate transaction control for reliable business logic execution.

## Triggers
**ALWAYS** read this skill when:
- Creating a new service definition in a Moqui component (`service/*.xml`).
- Modifying parameters, attributes, or transaction settings of an existing service.
- Defining service interfaces (`implements`) for consistent multi-implementation patterns.

## Use when
- Exposing business logic as a Moqui service.
- Wrapping entity-auto logic for complex validation before database operations.
- Defining remote-REST or Camel service gateways.

## Don't use when
- Implementing the actual logic (use `manage-logic` for Groovy/XML actions).
- Managing event-driven triggers (use `manage-eca`).

## Inputs
- Service requirements (verb, noun, intended operation).
- Input/Output parameter specifications.
- Security and transaction requirements.

## Outputs
- Clean and schema-compliant `<service>` definitions in `service/*.xml` files.

## Rules & Guardrails
1. **Naming**: Use `verb#Noun` format (e.g., `create#Product`, `calculate#OrderTotal`). The `#` symbol is required when calling services via the API or SECAs.
2. **Type Attribute**:
    - `entity-auto`: Use for simple CRUD on a single entity (auto-mapping fields).
    - `script`: Use for Groovy implementation (default if `<actions>` is present).
    - `rest` / `remote-rest`: Use for calling external REST APIs.
    - Custom types like `oms-rest` might exist in specific HotWax modules.
3. **Interfaces**: Use `<implements service="..."/>` to inherit parameters and definition from a base service (polymorphism).
4. **Transaction Control**:
    - `use-transaction="true"` (default): Runs within the current transaction.
    - `require-new="true"`: suspends current transaction and starts a new one.
    - `transaction="force-new"` or `transaction="ignore"`: Specific control for integration or large batches.
5. **Parameters**:
    - Use `<auto-parameters include="nonpk"/>` to reduce boilerplate for entity-based services.
    - Use `<parameter name="..." required="true"/>` for mandatory fields.
    - Leverage validation tags: `<text-email/>`, `<text-url/>`, `<number-integer/>`, `<number-decimal/>`.
    - Use `allow-html="any"` if the parameter accepts HTML content (e.g., email bodies).
6. **Authentication & Security**: 
    - `authenticate="true"` (default): Requires a valid user session.
    - `authenticate="false"`: Publicly accessible logic.
    - `authenticate="anonymous-all"`: Specific access for unauthenticated users.
    - Set `allow-remote="true"` ONLY if the service needs to be accessible via external REST/JSON gateways.

## Failure handling
- **Parameter Validation**: If a service call fails due to invalid parameters, ensure the types and `required` attributes match the incoming data.
- **Transaction Timeout**: For long-running services, consider `async="true"` or moving logic to a background job (`manage-jobs`).

## Minimal example
**Requirement**: Define a service that implements a common DataFeed interface for Solr indexing.

**Good Output**:
```xml
<service verb="index" noun="ProductSolr" authenticate="false">
    <implements service="org.moqui.EntityServices.receive#DataFeed"/>
    <actions>
        <iterate list="documentList" entry="dataDocument">
            <service-call name="co.hotwax.oms.search.SearchServices.call#CreateProductIndex" 
                          in-map="[productId:dataDocument._id]"
                          transaction="force-new" ignore-error="true"/>
        </iterate>
    </actions>
</service>
```
