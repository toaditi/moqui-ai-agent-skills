---
name: manage-data
description: Manage Moqui XML data files for seed, demo, and configuration data.
---

# Skill: manage-data

## Goal
Manage Moqui XML data files to populate the database with seed, demo, or configuration records using Moqui's flexible and intuitive data format.

## Triggers
**ALWAYS** read this skill when:
- Creating new records in the database via XML files (Seed, Demo).
- Defining status flags, enumeration types, or initial configuration.
- Fixing data loading errors or updating existing records via data XML.

## Use when
- Adding lookup data (Enums, StatusItems).
- Preparing demo data for testing.
- Configuring entities like `DataFeed`, `DataDocument`, or `ServiceJob`.

## Don't use when
- Defining the data schema itself (use `manage-entities`).

## Inputs
- Entity name to populate.
- Field values for the records.
- Data type (Seed, Demo, Install).

## Outputs
- Accurate Moqui XML data files in `data/`.

## Rules & Guardrails
1. **Root Tag**: The root tag is typically `<entity-engine-xml>` (though optional in Moqui, it is recommended for clarity).
2. **Entity Tags**: Use the entity name as the tag (e.g., `<moqui.basic.StatusItem .../>`).
3. **Primary Keys**: Explicitly provide primary keys for seed data (e.g., `statusId="EX_IN_DESIGN"`).
4. **Registration**: Unlike OFBiz, Moqui data files are often automatically picked up if they are in the `data/` directory of a component, but ensure they are correctly ordered if there are dependencies (use `data-install`, `data-seed` conventions).
5. **Update vs Insert**: Moqui's `EntityDataLoader` will update existing records by default if the primary key matches.
6. **Namespaces**: Use full entity names (package + name) to avoid ambiguity, especially for framework entities.

## Failure handling
- **Foreign Key Violation**: Ensure dependence data (e.g., the `StatusType`) is loaded before the dependent data (`StatusItem`). Use separate files if necessary.

## Minimal example
**Requirement**: Add a new Example Status Type and a 'In Design' status.

**Good Output**:
```xml
<entity-engine-xml>
    <moqui.basic.StatusType statusTypeId="ExampleStatus" description="Example Status Flow"/>
    <moqui.basic.StatusItem statusId="EXST_IN_DESIGN" statusTypeId="ExampleStatus" description="In Design" sequenceNum="10"/>
</entity-engine-xml>
```
