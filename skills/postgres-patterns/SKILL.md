---
name: postgres-patterns
description: Use when writing Postgres-specific SQL or schema beyond a plain query — choosing an index type, using JSONB, writing transactions, handling concurrency/locking, upserts, or fixing a slow query. Symptoms: seq scan on a big table, index not used, SELECT N+1, JSONB when a column fits, wrong isolation level, lock contention/deadlock, OFFSET pagination on deep pages, ON CONFLICT confusion, EXPLAIN unread.
---

# Postgres Patterns

## Overview

Postgres-specific choices — index type, JSONB vs columns, locking, isolation — that a generic "write SQL" instinct gets wrong. For *migration* safety (locks during DDL, backfills, expand/contract) use `database-migrations`; for *reviewing* a query or diagnosing prod use the `database-reviewer` agent. This skill is the delta: Postgres features and their traps.

Core principle: **let EXPLAIN, not intuition, tell you what's slow — then reach for the right Postgres tool.**

## Indexing

- **Read EXPLAIN (ANALYZE) before adding an index.** A seq scan on a small table is correct — the planner is often right. Optimize measured slow queries, not guesses.
- **Index the columns in your WHERE/JOIN/ORDER BY**, in the right order for composite indexes (equality columns first, then range). A composite `(a,b)` serves `WHERE a=` and `WHERE a= AND b=`, not `WHERE b=` alone.
- **Right index type:** B-tree (default, equality/range), GIN (JSONB, arrays, full-text), partial index (`WHERE active`) for a hot subset, expression index for `lower(email)`.
- **Index not used?** Type mismatch, a function on the column (`WHERE lower(x)=` needs an expression index), or the table's too small to bother. Check with EXPLAIN.

## JSONB vs columns

- **Columns by default.** Use real columns for anything you filter, join, or constrain on — you get types, constraints, and plain B-tree indexes.
- **JSONB for genuinely dynamic/sparse data** (varying attributes, external payloads). Index it with GIN if you query into it.
- **Don't use JSONB to dodge schema design.** A `data` blob holding fields you always query is a schema you refused to write — you lose typing and constraints.

## Transactions & concurrency

- **Right isolation level.** Default READ COMMITTED is fine for most; use SERIALIZABLE / `SELECT ... FOR UPDATE` when you read-then-write and a concurrent writer would corrupt the result (balances, counters, inventory).
- **Keep transactions short.** A transaction held open across a network call or user think-time holds locks and bloats. Do I/O outside the transaction.
- **Deadlocks:** acquire locks in a consistent order across code paths; keep the transaction small. Retry on deadlock (`40P01`) — they're expected under contention.

## Common mistakes

- **N+1 queries.** A query per row in a loop. Use a JOIN or `WHERE id = ANY($1)` to fetch in one round trip. (ORM lazy-loading is the usual culprit.)
- **OFFSET on deep pages.** `OFFSET 100000 LIMIT 20` scans and discards 100k rows. Use keyset/cursor pagination (`WHERE id > $last ORDER BY id LIMIT 20`).
- **Upsert done as SELECT-then-INSERT.** Race condition. Use `INSERT ... ON CONFLICT (key) DO UPDATE`.
- **`SELECT *` in app queries.** Fetches columns you don't need, breaks on schema change, defeats covering indexes. Name the columns.
- **`count(*)` on a huge table for pagination totals.** Exact count is a full scan. Use an estimate (`pg_class.reltuples`) or drop the total.
- **Storing money as float.** Rounding errors. Use `numeric`/`decimal`.

## When NOT to reach for it

- **No index until a query is measurably slow.** Every index costs write throughput and storage. (YAGNI)
- **No partitioning / read replicas** until size or load actually demands it — big operational cost for a small table.
- **No stored procedures / triggers for logic that lives fine in the app.** Hidden control flow is hard to test and debug.
