---
description: Review code for bugs, security, and quality — reports ranked findings, does not edit.
argument-hint: [optional: files, a diff range like main..HEAD, or a PR]
---

Review code for correctness, security, and quality. This is read-only — report findings, do not fix unless the user then asks.

## Scope

- If `$ARGUMENTS` names files, a diff range, or a PR → review exactly that.
- Otherwise → review the working changes (`git diff` + staged). If the tree is clean, ask what to review rather than reviewing the whole repo.

## What to look for (ranked by severity when reporting)

1. **Bugs / logic errors** — off-by-one, null/undefined, wrong operator, unhandled error path, race conditions, incorrect async/await.
2. **Security** — apply `web-security` and, for JS/TS, `javascript-typescript-security`: injection, XSS, broken authz, secrets, SSRF, unsafe sinks.
3. **Data safety** — migrations (`database-migrations`), transaction scope, N+1 / unbounded queries (`postgres-patterns`).
4. **Correctness of contracts** — API breaking changes (`api-design`), wrong status codes, missing validation at trust boundaries.
5. **Quality** — dead code, needless complexity/abstraction (prefer deletion), unclear naming, missing error handling.

For a deeper TS/JS pass, or a dedicated reviewer, dispatch the `ts-js-reviewer` or `feature-dev:code-reviewer` agent.

## Report format

- Group by severity: **Must fix** / **Should fix** / **Nit**.
- Each finding: `file:line` — one-sentence defect + concrete failure scenario (inputs → wrong result).
- Only report what you're confident is a real issue. No style nits the linter already enforces. If nothing's wrong, say so.
