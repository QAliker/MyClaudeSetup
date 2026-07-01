---
name: backend-patterns
description: Use when structuring backend/server code and unsure whether to reach for a design pattern — organizing business logic, data access, service boundaries, caching, background work, or retry/idempotency. Symptoms: about to add a repository/service/factory layer, a queue, a cache, or an abstraction "for flexibility"; logic tangled with I/O; not sure if the pattern earns its cost or is over-engineering.
---

# Backend Patterns

## Overview

Knowing the pattern is not the problem — knowing **when it earns its cost** is. Most backend code needs no pattern; a plain function that does the thing is the default. A pattern is justified only when a *concrete, present* pressure demands it. Speculative flexibility is not a pressure.

Core principle: **match the pattern to a real symptom you have now, not a future you imagine.** The wrong pattern costs more than no pattern.

For migration safety use `database-migrations`; for injection/authz use `web-security`. This skill is about *structure*.

## Symptom → pattern (and the cost)

| Real symptom you have now | Pattern | What it costs |
|---|---|---|
| Same data-access logic copied across call sites, or you want to swap the store / fake it in tests | **Repository** | one more layer; don't add it for a single caller |
| A use-case spans multiple repositories/steps and controllers are getting fat | **Service / use-case layer** | indirection; skip if the controller is 5 lines |
| Object construction is complex or varies by input | **Factory** | only past ~2 variants; one type = just `new` |
| Hard-coded dependency you can't test or swap | **Dependency injection** (pass it in) | wiring; a constructor arg, not a framework |
| Slow/expensive read, repeated, tolerates staleness | **Cache** | invalidation is the hard part — see below |
| Work is slow, external, or must survive a crash | **Queue / background job** | infra + retry + idempotency; sync is fine if fast |
| An operation may run twice (retry, double-submit) | **Idempotency key** | storage; required for money/side-effects |
| Behavior varies by type and you're writing an `if/switch` ladder that keeps growing | **Strategy / polymorphism** | more types; a 2-branch `if` is fine |

## When NOT to reach for a pattern

- **One caller, one implementation.** An interface with a single impl is indirection with no payoff. Inline it.
- **"We might need to swap X later."** You might not. Add the seam when the second impl actually exists (YAGNI). The refactor then is cheap; the abstraction now is a standing tax.
- **The pattern has more lines than the logic it wraps.** That's the pattern serving itself.
- **You can't name the concrete pressure.** "Cleaner" / "best practice" / "more flexible" are not pressures. A duplicated block, a failing test seam, a slow endpoint — those are.

## Caching has a second half

Adding a cache is easy; the cost is **invalidation and staleness**. Before caching, answer: how stale can this be, and what busts it (TTL, write-through, event)? No answer → you're caching a future bug. Reach for a built-in (`@lru_cache`, framework/HTTP cache, Redis) before a custom cache class.

## Common mistakes

- **Layered architecture for a CRUD app.** Controller → service → repository → mapper for `SELECT * FROM users WHERE id=?` is four files doing one query. Collapse it.
- **Pattern first, problem later.** Picking "hexagonal / DDD / CQRS" before the domain shows the need. Let duplication and pain point at the pattern.
- **Event/queue everything.** Async indirection makes flow hard to trace and debug at 3am. Use it where you need durability or slowness isolation, not everywhere.
- **Generic "manager"/"helper" abstractions.** Names with no domain meaning usually wrap unrelated things. Split by responsibility instead.
