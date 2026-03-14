---
name: manage-screens
description: Define Moqui XML Screens, managing hierarchy, transitions, and widget composition.
---

# Skill: manage-screens

## Goal
Implement structured and secure Moqui XML screens, leveraging hierarchical nesting, declarative transitions, and modular widget composition for consistent user interfaces.

## Triggers
**ALWAYS** read this skill when:
- Creating or modifying Moqui screen files (`*.xml` under `screen/` directories).
- Defining UI transitions, path parameters, or subscreen hierarchies.
- Configuring screen-level security and authentication requirements.

## Use when
- Building the application's UI structure.
- Managing navigation flows between screens.
- Defining root screens or detail pages in a Moqui component.

## Don't use when
- Designing the internal fields of a form (use `manage-forms`).
- Managing raw HTML/JavaScript templates (use `manage-templates`).

## Inputs
- UI design requirements (layout, nesting).
- Navigation logic (transitions, default screens).
- Dynamic data requirements for the screen (`actions`).

## Outputs
- Schema-compliant `<screen>` definitions in `screen/*.xml`.

## Rules & Guardrails
1. **Hierarchy & Nesting**:
    - Use `<subscreens>` to define child screens.
    - Use `default-item` to specify the landing subscreen.
    - Use `<subscreens-panel>` in the `<widgets>` section to determine where child content is rendered (e.g., `type="tab"`, `type="popup"`, or standard inclusion).
2. **Execution Lifecycle**:
    - `<pre-actions>`: Use for setting UI metadata (titles, descriptions) that must be available to the decorator.
    - `<actions>`: Standard Moqui logic block for fetching data.
    - `<widgets>`: The UI tree consisting of containers, forms, and other components.
3. **Transitions & Parameters**:
    - Name transitions using `lowerCamelCase`.
    - Use `<parameter name="..." required="true"/>` at the screen level to document and validate expected path/page parameters.
    - Path parameters: Use `<path-parameter name="..."/>` in transitions for RESTful URLs (e.g., `/edit/${id}`).
    - Responses: Use `<default-response url="..." page-parameter="..." />`. Use `type="none"` for raw JSON.
4. **Security & Mode**:
    - `require-authentication="true"` (default): Login required.
    - `require-authentication="false"`: Publicly accessible screen.
    - `standalone="true"`: Use for bypass decorators (e.g., for CSV/PDF exports or sub-segments loaded via AJAX).
5. **Nesting Best Practice**: Avoid deeply nested complex logic in a single screen file. Use `subscreens` to break down large UIs into manageable partials.

## Failure handling
- **URL Resolution**: If a transition fails to resolve, verify the relative path (e.g., `../FindExample` vs `./EditExample`).
- **Data Availability**: Ensure variables set in `<actions>` are correctly referenced in `<widgets>` using `${field}` syntax.

## Minimal example
**Requirement**: Define a root screen for an Example application with two tabs.

**Good Output**:
```xml
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-3.xsd">

    <subscreens default-item="FindExample">
        <subscreens-item name="FindExample" menu-title="Find"/>
        <subscreens-item name="EditExample" menu-title="Edit" menu-include="false"/>
    </subscreens>

    <widgets>
        <subscreens-panel id="example-tabs" type="tab"/>
    </widgets>
</screen>
```
