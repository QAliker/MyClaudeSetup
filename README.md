# QT-claude-kit

Quentin's personal Claude Code kit. Portable plugin: agents now; skills, commands, hooks, scripts later.

## Agents

| Agent | Job |
|---|---|
| `e2e-runner` | Run Playwright E2E suites, diagnose failures, fix flaky tests |
| `refactor-cleaner` | Find + remove dead code, verify with tests/build |
| `doc-updater` | Sync docs/README/comments with code |
| `docs-lookup` | Look up library/API docs (local + web), sourced answers |
| `database-reviewer` | Review schema, migrations, queries (advisory) |
| `ts-js-reviewer` | TS/JS-specific review (advisory) |

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
# skills/ commands/ hooks/ scripts/  ← added later
```

Adding more later: drop `skills/`, `commands/`, `hooks/` dirs at root, bump `version` in both json files.
