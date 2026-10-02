# QT-claude-kit

Quentin's personal Claude Code kit. Portable plugin: agents, skills, commands, opt-in rules, and hooks (scripts later).

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
| `transitions-dev` / `transitions-polish` | Adding / tuning CSS transitions (from [transitions.dev](https://github.com/Jakubantalik/transitions.dev)) |
| `gsap-*` (core, timeline, scrolltrigger, plugins, utils, react, frameworks, performance) | GSAP animation work (official [greensock/gsap-skills](https://github.com/greensock/gsap-skills)) |
| `make-interfaces-feel-better` | UI polish / design-detail review (from [jakubkrehel/make-interfaces-feel-better](https://github.com/jakubkrehel/make-interfaces-feel-better)) |
| `graphify` | Codebase → knowledge graph, `/graphify .` (needs CLI: `uv tool install graphifyy`) |

## Rules (opt-in)

Always-on conventions. **Not auto-loaded** — wire them into `~/.claude/CLAUDE.md`
with `@import` (see `rules/README.md`). Anything recognition-gated lives in a skill instead.

| Rule | Covers |
|---|---|
| `common/skill-index` | Trigger→skill map + security non-negotiables (covers trigger-miss) |
| `common/coding-style` | Immutability, file organization |
| `common/git-workflow` | Commit format, PR process |
| `common/performance` | Model selection, context management |

## Hooks

Auto-loaded with the plugin. Mechanical guards only — judgment calls stay skills.

| Hook | Event | Does |
|---|---|---|
| `commit-guard` | PreToolUse (Bash) | Blocks `git commit`/`git push` — the human commits, not the agent |
| `auto-format` | PostToolUse (Edit/Write) | Formats the edited file if a formatter is installed (prettier only when configured); never fails the edit |

## Companion plugins

This kit runs alongside these plugins (installed separately):

| Plugin | Marketplace | What it does |
|---|---|---|
| `caveman` | caveman | Terse "smart caveman" prose mode |
| `ponytail` | ponytail | Lazy-senior-dev minimalism (YAGNI, shortest working diff) |
| `security-guidance` | claude-plugins-official | Security hooks that warn on risky patterns |
| `superpowers` | claude-plugins-official | Skills framework (brainstorming, TDD, writing-skills, …) |
| `feature-dev` | claude-plugins-official | Guided feature dev + code-explorer/architect/reviewer agents |
| `claude-md-management` | claude-plugins-official | Audit / update CLAUDE.md |
| `claude-code-setup` | claude-plugins-official | Recommends hooks, skills, MCP servers for a repo |
| `typescript-lsp` | claude-plugins-official | TS/JS diagnostics + code navigation (needs `npm i -g typescript typescript-language-server`) |
| `playwright` | claude-plugins-official | Browser MCP: navigate, click, screenshot (needs Chrome: `npx playwright install chrome`; WSL/Linux also `sudo npx playwright install-deps chromium`). Add `.playwright-mcp/` to the project `.gitignore` |
| `context7` | claude-plugins-official | Up-to-date library docs MCP |
| `impeccable` | `npx skills add` (global skills, not a plugin) | Frontend design — UI/visual design guidance |

After editing this repo, refresh the installed copy:
`claude plugin marketplace update QT-claude-kit && claude plugin update QT-claude-kit@QT-claude-kit`

## Install

This repo is both a marketplace and the plugin.

```bash
# any machine (from GitHub) — run one command at a time
/plugin marketplace add https://github.com/QAliker/MyClaudeSetup.git
/plugin install QT-claude-kit@QT-claude-kit

# local dev (this machine, live-edits the checkout)
/plugin marketplace add ~/MyClaudeSetup
/plugin install QT-claude-kit@QT-claude-kit
```

Update later:

```bash
/plugin marketplace update QT-claude-kit
```

Repo: https://github.com/QAliker/MyClaudeSetup

## Layout

```
.claude-plugin/
  plugin.json        # plugin manifest
  marketplace.json   # so /plugin can install it
agents/              # subagents (*.md)
skills/              # auto-loaded skills (<name>/SKILL.md)
commands/            # slash commands (*.md)
rules/               # opt-in always-on rules (@import from CLAUDE.md)
hooks/               # mechanical guards (hooks.json + scripts)
# scripts/  ← added later
```

Adding more later: drop `hooks/`/`scripts/` dirs at root, bump `version` in both json files.
