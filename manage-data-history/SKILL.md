---
name: manage-data-history
description: Manage Moqui audit trails using EntityAuditLog and custom business history snapshot patterns.
---

# Skill: manage-data-history

## Goal
Establish robust auditing and historical tracking for data changes, enabling traceability of sensitive modifications and point-in-time reporting.

## Triggers
**ALWAYS** read this skill when:
- Designing entities that require change tracking (Financial, Order, Security).
- Designing report structures that need to show data as it existed in the past.
- Configuring `enable-audit-log` or `EntityAuditLog` retrieval.

## Use when
- Enabling field-level auditing for sensitive fields (e.g., `statusId`, `amount`, `thruDate`).
- Implementing "History" entities to capture snapshots of complex data (e.g., `OrderHistory`, `InventoryHistory`).
- Using effective-dating (thruDate) to maintain record versions.

## Don't use when
- Tracking high-frequency, non-critical data (Audit logging has a performance overhead).
- Storing temporary state changes that don't need persistent history.

## Inputs
- Entity field definitions.
- Regulatory or business requirements for audit trails.

## Outputs
- Updated entity definitions with `enable-audit-log`.
- Custom history entity definitions and services to populate them.

## Rules & Guardrails
1. **Built-in Auditing**: 
   - Use `enable-audit-log="true"` on specific fields rather than the whole entity to keep the log size manageable.
   - Access logs via `moqui.entity.EntityAuditLog` view or entity.
2. **Business History**:
   - For many-to-many or complex parent-child history, create a dedicated history entity (e.g., `MyEntityHistory`).
   - History entities should typically include `fromDate`, `thruDate`, and the ID of the user who made the change.
3. **Immutability**: Once a history record is "closed" (thruDate set), it should ideally never be modified.
4. **Context**: Leverage `ec.user.userId` when manually creating history records in services.

## Failure handling
- **Audit Overflow**: If `EntityAuditLog` grows too fast, prioritize which fields truly need auditing and consider archival strategies.

## Minimal example
**Requirement**: Track changes to an Example's status and maintain a history of name changes.

**Bad Output**:
```xml
<!-- Only built-in audit on EVERYTHING - inefficient -->
<entity entity-name="Example" enable-audit-log="true">
    <field name="exampleId" type="id" is-pk="true"/>
    <field name="exampleName" type="text-medium"/>
</entity>
```

**Good Output**:
```xml
<!-- Targeted audit and custom history for business context -->
<entity entity-name="Example">
    <field name="exampleId" type="id" is-pk="true"/>
    <field name="exampleName" type="text-medium"/>
    <field name="statusId" type="id" enable-audit-log="true"/> <!-- Only audit status -->
</entity>

<entity entity-name="ExampleNameHistory">
    <field name="exampleId" type="id" is-pk="true"/>
    <field name="fromDate" type="date-time" is-pk="true"/>
    <field name="thruDate" type="date-time"/>
    <field name="exampleName" type="text-medium"/>
    <field name="userId" type="id"/>
</entity>
```
