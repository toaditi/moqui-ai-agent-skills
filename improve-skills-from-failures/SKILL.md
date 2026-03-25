---
name: improve-skills-from-failures
description: Use this skill when test, build, lint, runtime, or E2E failures reveal missing guidance in an existing skill. It turns concrete failure evidence into focused updates to the right skill instead of repeating the same mistake.
---

# Improve Skills From Failures

## Overview

Use this skill after a real failure has been observed and you need to decide whether an existing skill should change. It separates one-off environment noise from actual skill gaps, then patches the smallest useful instruction, guardrail, or reference needed to prevent recurrence.

## Triggers

Use this skill when:
- A unit, integration, E2E, lint, typecheck, or build failure repeats across tasks.
- A test failure exposes a missing prerequisite, validation step, or guardrail in another skill.
- An agent followed a skill and still made a predictable mistake that better instructions could have prevented.
- A Moqui-specific error shows that the framework skill covered the wrong pattern or omitted a key distinction.

Do not use this skill for:
- Random CI noise with no stable pattern.
- Missing dependencies, credentials, or local setup problems that belong in environment docs or scripts.
- Product bugs where the code should change but the skill guidance was already adequate.

## Inputs

Collect the smallest useful evidence set before editing anything:
- The exact failing command.
- The error output or stack trace excerpt.
- The files or paths involved.
- The skill or skills that were active when the failure happened.
- The change, if any, that fixed the failure.

If you need a compact template, use [failure-review-template.md](references/failure-review-template.md).

## Workflow

### 1. Confirm it is a skill gap
Ask:
- Did the failure happen because the skill omitted a step that should usually happen?
- Did the skill recommend a fragile pattern or fail to warn about a known pitfall?
- Would a concise instruction change have prevented the mistake for a future run?

If the answer is no, do not edit the skill. Fix code, environment, or project docs instead.

### 2. Pick the right update target
Prefer updating the narrowest skill that owns the mistake:
- Verification failures: `verification-loop`
- Test-first workflow gaps: `tdd-workflow`
- Playwright or flake patterns: `e2e-testing`
- Moqui implementation mistakes: the relevant `manage-*`, `coding-standards`, or `project-structure` skill

Create a new skill only when the pattern does not belong inside an existing one.

### 3. Make the smallest durable change
Use one or more of these changes:
- Add a trigger so the skill is invoked earlier.
- Add a guardrail that names the failure mode explicitly.
- Add a verification step with the exact command shape to run.
- Add a reference file when the pattern is real but too detailed for `SKILL.md`.
- Add or update a helper script only when deterministic automation is better than prose.

Do not add long postmortems, project-specific noise, or vague advice.

### 4. Phrase the lesson using evidence
Good updates are concrete:
- Name the failing tool or command category.
- Name the condition that caused the failure.
- State the prevention step in imperative form.
- Keep examples short and realistic.

Bad updates are vague:
- "Be careful with tests"
- "Make sure everything is installed"
- "Sometimes Playwright fails for timing reasons"

### 5. Re-run the relevant verification
After updating the skill, re-run the closest failing check when possible. The goal is not to prove the skill caused the fix by itself, but to ensure the documented lesson matches reality.

### 6. Keep the repo as source of truth
Make changes in this maintained skills repo first. Then sync the affected skills into the active agent directory only after the update is useful and validated.

## Update Rules

- Prefer editing an existing skill over creating a duplicate.
- Prefer a 3-line guardrail over a 30-line essay.
- Do not encode secrets, machine-specific paths, or temporary outages as permanent guidance.
- Do not turn a code bug into a skill change unless the skill genuinely misled the implementation.
- When a failure is repo-specific, scope the instruction to the relevant framework, folder, or task.
- If the fix requires a new command, include the exact command shape.

## Typical Targets

- `verification-loop`: missing validation order, missing gates, wrong failure-reporting format
- `tdd-workflow`: missing test-first discipline, weak coverage expectations, missing edge-case prompts
- `e2e-testing`: flake signatures, wrong wait strategy, bad artifact capture, missing retry guidance
- `coding-standards`: naming, logging, Moqui-vs-OFBiz confusion, comment quality
- `manage-services`, `manage-rest`, `manage-screens`, and similar: framework-specific failure patterns

## Output

When you use this skill, produce:
- A short diagnosis of whether the failure reflects a skill gap.
- The specific skill or skills to update.
- The exact patch or guidance change to make.
- The verification command to rerun after the update.

## Resources

### references/
Use [failure-review-template.md](references/failure-review-template.md) to capture a failure cleanly before changing another skill.
