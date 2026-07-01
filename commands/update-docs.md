---
description: Update documentation to match the current code — README, docstrings, comments, changelog.
argument-hint: [optional: doc file or area to update]
---

Dispatch the **doc-updater** agent to bring documentation in line with the current code.

Scope to `$ARGUMENTS` if given; otherwise find docs affected by recent changes (README, API docs, docstrings, comments, changelog) and update those.

Relay what the agent changed. Docs must describe what the code actually does now — no aspirational or stale claims. If code and docs contradict and it's unclear which is right, surface it rather than guessing.
