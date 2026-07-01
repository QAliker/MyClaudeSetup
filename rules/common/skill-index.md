# Skill index

Always-on. Skills auto-load on trigger match, but match isn't guaranteed. If
you're doing any of the below and the skill hasn't loaded, **invoke it yourself**
before writing code. The skill is the source of truth — this is just the pointer.

| When you're… | Invoke |
|---|---|
| Touching a trust boundary — input, auth, queries, uploads, secrets | `web-security` |
| Writing JS/TS with raw-HTML, `eval`, prototype access, or new deps | `javascript-typescript-security` |
| Writing unit/integration tests | `js-ts-testing` |
| Authoring end-to-end tests | `e2e-testing` |
| Changing schema against live data | `database-migrations` |
| Tuning Postgres SQL — indexing, JSONB, locking, slow queries | `postgres-patterns` |
| Designing or changing an HTTP/REST surface | `api-design` |
| Deciding whether a backend design pattern earns its cost | `backend-patterns` |
| Structuring UI state/composition | `frontend-patterns` |
| Writing a Dockerfile / image build | `docker-patterns` |
| Shipping to prod — rollout, rollback, health | `deployment-patterns` |

## Security non-negotiables

These hold even if no skill loads. At any trust boundary:

- **Never trust input.** Validate/normalize at the boundary before use.
- **Parametrize queries.** No string-built SQL, ever. No shell/HTML/`eval` from user data.
- **No secrets in code, logs, or errors.** From env/secret store at runtime.
- **Authorize every request** on the server — not just authenticate. Check the caller may touch *this* resource.

When in doubt, invoke `web-security`.
