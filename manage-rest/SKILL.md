---
name: manage-rest
description: Define and manage Moqui declarative REST API structures in rest.xml files.
---

# Skill: manage-rest

## Goal
Declaratively define RESTful APIs in Moqui by mapping HTTP verbs to services and entities, organizing resources into logical hierarchies with proper path parameters.

## Triggers
**ALWAYS** read this skill when:
- Creating or modifying `*.rest.xml` files in a Moqui component (usually under `service/`).
- Mapping web requests to Moqui services or entities for external consumption.
- Configuring authentication and authorization requirements for specific REST endpoints.

## Use when
- Exposing existing Moqui services as public or private REST endpoints.
- Building standard CRUD-based REST APIs for entities (e.g., Products, Orders).
- Organizing complex API paths using hierarchical `resource` and `id` tags.

## Don't use when
- Implementing the underlying business logic (use `manage-services` and `manage-logic`).
- Handling outbound REST calls (use `manage-outbound-api`).

## Inputs
- API path structure and endpoints.
- Moqui services or entities to map.
- Authentication requirements (`anonymous-view`, `anonymous-all`, or default).

## Outputs
- Accurate `rest.xml` files registered via Moqui's service loader.

## Rules & Guardrails
1. **Verb Mapping Best Practice**:
    - `GET` -> `operation="list"` or `operation="one"` (entities) / find-based services.
    - `POST` -> `create` operations.
    - `PATCH/PUT` -> `update` or `store` operations.
    - `DELETE` -> `delete` operations.
2. **Resource Hierarchy**: Use `<resource>` for segments and `<id>` for path parameters (e.g., `/{exampleId}`).
3. **Master Names**: Use `masterName="default"` (or a specific master definition) in `<entity>` one/list operations to return hierarchical object graphs.
4. **Security**: Use `require-authentication` at resource, id, or method level. Values: `true` (default), `false`, `anonymous-all`, `anonymous-view`.
5. **Extra Path**: Use `allow-extra-path="true"` on `<id>` to allow arbitrary path segments following the ID (accessible via `ec.web.getPathInfo()`).
6. **Naming**: Use `lowerCamelCase` for resource names to follow RESTful conventions.
7. **Versioning**: Use the `version` attribute on the root `<resource>` tag to track API iterations.

## Failure handling
- **Path Conflicts**: Ensure resource names and IDs don't overlap in a way that creates ambiguous routes.
- **Master Detail Missing**: If an object graph doesn't return related records, ensure the `<master>` definition exists on the entity.

## Minimal example
**Requirement**: Create a REST API for 'Example' with sub-resource for 'Items'.

**Good Output (`example.rest.xml`)**:
```xml
<resource name="example" displayName="Example API" version="1.0.0">
    <resource name="examples">
        <method type="get"><entity name="moqui.example.Example" operation="list"/></method>
        <method type="post"><service name="create#moqui.example.Example"/></method>

        <id name="exampleId">
            <method type="get"><entity name="moqui.example.Example" masterName="default" operation="one"/></method>
            <method type="patch"><service name="update#moqui.example.Example"/></method>

            <resource name="items">
                <method type="get"><entity name="moqui.example.ExampleItem" operation="list"/></method>
                <id name="exampleItemSeqId">
                    <method type="get"><entity name="moqui.example.ExampleItem" operation="one"/></method>
                    <method type="delete"><entity name="moqui.example.ExampleItem" operation="delete"/></method>
                </id>
            </resource>
        </id>
    </resource>
</resource>
```
