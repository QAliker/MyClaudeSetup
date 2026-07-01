---
name: database-migrations
description: Use when writing or changing a database schema migration that will run against live data — adding/dropping columns or tables, changing types, adding constraints or indexes, backfilling, or renaming. Symptoms: migration locks a busy table, deploy needs downtime, NOT NULL/unique added to a big table, rename breaks the running old code, no rollback path.
---

# Database Migrations

## Overview

A migration on an empty dev DB always "works." The risk is production: a table with millions of rows and live traffic. A careless migration takes a lock, blocks every read/write behind it, and the app is down until it finishes.

Core principle: **a migration must be safe to run while the old code is still serving traffic, and reversible if it goes wrong.**

For *reviewing* a migration or diagnosing slow/locking DB behavior, use the `database-reviewer` agent. This skill is about *authoring* migrations that don't take the app down.

## The one rule: schema change and code change are separate deploys

Old code and new schema run at the same time during any deploy. So a migration can never break the code currently running. This forces **expand → migrate → contract**:

1. **Expand** — additive only. Add the new column/table/index. Old code ignores it, new code can use it. Safe.
2. **Migrate** — deploy code that writes/reads the new shape. Backfill old rows.
3. **Contract** — only after all traffic uses the new shape, drop the old column/constraint. Separate deploy.

A "rename column" is not one step — it's add new → backfill → dual-write → switch reads → drop old. Doing it in one `ALTER` breaks the old code the instant it lands.

## Operations that lock — and the safe form

| Naive op | Why it hurts | Safe form |
|---|---|---|
| `CREATE INDEX` | locks writes for the whole build | `CREATE INDEX CONCURRENTLY` (Postgres); online DDL (MySQL 8) |
| `ADD COLUMN ... NOT NULL DEFAULT x` on old engines | full table rewrite | add nullable → backfill in batches → set `NOT NULL` |
| `ADD CONSTRAINT` / FK | validates every row under lock | add `NOT VALID` → `VALIDATE CONSTRAINT` separately (Postgres) |
| `ALTER COLUMN TYPE` | rewrites + locks | add new column → backfill → swap |
| Backfill in one `UPDATE` | one giant transaction, long lock, huge WAL | batch by id/PK, commit per batch |
| Drop column immediately | old code still selects it → errors | contract step, after code no longer references it |

## Backfill in batches

One `UPDATE table SET ...` over millions of rows holds a transaction and locks too long. Loop in bounded chunks, commit each:

```sql
-- ❌ one long transaction, locks + bloats WAL
UPDATE orders SET status = 'legacy' WHERE status IS NULL;

-- ✅ batched, each commits fast, replicas keep up
-- run until 0 rows affected (driver loop or a DO block)
UPDATE orders SET status = 'legacy'
WHERE id IN (
  SELECT id FROM orders WHERE status IS NULL LIMIT 5000
);
```

## Every migration needs a down path

If it can't be reversed, a bad deploy can't be rolled back. Write the `down`/rollback and confirm it actually reverses `up`. Irreversible by nature (a destructive `DROP`)? Say so explicitly and gate it — don't let it look reversible.

## Common mistakes

- **Schema + data in one migration.** Mixing DDL and a big backfill means one long lock and a hard-to-reverse step. Split them.
- **Testing only on empty tables.** Test against production-scale row counts, or at least reason about the row count. Lock duration scales with rows.
- **Drop in the same release that stops using the column.** The old pod is still running mid-deploy. Contract in the *next* release.
- **No timeout.** Set `lock_timeout`/`statement_timeout` so a blocked migration fails fast instead of queuing all traffic behind it.
- **Trusting the ORM's auto-migration.** ORM-generated DDL often picks the naive locking form. Read the SQL it emits before shipping.
