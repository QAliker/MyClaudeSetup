---
name: web-security
description: Use when handling anything that crosses a trust boundary in a web app — rendering user input, building a database/shell/LDAP query, auth/login/sessions, file uploads, server-side requests built from user input, setting CORS or cookies, or handling secrets. Symptoms about to happen: XSS, SQL/command injection, CSRF, SSRF, broken access control, leaked secrets, credential/session bugs.
---

# Web Security

## Overview

The gap is almost never knowledge — it's the **skipped check** under ship-it pressure. You know XSS exists; you just didn't stop to verify this one render path. This skill is a gate, not a lesson: when you touch a trust boundary, run the check before moving on.

Core principle: **never trust input, always encode output, always verify authorization server-side.**

For TS/JS-specific sinks (`eval`, `dangerouslySetInnerHTML`, prototype pollution, supply chain), also use `javascript-typescript-security`.

## Fires when you are about to

- render/interpolate any user-controlled value into HTML, SQL, a shell command, a URL, or a template
- read/write auth, login, sessions, tokens, or permissions
- accept a file upload or a redirect target
- make a server-side request to a URL derived from user input
- set CORS, cookies, or security headers
- touch a secret (API key, DB password, token)

If none of these → this skill doesn't apply, move on.

## The checklist

**XSS** — never concatenate untrusted data into HTML. Use the framework's auto-escaping (React/Vue/Angular escape by default). Escape by *context* (HTML body ≠ attribute ≠ JS ≠ URL). Avoid raw-HTML sinks; if unavoidable, sanitize (DOMPurify). Add a Content-Security-Policy.

**Injection** — parameterized queries / prepared statements, always. Never build SQL, shell, LDAP, or NoSQL queries by string concatenation. Validate against an allowlist, not a denylist.

**Access control** — check authorization on the **server, every request**, for the specific object (not just "is logged in" — "may *this* user touch *this* row"). Never trust client-sent role/ownership. This is the #1 real-world breach class.

**Auth & sessions** — cookies `HttpOnly` + `Secure` + `SameSite`. Rotate session id on login. Hash passwords with bcrypt/argon2, never fast hashes. Rate-limit login.

**CSRF** — state-changing requests need a CSRF token or `SameSite=Strict/Lax` cookies. GET must never mutate.

**SSRF** — outbound URL from user input: allowlist hosts, block internal ranges (169.254.*, 10.*, localhost, metadata endpoints).

**Secrets** — never in code, repo, or logs. Env var / secret manager. Assume anything shipped to the browser is public.

**Transport** — HTTPS everywhere, HSTS. No secrets or tokens in URLs (they land in logs/referrers).

## Rationalizations — all rejected

| Excuse | Reality |
|---|---|
| "It's an internal tool" | Internal tools get exposed, SSRF'd, or attacked by insiders. Check anyway. |
| "The input is trusted / it's our own frontend" | The client is attacker-controlled. Any request can be forged. Validate server-side. |
| "Framework handles it" | Only for the default path. Raw-HTML sinks, string queries, and manual routes bypass it. |
| "I'll add auth checks later" | Later = the breach. Add the authz check with the endpoint. |
| "It's just a prototype" | Prototypes ship. Parameterized queries and escaping cost nothing now. |

## Red flags — stop immediately

- a query string built with `+`, template literals, or f-strings around user input
- any HTML built by string concatenation from user data
- an endpoint that mutates data with no server-side ownership/permission check
- a secret literal in source
- `Access-Control-Allow-Origin: *` together with credentials
- a redirect or server-side fetch whose target comes from the request
