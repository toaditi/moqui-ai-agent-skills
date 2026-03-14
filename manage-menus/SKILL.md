---
name: manage-menus
description: Manage Moqui navigation and menu structures, focusing on screen integration and permission-based filtering.
---

# Skill: manage-menus

## Goal
Manage Moqui application navigation by defining and organizing menu structures that are automatically filtered by user permissions and consistent across the application.

## Triggers
**ALWAYS** read this skill when:
- Organizing navigation in a root or application screen.
- Adjusting menu titles, indices, or visibility of subscreens.
- Configuring menu-level images or icons.

## Use when
- Designing the main navigation bar for a Moqui component.
- Creating sidebar menus or secondary navigation levels.
- Controlling which screens appear in the menu vs those that are functional-only.

## Don't use when
- Implementing the widgets on a screen (use `manage-screens`).

## Inputs
- Application structure and screen hierarchy.
- User roles and navigation requirements.

## Outputs
- `menu-*` attributes and `<subscreens-item>` configurations in XML screens.

## Rules & Guardrails
1. **Menu Inclusion**:
    - Every `<subscreens-item>` is included in the menu by default.
    - Use `menu-include="false"` to hide a subscreen from the navigation while keeping it accessible via direct URL/link.
2. **Ordering & Labels**:
    - Use `menu-index` to control the order (lower numbers first).
    - Use `menu-title` for the text displayed in the menu.
    - Set `default-menu-title` at the `<screen>` level to define its label in parent menus.
3. **Icons & Images**:
    - Use `menu-image` (for assets) or `fa fa-icon` (for FontAwesome icons).
    - Specify `menu-image-type="icon"` for font icons.
4. **App Level Menus**: 
    - Application-wide navigation is typically defined in a root screen (e.g., `webroot.xml` or a component-specific root like `ExampleApp.xml`).
5. **Security Filtering**: Moqui automatically hides menu items if the user does not have `AUTHZA_VIEW` permission for that specific screen. No manual filtering logic is usually required.

## Failure handling
- **Missing Menu Item**: Check if `menu-include` is accidentally set to `false` or if the user lacks permissions for the target screen.
- **Incorrect Order**: Ensure `menu-index` values are unique and logically sequenced across all siblings.

## Minimal example
**Requirement**: Define a main navigation screen with ordered items and icons.

**Good Output**:
```xml
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-3.xsd"
        menu-image="fa fa-dashboard" menu-image-type="icon">

    <subscreens default-item="Dashboard">
        <subscreens-item name="Dashboard" menu-index="1" menu-title="Home"/>
        <subscreens-item name="Reports" menu-index="2" menu-title="Analytics"/>
        <subscreens-item name="Settings" menu-index="3" menu-title="Configuration"/>
    </subscreens>
</screen>
```
