---
description: Author a new skill the right way — via the test-driven writing-skills workflow.
argument-hint: [what the skill should teach / the recurring problem it solves]
---

Create a new skill for: `$ARGUMENTS`

Do this through the **superpowers:writing-skills** skill — invoke it and follow it exactly. Do NOT freehand a SKILL.md or generate one from git history; a skill is a reusable technique, not a narrative of one solve, and writing-skills' Iron Law is *no skill without a failing test first*.

Key gates from that skill (it has the full process):

1. **Confirm it earns a skill.** Reusable across projects, non-obvious, judgment-based. Mechanical/lint-enforceable rules or one-off solutions → not a skill.
2. **Classify the failure** the skill prevents (discipline vs technique vs pattern vs reference) — it sets the form.
3. **Baseline first (RED).** Watch an agent fail without the skill; capture the exact rationalizations.
4. **Write the minimal skill (GREEN)** addressing those failures. Frontmatter `name` (hyphens only) + `description` ("Use when…", triggers only, no workflow summary).
5. **Refactor** — close loopholes, re-test under pressure.

Place it in `skills/<name>/SKILL.md`. Match the style of the existing skills in this repo. When done, bump the `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` and add the skill name to the marketplace description.
