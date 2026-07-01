# QT-claude-kit

Quentin's personal Claude Code kit. Portable plugin: agents, skills, and commands (hooks + scripts later).

## Agents

| Agent | Job |
|---|---|
| `e2e-runner` | Run Playwright E2E suites, diagnose failures, fix flaky tests |
| `refactor-cleaner` | Find + remove dead code, verify with tests/build |
| `doc-updater` | Sync docs/README/comments with code |
| `docs-lookup` | Look up library/API docs (local + web), sourced answers |
| `database-reviewer` | Review schema, migrations, queries (advisory) |
| `ts-js-reviewer` | TS/JS-specific review (advisory) |

## Commands

| Command | Job |
|---|---|
| `/build-fix` | Fix build/compile errors — minimal fix, re-run until green |
| `/code-review` | Read-only ranked review (bugs, security, quality) |
| `/refactor-clean` | Dispatch `refactor-cleaner` to remove dead code safely |
| `/update-docs` | Dispatch `doc-updater` to sync docs with code |
| `/skill-create` | Author a new skill via the `writing-skills` TDD flow |

## Skills

Auto-loaded by trigger; no manual invocation needed.

| Skill | Fires when |
|---|---|
| `e2e-testing` | Authoring end-to-end tests |
| `js-ts-testing` | Writing unit/integration tests in JS/TS |
| `web-security` | Touching a trust boundary (input, queries, auth, uploads, secrets) |
| `javascript-typescript-security` | JS/TS sinks — raw-HTML, eval, prototype pollution, supply chain |
| `database-migrations` | Schema changes against live data (zero-downtime) |
| `postgres-patterns` | Postgres-specific SQL — indexing, JSONB, locking, slow queries |
| `api-design` | Designing/changing an HTTP/REST surface |
| `backend-patterns` | Structuring backend code — when a design pattern earns its cost |
| `frontend-patterns` | Structuring UI/component code — state, composition, when to abstract |
| `docker-patterns` | Writing a Dockerfile / image build |
| `deployment-patterns` | Shipping to prod — rollout, rollback, health, config |

## Companion plugins

This kit runs alongside these plugins (installed separately):

| Plugin | Marketplace | What it does |
|---|---|---|
| `caveman` | caveman | Terse "smart caveman" prose mode |
| `ponytail` | ponytail | Lazy-senior-dev minimalism (YAGNI, shortest working diff) |
| `security-guidance` | claude-code-plugins | Security hooks that warn on risky patterns |
| `superpowers` | claude-plugins-official | Skills framework (brainstorming, TDD, writing-skills, …) |
| `impeccable` | impeccable | Frontend design — UI/visual design guidance |

## Install

This repo is both a marketplace and the plugin.

```bash
# local (this machine)
/plugin marketplace add ~/QT-claude-kit
/plugin install QT-claude-kit@QT-claude-kit

# another machine (after pushing to GitHub)
/plugin marketplace add <you>/QT-claude-kit
/plugin install QT-claude-kit@QT-claude-kit
```

## Layout

```
.claude-plugin/
  plugin.json        # plugin manifest
  marketplace.json   # so /plugin can install it
agents/              # subagents (*.md)
skills/              # auto-loaded skills (<name>/SKILL.md)
commands/            # slash commands (*.md)
# hooks/ scripts/  ← added later
```

Adding more later: drop `hooks/`/`scripts/` dirs at root, bump `version` in both json files.
