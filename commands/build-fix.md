---
description: Fix build/compile errors — read the failure, locate the cause, apply the minimal fix, re-run until green.
argument-hint: [optional build command, e.g. npm run build]
---

Fix the project's build. Do NOT add features or refactor — the goal is a green build with the smallest change.

## Steps

1. **Run the build.** Use `$ARGUMENTS` if given; otherwise detect it (package.json scripts, Makefile, cargo, go build, etc.). Capture the exact error output.
2. **Read the first real error, not the last.** Cascading errors usually trace to one root cause upstream. Fix that first; many others vanish.
3. **Locate the cause** — open the file/line the error names. Confirm the actual problem (missing import, type mismatch, renamed symbol, bad config), don't guess from the message alone.
4. **Apply the minimal fix.** Match surrounding code. No opportunistic rewrites, no new dependencies unless the error is literally a missing one the project already expects.
5. **Re-run the build.** Repeat from step 2 until it passes.
6. **Report** — each error, its root cause, and the one-line fix. If an error needs a real decision (API removed, ambiguous intent), stop and surface it instead of forcing a fix.

## Rules

- Smallest diff that makes it compile. Don't "improve" working code.
- Don't silence errors (blanket `any`, `@ts-ignore`, `# type: ignore`, disabling a lint) unless there is genuinely no correct fix — and then say so explicitly.
- End with the passing build output as proof.
