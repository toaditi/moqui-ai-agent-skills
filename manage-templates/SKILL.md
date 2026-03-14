---
name: manage-templates
description: Manage Moqui dynamic templates using Freemarker (FTL), including screen macro overrides and custom content rendering.
---

# Skill: manage-templates

## Goal
Implement and customize dynamic UI content in Moqui using Freemarker (FTL) templates, enabling bespoke rendering logic and overriding standard screen macros for advanced user experiences.

## Triggers
**ALWAYS** read this skill when:
- Creating or modifying `*.ftl` files in a Moqui component (e.g., `template/` directories).
- Overriding default screen rendering via `<macro-template>`.
- Using `<render-mode>` to include custom HTML, XML, or Text content in a screen.

## Use when
- Building custom email templates.
- Creating advanced UI components not supported by declarative forms.
- Overriding the standard look and feel of Moqui screens globally or per-component.

## Don't use when
- Standard declarative widgets (containers, forms) are sufficient (use `manage-screens` or `manage-forms`).

## Inputs
- Content requirements (markup, styling).
- Data context available in the template (Moqui context).

## Outputs
- Freemarker template files (`.ftl`).
- `<macro-template>` or `<render-mode>` configurations in XML screens.

## Rules & Guardrails
1. **Template Location**: Store FTL files under `runtime/component/<component>/template/`.
2. **Context Access**: Access the Moqui context using `${variable}`. Use `${ec.web.getRequestAttributes().get('attr')}` to access low-level web attributes if needed.
3. **Macro Overrides**:
    - Use `<macro-template type="html" location="component://..."/>` inside a `<screen>` to change rendering for all widgets.
    - Common macro types: `html` (Standard), `vuet` (Vue templates), `qvt` (Quasar/Vue templates), `xml`, `text`, `csv`, `pdf`.
4. **Render Modes**:
    - Use `<render-mode><text type="html,vuet,qvt"><![CDATA[ ... ]]></text></render-mode>` for inline content targeting specific output formats.
    - Use `<render-mode><text type="html" location="component://.../template.ftl"/></render-mode>` for external FTL files.
5. **Freemarker Best Practices**:
    - Access Moqui context: `${field}`, `${ec.user.username}`.
    - Null safety: `${variable!''}` or `<#if variable??>`.
    - Local variables: `<#assign myVar = ...>`.

## Failure handling
- **FTL Syntax Errors**: Check the Moqui logs for detailed Freemarker stack traces.
- **Missing Variables**: Use `${variable!''}` or `<#if variable??>` to handle nulls Safely in FTL.

## Minimal example
**Requirement**: Add a custom HTML banner to a screen using an external FTL.

**Good Output (XML Screen)**:
```xml
<widgets>
    <render-mode>
        <text type="html" location="component://example/template/ExampleBanner.ftl"/>
    </render-mode>
</widgets>
```

**Good Output (ExampleBanner.ftl)**:
```html
<div class="alert alert-info">
    <h4>Welcome to ${appTitle!'Moqui Application'}</h4>
    <p>Current user: ${ec.user.username}</p>
</div>
```
