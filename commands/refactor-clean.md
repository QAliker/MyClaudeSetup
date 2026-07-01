---
description: Remove dead code, unused exports/deps, and redundant abstractions — safely.
argument-hint: [optional: path or module to scope the cleanup]
---

Dispatch the **refactor-cleaner** agent to find and remove dead code, unused exports/dependencies, and redundant abstractions, proving nothing breaks with the project's build + tests.

Scope the cleanup to `$ARGUMENTS` if given; otherwise the whole repo.

Relay the agent's report: what was removed, why it was safe, and anything flagged-but-not-deleted because it couldn't be proven dead. The agent deletes conservatively and ends with build + test output as proof — do not delete anything it couldn't prove unused.
