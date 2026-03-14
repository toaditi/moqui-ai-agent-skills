# Moqui AI Agent Skills

A comprehensive collection of specialized skills designed for an AI agent to architect, implement, and maintain applications within the Moqui Ecosystem.

## Component Overview

This component provides a structured set of `SKILL.md` files, each targeting a specific area of the Moqui Framework. These skills are designed to be consumed by agentic AI workflows to ensure best practices, consistent naming conventions, and rapid development.

## Deployment

To make these skills available and properly formatted for your specific AI agents, run the automated Gradle synchronization tasks from your **Moqui project root** directory.

### Synchronize Skills
Run the following base command from the Moqui root:

```bash
# Navigate to your Moqui project root
cd /path/to/moqui-framework

# Default sync: Copies to .agents/skills/
./gradlew syncAgentSkills
```

### Sync Targets individuals using the -Pagent parameter
You can target specific AI agents by passing the `-Pagent` property. This will recopy the structured files into the appropriate hidden folder for that agent.

```bash
./gradlew syncAgentSkills -Pagent=agents    # Syncs to .agents/skills/
./gradlew syncAgentSkills -Pagent=gemini    # Syncs to .gemini/skills/ (Antigravity)
./gradlew syncAgentSkills -Pagent=claude    # Syncs to .claude/skills/
./gradlew syncAgentSkills -Pagent=github    # Syncs to .github/skills/ (Copilot)
./gradlew syncAgentSkills -Pagent=cursor    # Syncs to .cursor/skills/

# Sync to all supported agents at once:
./gradlew syncAgentSkills -Pagent=all

# Sync to a subset explicitly:
./gradlew syncAgentSkills -Pagent=gemini,cursor
```

### Updating Skills
If you modify or add any content inside `runtime/component/moqui-ai-agent-skills`, you must re-run the sync command for the changes to take effect in your AI agents.

---

## Skill Categories

### 🛠 Core & Structure
- **[project-structure](project-structure/SKILL.md)**: Standard Moqui component layout and directory conventions.
- **[coding-standards](coding-standards/SKILL.md)**: Naming conventions, commenting styles, log message patterns, and professionalism.

### 📊 Data Layer
- **[manage-entities](manage-entities/SKILL.md)**: Entity modeling, relationships, and master-detail definitions.
- **[manage-view-entities](manage-view-entities/SKILL.md)**: Static and Dynamic View Entities for join-based data retrieval and optimization.
- **[manage-data](manage-data/SKILL.md)**: Seed/Demo data management via XML files.
- **[manage-data-document](manage-data-document/SKILL.md)**: Search indexing and flattened data structures for Elasticsearch/Solr.
- **[manage-data-feeds](manage-data-feeds/SKILL.md)**: Real-time and polling data synchronization (CSV/JSON feed creation).
- **[manage-data-history](manage-data-history/SKILL.md)**: Auditing and history tracking patterns.

### ⚙️ Logic & Service Layer
- **[manage-services](manage-services/SKILL.md)**: Defining services (XML/Groovy), parameters, and transaction control.
- **[manage-logic](manage-logic/SKILL.md)**: Groovy script and XML logic implementations using the `ExecutionContext`.
- **[manage-eca](manage-eca/SKILL.md)**: Event-driven logic (SECA/EECA) with priority management.
- **[manage-jobs](manage-jobs/SKILL.md)**: Scheduled tasks and background job persistent state.

### 🖥 UI Layer
- **[manage-screens](manage-screens/SKILL.md)**: Hierarchical XML screens, subscreens, and transitions.
- **[manage-forms](manage-forms/SKILL.md)**: Declarative forms, advanced layouts, and bulk updates.
- **[manage-menus](manage-menus/SKILL.md)**: Navigation, subscreen menus, and permission filtering.
- **[manage-templates](manage-templates/SKILL.md)**: Freemarker templates (FTL) and macro overrides for custom rendering.

### 🌐 Integration & Advanced
- **[manage-rest](manage-rest/SKILL.md)**: Declarative REST API mapping in `rest.xml` with advanced security options.
- **[manage-outbound-api](manage-outbound-api/SKILL.md)**: High-level `RestClient` logic covering builders, retries, and multipart requests.
- **[manage-webhooks-system-message](manage-webhooks-system-message/SKILL.md)**: Reliable messaging and status-lifecycle tracking using `SystemMessage`.
- **[manage-security](manage-security/SKILL.md)**: Access control, Permissions, and custom `ServiceArtifactAuthorizer` logic.
- **[manage-caching](manage-caching/SKILL.md)**: Performance optimization using `CacheFacade` and distributed caching.

## Usage

These skills are designed to be used with any agentic AI framework, coding assistant, or specialized LLM-based workflow. By providing these structured documents as context, you enable any AI agent to operate with deep, framework-specific expertise within the Moqui ecosystem.
