# Git workflow

Always-on.

## The human commits

Do **not** commit or push unless explicitly asked. Stage nothing on your own.
When work is done, say so and leave the commit to the human.

## Commit messages

Conventional Commits:

```
<type>(<scope>): <subject>
```

- `type`: feat, fix, docs, refactor, test, chore, perf, build, ci
- `subject`: imperative, lowercase, no trailing period ("add retry", not "Added retry.")
- Body (optional): the *why*, not the *what* — the diff shows what.
- One logical change per commit. Don't bundle a refactor with a feature.

## Branches & PRs

- Never commit to the default branch directly — branch first.
- Branch name: `<type>/<short-desc>` (`fix/token-expiry`).
- PR description: what changed, why, how to verify. Link the issue.
- Keep PRs small enough to review in one sitting.
