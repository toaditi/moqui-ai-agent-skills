---
name: manage-entities
description: Manage Moqui entity definitions, relationships, indexing, and static ViewEntity patterns.
---

# Skill: manage-entities

## Goal
Efficiently define and maintain the Moqui Data Model, ensuring proper indexing, relationship mapping, and audit logging for high-performance applications.

## Triggers
**ALWAYS** read this skill when:
- Creating a new entity or view-entity in a Moqui component.
- Adding fields, relationships, or indexes to an existing entity.
- Configuring audit logs or field encryption for sensitive data.

## Use when
- Modeling business objects as Moqui entities.
- Defining join-based data retrieval structures (View Entities).
- Mapping relationships between core framework entities and custom entities.

## Don't use when
- Managing dynamic view entities at runtime (use `manage-view-entities` for that).
- Handling large-scale history data or audit log review (use `manage-data-history`).

## Inputs
- Entity requirements (fields, types, relationships).
- Security requirements (auditing, encryption).

## Outputs
- Accurate and performance-optimized `.xml` entity definitions in the `entity/` directory.

## Rules & Guardrails
1. **Naming**: Use `UpperCamelCase` for entity names and `lowerCamelCase` for fields.
2. **Short Aliases**: ALWAYS provide a `short-alias` on entities and many-to-one relationships to enable user-friendly REST APIs.
3. **Audit Logging**: Use `enable-audit-log="true"` on fields that require change tracking (e.g., `statusId`, `amount`).
4. **Encryption**: Use `encrypt="true"` for PII or sensitive secrets (e.g., `secretAnswer`, `governmentId`).
5. **View Entity Best Practices**:
    - Use `join-from-alias` for clear join paths.
    - Leverage `<alias-all>` to reduce verbose mapping.
    - Use `<exclude>` within `<alias-all>` to avoid duplicate field names or irrelevant data.
7. **REST Optimization**: Use `<master>` and `<detail>` elements within an entity to define the hierarchical structure for automatic REST API responses and efficient `oneMaster()` Groovy fetches.
8. **Relationships**: Use `short-alias` on many-to-one relationships to enable user-friendly dots-style navigation (e.g., `example.type.description`).
9. **Sequence IDs**: Use `type="id"` for primary keys and sequenced IDs.

## Failure handling
- **Missing Relationship**: If a related entity cannot be found during runtime, ensure the `package` attribute is correctly specified in the `related` attribute.
- **Join Complexity**: If a View Entity join causes performance issues, verify that join fields are indexed on the member entities.

## Minimal example
**Requirement**: Define an 'Example' entity with a status and a list of items.

**Bad Output**:
```xml
<!-- Missing short-aliases and audit logging -->
<entity entity-name="MyExample" package="co.hotwax.demo">
    <field name="id" type="id" is-pk="true"/>
    <field name="name" type="text-medium"/>
    <field name="status" type="id"/>
    <relationship type="one" related="moqui.basic.StatusItem">
        <key-map field-name="status"/>
    </relationship>
</entity>
```

**Good Output**:
```xml
<entity entity-name="Example" package="moqui.example" short-alias="examples">
    <field name="exampleId" type="id" is-pk="true"/>
    <field name="exampleName" type="text-medium"/>
    <field name="statusId" type="id" enable-audit-log="true"/>
    
    <relationship type="one" title="Status" related="moqui.basic.StatusItem" short-alias="status">
        <key-map field-name="statusId"/>
    </relationship>
    <relationship type="many" related="moqui.example.ExampleItem" short-alias="items">
        <key-map field-name="exampleId"/>
    </relationship>
</entity>
```
