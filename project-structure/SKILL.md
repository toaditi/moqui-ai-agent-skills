---
name: project-structure
description: Overview of the Moqui directory layout and guidelines on where to place specific artifacts.
---

# Skill: project-structure

## Goal
Ensure all Moqui artifacts are placed in the correct directory according to the framework's component-based architecture for proper discovery and execution.

## Triggers
**ALWAYS** read this skill when:
- Creating a new Moqui component.
- Adding new entities, services, screens, or scripts to an existing component.
- Organizing file structures within `runtime/component`.

## Use when
- Determining the correct path for a new XML Screen or Groovy script.
- Verifying if a file belongs in `framework/` or `runtime/`.

## Don't use when
- Editing the content of a file (use `manage-services`, `manage-entities`, etc., for specific content).

## Inputs
- The type of artifact to be created (e.g., "I need to add a new REST API").
- The target component name.

## Outputs
- The correct absolute or relative path for the new artifact.

## Rules & Guardrails
1. **Never modify `framework/`**: All custom development happens in `runtime/component/`.
2. **Standard Internal Layout**:
    - `entity/`: Data Model (`.xml`).
    - `service/`: Service Definitions (`.xml`, `.rest.xml`).
    - `script/`: Business Logic (`.groovy`).
    - `screen/`: UI Screens (`.xml`).
    
    | Directory | Description | Example Files |
    |---|---|---|
    | `data/` | Seed and Demo data | `MySeedData.xml`, `MyDemoData.xml` |
    | `template/` | FreeMarker Macros/Templates | `MyMacros.ftl`, `EmailTemplate.ftl` |
    | `webapp/` | Static/Web resources | `css/`, `js/`, `images/` |
    | `lib/` | Java libraries (JARs) | `custom-logic.jar` |
3. **Package Matching**: Subdirectories under `service/` and `script/` SHOULD match the logical package (e.g., `service/co/hotwax/...`).
4. **Single Responsibility**: Keep component boundaries clear. Don't put "Order" logic in a "Product" component unless it's a cross-cutting bridge.

## Failure handling
- **Path Verification**: If an artifact is not being loaded by the Moqui server, re-check this skill to ensure it's in a standard directory that Moqui scans.

## Minimal example
**Requirement**: Add a new background job script.

**Bad Path**:
`runtime/component/my-app/background_job.groovy` (Root level of component is not scanned for scripts).

**Good Path**:
`runtime/component/my-app/script/co/hotwax/jobs/BackgroundJob.groovy` (Scanned and follows package convention).
