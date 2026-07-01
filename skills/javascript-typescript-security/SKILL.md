---
name: javascript-typescript-security
description: Use when writing JavaScript/TypeScript that touches untrusted data — React/Vue raw-HTML props, dynamic code execution, object merging/cloning, regexes on user input, npm dependencies, runtime validation of external data, or Node child_process/filesystem calls. Symptoms about to happen: XSS via dangerouslySetInnerHTML/v-html, eval injection, prototype pollution, ReDoS, supply-chain compromise, secrets leaked in the client bundle, unsafe `as` casts.
---

# JavaScript / TypeScript Security

## Overview

The JS/TS-specific delta on top of `web-security` — use that skill for the universal checks (XSS, injection, access control, secrets, CORS). This one covers the sinks and footguns unique to the ecosystem. Same principle: the gap is the skipped check, not the knowledge.

## The checklist

**Raw-HTML sinks** — `dangerouslySetInnerHTML` (React), `v-html` (Vue), `bypassSecurityTrustHtml` (Angular), `.innerHTML =`. Each disables the framework's auto-escaping. Sanitize with DOMPurify first, or don't use them. Never pass user input straight in.

**Dynamic code execution** — `eval`, `new Function`, `setTimeout`/`setInterval` with a *string* arg, `import()` with a user-built path. Never with any untrusted input. There is almost always a non-eval way.

**Prototype pollution** — merging/cloning untrusted objects (`Object.assign` deep-merge, `lodash.merge`, spreading parsed JSON) can set `__proto__`/`constructor`/`prototype` and poison every object. Guard those keys, use `Object.create(null)` for maps, or a merge lib patched against it.

**ReDoS** — a catastrophic-backtracking regex (nested quantifiers like `(a+)+`) run on user input hangs the event loop → whole server stalls. Keep regexes linear; validate length first.

**Runtime validation at the boundary** — TypeScript types vanish at runtime. `as SomeType` and `any` are lies about external data (API responses, `JSON.parse`, form input, env). Validate with zod/valibot at the trust boundary; don't `as`-cast your way past it.

**Secrets in the bundle** — anything imported into client code ships to the browser and is public. `NEXT_PUBLIC_`/`VITE_` env vars are baked in. Keep real secrets server-only.

**Supply chain** — commit the lockfile, `npm audit` in CI, pin/review before upgrading. Be wary of `postinstall` scripts and typosquatted names. Fewer dependencies = smaller attack surface (a few lines often beats a new dep anyway).

**Node sinks** — `child_process.exec`/`execSync` with user input = command injection (use `execFile` with an arg array). `fs`/`path.join` with user input = path traversal (resolve and confirm it stays under the intended root).

## Rationalizations — all rejected

| Excuse | Reality |
|---|---|
| "TypeScript makes it type-safe" | Types are compile-time only. Runtime data can be anything. Validate it. |
| "It's just a dev dependency" | `postinstall` runs on your machine and CI regardless of dep type. |
| "DOMPurify is overkill here" | If it's raw HTML from a user, it's not overkill. It's the requirement. |
| "The regex is fine, it's short" | ReDoS is about structure, not length of the pattern. Check for nested quantifiers. |

## Red flags — stop immediately

- `dangerouslySetInnerHTML` / `v-html` / `.innerHTML` fed anything user-derived without sanitizing
- `eval` / `new Function` / string-arg `setTimeout` anywhere near input
- a deep-merge or clone of parsed JSON with no `__proto__` guard
- `as` or `any` on data that just crossed a network/form/file boundary
- `child_process.exec` with an interpolated command string
- a secret value reachable from client-side code
