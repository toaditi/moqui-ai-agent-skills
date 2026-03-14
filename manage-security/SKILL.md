---
name: manage-security
description: Manage Moqui security artifacts, artifact groups, and access control policies.
---

# Skill: manage-security

## Goal
Secure Moqui resources (services, screens, entities) by grouping them into logically related Artifact Groups and defining fine-grained authorization policies.

## Triggers
**ALWAYS** read this skill when:
- Defining new security artifacts or groups in a Moqui component (XML data files).
- Restricting access to a specific service or entity based on user roles or groups.
- Troubleshooting "Access Denied" errors for REST APIs, services, or screens.

## Use when
- Creating an `ArtifactGroup` to bundle related business operations (e.g., "OrderManagementServices").
- Mapping artifacts (Services, Screens, Transitons) to a group via `ArtifactGroupMember`.
- Defining authorization for a group via `ArtifactAuthz`.

## Don't use when
- Managing user accounts or passwords (handled by Moqui User/Auth logic).

## Inputs
- Resource names (full service name, screen path, or entity name).
- Artifact type (`AT_SERVICE`, `AT_ENTITY`, `AT_XML_SCREEN`, `AT_REST_PATH`).
- Authorization levels (View, Create, Update, Delete).

## Outputs
- Moqui XML security data files (typically `data/*SecurityData.xml`).

## Rules & Guardrails
1. **Artifact Groups**: Group artifacts by functional area or API version (e.g., `PoortiAdminAPI`).
2. **Artifact Names**:
    - Services: `full.package.Service#name`.
    - Entities: `full.package.Entity`.
    - Screens: Use the full path (e.g., `component://example/screen/Example.xml`).
3. **Inheritance**: Authorization on a screen artifact inherently covers its child subscreens and transitions unless overridden.
4. **Member Mapping**: Use `moqui.security.ArtifactGroupMember` to link artifacts to groups. Use `inheritAuthz="Y"` for screens to simplify parent-child security.
5. **Authorization Strategy**: Use `ArtifactAuthz` to link a `UserGroup` to an `ArtifactGroup` with specific `authzTypeEnumId` (e.g., `AUTHZ_ALL`, `AUTHZ_VIEW`).
6. **Custom Logic**: Implement `org.moqui.context.ServiceArtifactAuthorizer` for custom, logic-based authorization that can't be expressed declaratively.
7. **Preferences**: Use `moqui.security.user.UserGroupPreference` for granular, group-specific settings (e.g., restricted IP ranges).

## Failure handling
- **Access Denied**: Verify that BOTH the artifact is in an `ArtifactGroup` AND the user's `UserGroup` has an `ArtifactAuthz` for that group.
- **Ambiguous Mapping**: If multiple groups cover the same artifact, Moqui evaluates according to priority/specificity rules.

## Minimal example
**Requirement**: Create a security group for the 'Example' component and grant access to the 'User' group.

**Good Output (XML Data)**:
```xml
<entity-engine-xml>
    <!-- Define the Group -->
    <moqui.security.ArtifactGroup artifactGroupId="ExampleGroup" description="Example Component Artifacts"/>

    <!-- Add Services/Entities to Group -->
    <moqui.security.ArtifactGroupMember artifactGroupId="ExampleGroup" 
        artifactName="moqui.example.Example" artifactTypeEnumId="AT_ENTITY" inheritAuthz="Y"/>
    <moqui.security.ArtifactGroupMember artifactGroupId="ExampleGroup" 
        artifactName="moqui.example.ExampleServices.create#Example" artifactTypeEnumId="AT_SERVICE"/>

    <!-- Grant Authorization -->
    <moqui.security.ArtifactAuthz artifactGroupId="ExampleGroup" 
        userGroupId="USER" authzTypeEnumId="AUTHZ_ALL" authzActionEnumId="AUTHZ_ALL"/>
</entity-engine-xml>
```
