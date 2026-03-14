---
name: manage-forms
description: Define Moqui declarative forms (single and list), covering fields, automation, and interactivity.
---

# Skill: manage-forms

## Goal
Design and implement declarative Moqui forms (`form-single` and `form-list`) that leverage automation, dynamic validation, and interactive components for efficient data management.

## Triggers
**ALWAYS** read this skill when:
- Defining or modifying forms in an XML screen.
- Adding fields to existing forms.
- Configuring form-level automation (`auto-widget-*`) or dynamic behavior (`depends-on`, `dynamic-options`).

## Use when
- Creating CRUD interfaces for entities.
- Building searchable tables or reports.
- Implementing diagnostic input dialogs.

## Don't use when
- Controlling the overall screen hierarchy (use `manage-screens`).

## Inputs
- Data model (entity) or service definition to be mapped.
- Input requirements (field types, validation).
- Functional requirements (searchable, editable, csv export).

## Outputs
- `<form-single>` or `<form-list>` definitions within `<widgets>`.

## Rules & Guardrails
1. **Form Types**:
    - `form-list`: Use for displaying and searching multiple records. Use `list="..."` for the source list.
    - `multi="true"`: Use in `form-list` to allow bulk updates (multiple rows submitted in one call). Fields in a multi-form are automatically indexed (e.g., `fieldName_0`, `fieldName_1`).
2. **Automation & Mapping**:
    - Use `<auto-fields-service service-name="..."/>` or `<auto-fields-entity entity-name="..."/>` at the form level to pre-generate fields.
    - Use `<auto-widget-entity entity-name="..." field-type="edit|find|display"/>` for specific fields.
    - Use `map="..."` on a form to specify the data source (e.g., resulting from `entity-find-one`).
3. **Advanced Layout**:
    - Use `<field-layout>` to organize fields into rows, groups, or accordions.
    - `<field-row>`: Places fields side-by-side.
    - `<field-group title="...">`: Groups related fields visually.
    - `<field-accordion>`: Collapsible sections for complex forms.
    - `<fields-not-referenced/>`: Essential when using custom layout to include all other fields.
4. **Interactive Fields**:
    - `<dynamic-options>`: AJAX-fetched drop-down options.
    - `<depends-on>`: Refresh field B when field A changes.
    - `<display-entity>`: Display a field from a related entity (e.g., name from a code). 
5. **Layout & Style**:
    - Use `skip-form="true"` in `form-list` if it's purely for display and doesn't wrap actions.
    - Enable features like `show-csv-button="true"`, `select-columns="true"`, and `header-dialog="true"` for full-featured list forms.

## Failure handling
- **Field Name Mismatch**: Ensure field names match the entity field names or the map keys in the list.
- **Empty Lists**: Use `<row-actions>` in `form-list` for data processing required for each row.

## Minimal example
**Requirement**: Create a search form for Examples with a dynamic type drop-down.

**Good Output**:
```xml
<form-list name="ListExamples" list="exampleList" skip-form="true" header-dialog="true">
    <field name="exampleId">
        <header-field show-order-by="true"><text-find hide-options="true"/></header-field>
        <default-field><link url="editExample" text="${exampleId}" link-type="anchor"/></default-field>
    </field>
    <field name="exampleTypeEnumId">
        <header-field title="Type">
            <drop-down allow-empty="true">
                <dynamic-options transition="getExampleTypeEnumList"/>
            </drop-down>
        </header-field>
        <default-field><display-entity entity-name="moqui.basic.Enumeration"/></default-field>
    </field>
    <field name="submitButton">
        <header-field title=" "><submit text="Find"/></header-field>
    </field>
</form-list>
```
