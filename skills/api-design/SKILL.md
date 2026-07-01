---
name: api-design
description: Use when designing or changing an HTTP/REST API surface — modeling resources and URLs, choosing methods and status codes, shaping request/response bodies, pagination, filtering, errors, versioning, or idempotency. Symptoms: about to add an endpoint, name a route, return an error shape, break an existing response, verb-in-URL like /getUser or /doAction, unbounded list, or unsure how clients evolve without breaking.
---

# API Design

## Overview

An API is a contract: once a client depends on it, the shape is expensive to change. The failure mode isn't not knowing REST — it's shipping an inconsistent surface (ad-hoc URLs, random status codes, unversioned breaking changes) that clients then lock in. Decide the conventions once; apply them everywhere.

Core principle: **model resources not actions, be predictable, and never break an existing client silently.**

For authz/injection/CORS on these endpoints use `web-security`. This skill is about the *contract shape*.

## The checklist

**Resources, not verbs.** URLs name nouns; the HTTP method is the verb. `GET /users/42`, `DELETE /users/42` — not `/getUser?id=42` or `POST /deleteUser`. An action that isn't CRUD → model it as a resource (`POST /transfers`) or a sub-resource (`POST /orders/42/refunds`).

**Methods & status codes carry meaning.** GET (safe, no side effects), PUT/PATCH (update, idempotent), POST (create/action), DELETE. Return the right class: 200/201 with body, 204 empty, 400 client bad input, 401 unauthenticated vs 403 unauthorized, 404, 409 conflict, 422 validation, 429 rate limit, 5xx server. Never 200 with `{"error": ...}`.

**Consistent bodies.** Pick one case convention (snake or camel) and one date format (ISO-8601/UTC) across the whole API. Wrap collections so you can add metadata later. One error envelope everywhere: `{ error: { code, message, details } }` — a stable machine `code`, not just prose.

**Pagination — always, from day one.** Any list that can grow needs bounds. Cursor-based for large/changing sets (stable, no skipped rows); offset/limit only for small stable data. An unbounded list endpoint is a future outage.

**Idempotency for unsafe retries.** POST that moves money or has side effects → accept an `Idempotency-Key` so a retry doesn't double-charge. PUT/DELETE should already be idempotent by definition.

**Versioning before the first breaking change.** Additive changes (new optional field, new endpoint) don't need a version bump — clients ignore unknowns. Removing/renaming a field or changing a type IS breaking → version it (`/v2`, header, or media type) and keep the old one until clients migrate.

## What is a breaking change

| Safe (additive) | Breaking (version it) |
|---|---|
| Add a new optional request field | Add a *required* request field |
| Add a field to a response | Remove/rename a response field |
| Add a new endpoint or method | Change a field's type or meaning |
| Add a new optional query param | Change status code or error shape |
| Loosen validation | Tighten validation on existing input |

Assume clients ignore unknown fields and depend on every field you send.

## When NOT to over-design

- **No HATEOAS / hypermedia** unless a client actually consumes links. It's ceremony almost no one uses. (YAGNI)
- **No GraphQL/gRPC "for flexibility"** when a handful of REST endpoints serve the need. Match the protocol to a real client requirement.
- **Don't version on day one.** Ship `/v1` (or unversioned) and only branch when the first breaking change is real.
- **Don't invent custom methods/verbs** when a resource models it. `POST /orders/42/cancel` is a fine pragmatic action; a whole RPC vocabulary is not.

## Common mistakes

- **Verb-in-URL RPC over HTTP.** `/api/doThing` throws away everything HTTP gives you (caching, methods, status). Model the noun.
- **Inconsistent naming/casing across endpoints.** `user_id` here, `userId` there — clients hit it constantly. Lint it.
- **Unbounded lists.** `GET /users` returning all rows works in dev, times out in prod. Paginate from the start.
- **Leaking internals.** Exposing DB column names, auto-increment IDs, or stack traces in errors couples clients to your storage and leaks info. Return stable public fields.
- **Breaking changes without a version.** Renaming a field "quickly" breaks every live client at once. Additive or versioned — no third option.
