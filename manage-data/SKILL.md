---
name: manage-data
description: Manage Moqui Entity Facade XML data files for seed, demo, configuration, and Darpan release-safe setup data.
---

# Skill: manage-data

## Goal
Manage Moqui Entity Facade XML data files so setup data loads in the right order and release upgrade data can be generated from the generic source files.

## Triggers
**ALWAYS** read this skill when:
- Creating new records in the database via XML files (Seed, Demo).
- Defining status flags, enumeration types, or initial configuration.
- Fixing data loading errors or updating existing records via data XML.
- Adding Darpan or NetSuite setup records that must be included in a future release.

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
- Accurate Moqui Entity Facade XML data files in the owning component `data/` directory.
- Correct `<entity-facade-xml type="...">` reader type.

## Procedure
1. Identify the owning component and data domain before editing.
2. Reuse the appropriate existing generic data file whenever possible.
3. Add root `<entity-facade-xml type="seed|install|demo|custom-reader-type">`.
4. Add entity elements with stable primary keys, for example `<moqui.basic.Enumeration .../>`.
5. Keep dependent data in files/readers that load after the records they reference.
6. Verify with the narrowest relevant Gradle load task.

## Darpan release-data source of truth
- New Darpan setup data must be added to the appropriate generic source file under `darpan-backend/runtime/component/darpan/data/*.xml` first. Do not author release-only records directly in `data/upgrade-data.xml`.
- Release preflight compares generic source data files against the previous tag to build or validate the current release `upgrade-data.xml`; records that exist only in `upgrade-data.xml` will be missed by normal source-data management and should be treated as invalid.
- Add a new generic source file only when the records form a distinct setup domain or load bundle. Name it by domain and end with `SeedData.xml`.
- Use `darpan-seed-initial` for Darpan base type/classification records that other Darpan data depends on. Use `darpan-seed` for ordinary Darpan setup/configuration records.
- Use `netsuite-seed-initial` and `netsuite-seed` for NetSuite component data under `darpan-backend/runtime/component/netsuite-darpan/data/*.xml`; these readers load after Darpan component data.
- Do not use Moqui framework `seed` or `seed-initial` readers for Darpan-specific or NetSuite-specific records.

## Darpan file selection
- Types, classifications, and source-type setup: `DarpanSystemSourceTypeSeedData.xml` or the matching domain `*Type*SeedData.xml`.
- System sources and source instances: `DarpanSystemSourceSeedData.xml` or `RunSystemInstance*SeedData.xml`.
- Security and artifact authorization: `SecuritySeedData.xml`.
- System message remotes and endpoints: `SystemMessageRemoteSeedData.xml`.
- Scheduled jobs: `ReconciliationJobSeedData.xml`.
- Reconciliation mappings and setup: `MappingSeedData.xml`, `ReconciliationInventorySeedData.xml`, or `ReconciliationCompareScopeFixtureData.xml`.
- NetSuite-specific reconciliation setup: the matching file under `runtime/component/netsuite-darpan/data/`.

## Rules & Guardrails
1. **Root Tag**: Use `<entity-facade-xml type="...">`.
2. **Entity Tags**: Use the entity name as the tag (e.g., `<moqui.basic.StatusItem .../>`).
3. **Primary Keys**: Explicitly provide primary keys for seed data (e.g., `statusId="EX_IN_DESIGN"`).
4. **Registration**: Unlike OFBiz, Moqui data files are often automatically picked up if they are in the `data/` directory of a component, but ensure they are correctly ordered if there are dependencies (use `data-install`, `data-seed` conventions).
5. **Update vs Insert**: Moqui's `EntityDataLoader` will update existing records by default if the primary key matches.
6. **Namespaces**: Use full entity names (package + name) to avoid ambiguity, especially for framework entities.
7. **Release Safety**: Every Darpan release upgrade record should be traceable back to a generic source data file diff.

## Failure handling
- **Foreign Key Violation**: Ensure dependence data (e.g., the `StatusType`) is loaded before the dependent data (`StatusItem`). Use separate files if necessary.
- **Darpan Load Order**: Use `./gradlew loadDarpanData` for full ordered component setup, and `./gradlew loadDarpanUpgradeData` for the current release upgrade file.

## Minimal example
**Requirement**: Add a new Example Status Type and a 'In Design' status.

**Good Output**:
```xml
<entity-facade-xml type="seed">
    <moqui.basic.StatusType statusTypeId="ExampleStatus" description="Example Status Flow"/>
    <moqui.basic.StatusItem statusId="EXST_IN_DESIGN" statusTypeId="ExampleStatus" description="In Design" sequenceNum="10"/>
</entity-facade-xml>
```
