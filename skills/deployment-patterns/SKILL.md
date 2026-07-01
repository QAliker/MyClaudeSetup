---
name: deployment-patterns
description: Use when shipping code to production or designing a release/rollout — deploy strategy, health checks, rollback, config/secrets, migrations during deploy, or handling in-flight requests. Symptoms: deploy needs downtime, no rollback path, secret in the repo/image, migration coupled to code deploy, no healthcheck/readiness, config hard-coded per env, all instances updated at once, no way to disable a feature without redeploy.
---

# Deployment Patterns

## Overview

Most outages happen at deploy time, not at rest. The gap isn't knowing what CI/CD is — it's shipping without the safety nets: no rollback, no health gate, a schema change welded to the code deploy, a secret in the image. Each is cheap to add before the deploy and catastrophic to lack during a bad one.

Core principle: **every deploy must be rollback-able, gated by a health check, and safe to run while the old version is still live.**

For the schema side (expand→migrate→contract) use `database-migrations`; for the image side use `docker-patterns`. This skill is the *rollout*.

## The checklist

**Rollback path first.** Before deploying, know how to undo it — redeploy the previous image/tag, or flip traffic back. Immutable, versioned artifacts (a tagged image, not "rebuild from main") make rollback instant. A deploy with no tested rollback is a one-way door.

**Health / readiness gate.** The orchestrator must not send traffic until the new instance is actually ready (DB connected, warm). Expose a readiness endpoint; roll instance-by-instance and stop the rollout if health fails — don't replace all at once.

**Gradual rollout.** Rolling / blue-green / canary so a bad version hits some traffic, not all. Canary a small % first, watch error rate, then proceed or abort. Big-bang deploys turn a bug into a full outage.

**Migrations decoupled from code.** Schema change and code change are *separate, ordered* deploys (expand→migrate→contract, see `database-migrations`). The new code must run against the old schema and vice versa during the overlap. Never gate the app boot on a migration finishing.

**Drain in-flight requests.** On shutdown: stop accepting new connections, finish the ones in progress, then exit (handle `SIGTERM`, honor a grace period). Killing instances mid-request drops user work.

**Config & secrets per environment, injected at runtime.** No env-specific values or secrets in the code or image (`docker-patterns`). Inject via env/secret manager. Same artifact promotes dev→staging→prod; only config differs.

**Feature flags for risky changes.** A flag lets you ship code dark and enable it without a redeploy — and disable it instantly if it misbehaves. Decouples *deploy* from *release*.

**Observability before you need it.** Logs, error tracking, and a key metric (error rate, latency) visible at deploy time. You can't tell a canary is failing if nothing's watching.

## Common mistakes

- **No rollback plan.** "We'll fix forward" during an outage means writing code under maximum pressure. Roll back, then fix calmly.
- **Migration in the same step as code.** The deploy half-applies, old pods hit new schema (or vice versa) and error. Separate and order them.
- **Replacing all instances at once.** A startup bug takes the whole service down with no healthy instances left. Roll gradually.
- **Rebuilding the artifact per environment.** "Works in staging, breaks in prod" because they're different builds. Build once, promote the same artifact.
- **Secrets in CI config or image.** Leaked and hard to rotate. Use the platform's secret store.
- **No graceful shutdown.** Every deploy drops in-flight requests and users see errors. Handle `SIGTERM`.

## When NOT to over-engineer

- **No canary/blue-green for a low-traffic internal tool** — a rolling deploy with a healthcheck is plenty. (YAGNI)
- **No Kubernetes for one small service** — a managed platform (or a single host + reverse proxy) may be all it needs. Match infra to load.
- **No feature-flag system for a solo project** — an env var toggle is a fine flag until a real platform earns its cost.
