# Changelog

Notable changes per version. Format loosely follows
[Keep a Changelog](https://keepachangelog.com); versions are the `version`
field in `plugin.json` / `marketplace.json`.

## 0.10.0 — 2026-07-01

### Added
- `hooks/` — first hooks, auto-loaded via `hooks/hooks.json`:
  - `commit-guard` (PreToolUse/Bash) — blocks `git commit`/`git push` (incl. `rtk git commit`); the human commits, not the agent.
  - `auto-format` (PostToolUse/Edit·Write) — formats the edited file when a formatter is installed (gofmt/ruff/black/rustfmt; prettier only when configured); best-effort, never fails the edit.
- `"hooks"` reference in `plugin.json`.

## 0.9.0 — 2026-07-01

### Added
- Rule `common/skill-index` — trigger→skill map so skills get invoked even when auto-trigger misses, plus security non-negotiables that hold with no skill loaded.

## 0.8.0 — 2026-07-01

### Added
- `rules/` — opt-in always-on conventions (`@import` from `CLAUDE.md`, not auto-loaded): `common/coding-style`, `common/git-workflow`, `common/performance`.

## 0.7.0 — 2026-07-01

### Added
- Commands: `/build-fix`, `/code-review`, `/refactor-clean`, `/update-docs`, `/skill-create`.
- README: companion-plugins section (caveman, ponytail, security-guidance, superpowers, impeccable).

## 0.6.0 — 2026-07-01

### Added
- Skills: `docker-patterns`, `js-ts-testing`, `postgres-patterns`, `deployment-patterns`.

## 0.5.0 — 2026-07-01

### Added
- Recognition-gate skills: `backend-patterns`, `frontend-patterns`, `api-design`.

## 0.4.0 — baseline

- Agents: `e2e-runner`, `refactor-cleaner`, `doc-updater`, `docs-lookup`, `database-reviewer`, `ts-js-reviewer`.
- Skills: `e2e-testing`, `database-migrations`, `web-security`, `javascript-typescript-security`.
- Plugin + marketplace manifests.

_(History before 0.4.0 not tracked.)_
