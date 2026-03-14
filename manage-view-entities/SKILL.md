---
name: manage-view-entities
description: Manage dynamic View Entities at runtime using Moqui's EntityDynamicView API.
---

# Skill: manage-view-entities

## Goal
Construct join-based data retrieval structures dynamically at runtime in Groovy logic, allowing for flexible reporting and filtered data access without pre-defining entities in XML.

## Triggers
**ALWAYS** read this skill when:
- You need to join multiple entities for a search but no static View Entity exists.
- Implementing a report or summary screen that requires cross-entity filtering.
- Using `ec.entity.makeDynamicView()` in a Groovy script or Service.

## Use when
- Creating ad-hoc reports in Groovy.
- Joining a custom entity with a framework entity (like `StatusItem` or `Enumeration`) on the fly.
- Performance optimization for specific queries where joining is more efficient than nested lookups.

## Don't use when
- The join structure is common and reused frequently (use static `<view-entity>` in `entity/*.xml` instead).

## Inputs
- Member entities to be joined.
- Join conditions (key maps).
- Fields to alias.

## Outputs
- An `EntityDynamicView` object used as an input to `ec.entity.find()`.

## Rules & Guardrails
1. **Instantiation**: Always start with `EntityDynamicView edv = ec.entity.makeDynamicView()`.
2. **Member Addition**: Use `.addMemberEntity(alias, entityName, joinFromAlias, joinOptional, keyMap)`.
   - `joinOptional` should be `true` for `LEFT OUTER JOIN`.
3. **Aliasing**:
    - Use `.addAliasAll(alias, prefix)` to include all fields from a member.
    - Use `.addAlias(alias, name, field, function)` for specific fields or aggregate functions (e.g., `count`, `sum`, `max`).
4. **Calculated Fields**: For mathematical operations in dynamic views, use `complex-alias` patterns via XML (static) or the API (if supported by specific persistence layers).
    - *Example (Static XML)*: `<alias name="total"><complex-alias operator="*"><complex-alias-field entity-alias="ITEM" field="quantity"/><complex-alias-field entity-alias="ITEM" field="unitAmount"/></complex-alias></alias>`
5. **Execution**: Pass the dynamic view object directly to the find method: `ec.entity.find(edv)`.
6. **Efficiency**: Only alias the fields necessary for the specific business logic to minimize data transfer from the database.

## Failure handling
- **Ambiguous Fields**: If two member entities have the same field name, ensure you use a `prefix` in `addAliasAll` or explicitly alias them with unique names to avoid conflicts.

## Minimal example
**Requirement**: Find Examples joined with their Status descriptions dynamically.

**Bad Output**:
```groovy
// Inefficient nested lookups
def results = ec.entity.find("Example").list()
results.each { ex ->
    ex.statusDescription = ec.entity.find("StatusItem").condition("statusId", ex.statusId).one().description
}
```

**Good Output**:
```groovy
// Efficient dynamic join
EntityDynamicView edv = ec.entity.makeDynamicView()
edv.addMemberEntity("EXPL", "moqui.example.Example", null, null, null)
edv.addMemberEntity("STIT", "moqui.basic.StatusItem", "EXPL", true, [statusId: 'statusId'])
edv.addAliasAll("EXPL", null)
edv.addAlias("STIT", "statusDescription", "description", null)

List<EntityValue> results = ec.entity.find(edv).condition("statusId", "EXST_IN_DESIGN").list()
```
