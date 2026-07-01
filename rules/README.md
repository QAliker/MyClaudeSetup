# Rules

Always-on guidelines. Unlike skills (recognition-gated, auto-loaded by the
plugin), rules are unconditional — they only take effect if you wire them into
your own config. The plugin does **not** auto-load this directory.

## Install

Import from `~/.claude/CLAUDE.md`:

```markdown
@./rules/ecc/common/coding-style.md
@./rules/ecc/common/git-workflow.md
@./rules/ecc/common/performance.md
```

Or copy the files into `~/.claude/rules/ecc/` and import from there.

## Scope

These are **always-on conventions**, not techniques. Anything recognition-gated
(security, testing, design patterns, migrations) lives in `skills/` instead — a
rule and a skill covering the same ground will drift apart. Keep this dir for
things that are true on every task regardless of context.

## Files

| File | Covers |
|---|---|
| `common/coding-style.md` | Immutability, file organization |
| `common/git-workflow.md` | Commit format, PR process |
| `common/performance.md` | Model selection, context management |
