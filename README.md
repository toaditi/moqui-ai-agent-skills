# Moqui AI Agent Skills

A maintained fork of Moqui-focused agent skills, plus a small set of Codex-oriented testing and skill-maintenance skills that can be updated independently from upstream.

## Overview

This repo stays as the editable source of truth. Sync the skills you want into your active agent directory after you update or validate them.

## Deployment

### Sync to Codex

Use the repo-level sync helper to copy selected skills into `~/.codex/skills`:

```bash
cd /path/to/moqui-ai-agent-skills
python3 scripts/sync_skills.py \
  --dest ~/.codex/skills \
  improve-skills-from-failures verification-loop tdd-workflow e2e-testing
```

Restart Codex after syncing so the updated skills are picked up.

If you prefer Gradle, this fork also supports a Codex target:

```bash
cd /path/to/moqui-ai-agent-skills
./gradlew syncAgentSkills -Pagent=codex
```

### Sync to Moqui Agent Folders

To sync into a Moqui project checkout, point the Gradle task at the Moqui root:

```bash
cd /path/to/moqui-ai-agent-skills
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework
```

You can target specific agent directories with `-Pagent`:

```bash
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=agents
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=claude
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=github
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=cursor
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=gemini,cursor
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=codex,claude
./gradlew syncAgentSkills -PmoquiRoot=/path/to/moqui-framework -Pagent=all
```

### Updating Skills

When you change or add skill content in this fork, rerun the relevant sync command so the new version lands in the active agent directory.

## Skill Categories

### Core & Structure

- **[project-structure](project-structure/SKILL.md)**: Standard Moqui component layout and directory conventions.
- **[coding-standards](coding-standards/SKILL.md)**: Naming conventions, commenting styles, log message patterns, and professionalism.

### Data Layer

- **[manage-entities](manage-entities/SKILL.md)**: Entity modeling, relationships, and master-detail definitions.
- **[manage-view-entities](manage-view-entities/SKILL.md)**: Static and Dynamic View Entities for join-based data retrieval and optimization.
- **[manage-data](manage-data/SKILL.md)**: Seed and demo data management via XML files.
- **[manage-data-document](manage-data-document/SKILL.md)**: Search indexing and flattened data structures for Elasticsearch or Solr.
- **[manage-data-feeds](manage-data-feeds/SKILL.md)**: Real-time and polling data synchronization patterns.
- **[manage-data-history](manage-data-history/SKILL.md)**: Auditing and history tracking patterns.

### Logic & Service Layer

- **[manage-services](manage-services/SKILL.md)**: Defining services, parameters, and transaction control.
- **[manage-logic](manage-logic/SKILL.md)**: Groovy script and XML logic implementations using the `ExecutionContext`.
- **[manage-eca](manage-eca/SKILL.md)**: Event-driven logic with SECA and EECA patterns.
- **[manage-jobs](manage-jobs/SKILL.md)**: Scheduled tasks and background job state.

### UI Layer

- **[manage-screens](manage-screens/SKILL.md)**: Hierarchical XML screens, subscreens, and transitions.
- **[manage-forms](manage-forms/SKILL.md)**: Declarative forms, layouts, and bulk updates.
- **[manage-menus](manage-menus/SKILL.md)**: Navigation, subscreen menus, and permission filtering.
- **[manage-templates](manage-templates/SKILL.md)**: Freemarker templates and macro overrides for custom rendering.

### Integration & Advanced

- **[manage-rest](manage-rest/SKILL.md)**: Declarative REST API mapping in `rest.xml`.
- **[manage-outbound-api](manage-outbound-api/SKILL.md)**: `RestClient` builders, retries, and multipart requests.
- **[manage-webhooks-system-message](manage-webhooks-system-message/SKILL.md)**: Reliable messaging and lifecycle tracking using `SystemMessage`.
- **[manage-security](manage-security/SKILL.md)**: Access control, permissions, and custom authorizers.
- **[manage-caching](manage-caching/SKILL.md)**: Performance optimization using `CacheFacade` and distributed caching.

### Testing & Skill Maintenance

- **[verification-loop](verification-loop/SKILL.md)**: Build, typecheck, lint, test, and security verification workflow.
- **[tdd-workflow](tdd-workflow/SKILL.md)**: Test-first workflow with coverage expectations and feedback loops.
- **[e2e-testing](e2e-testing/SKILL.md)**: Playwright E2E patterns, debugging, and flake reduction.
- **[improve-skills-from-failures](improve-skills-from-failures/SKILL.md)**: Turns repeated failures into targeted updates for the relevant skills.

## Usage

These skills are meant to be maintained here, then synced outward to the agent environment that should use them. For Codex, keep this repo as the editable source of truth and sync only the skills you want active in `~/.codex/skills`.
