---
name: e2e-testing
description: Use when writing, structuring, or stabilizing browser end-to-end tests (Playwright, Cypress) — choosing selectors, waiting on async UI, isolating test data, or deciding what belongs at the E2E level vs a unit test. Symptoms: flaky tests, arbitrary sleeps, brittle CSS selectors, tests that share state, slow suites.
---

# E2E Testing

## Overview

E2E tests verify real user journeys through a real browser against a real (or realistic) backend. They are the slowest, most expensive tests you own — so each one must earn its place and must not flake. A flaky E2E suite is worse than no suite: it trains people to ignore red.

Core principle: **test user-visible behavior, wait on conditions not time, isolate every test.**

For *running* and diagnosing an existing suite, use the `e2e-runner` agent. This skill is about *authoring* tests that don't flake.

## What belongs at E2E level

E2E is for critical paths that cross the whole stack: signup/login, checkout, the one flow that loses money if it breaks. Everything else drops down the pyramid.

| Question | Test type |
|---|---|
| Does this function compute right? | Unit |
| Do these modules integrate? | Integration |
| Can a user complete this journey in a browser? | E2E |

If a bug can be caught by a cheaper test, catch it there. Reserve E2E for "does the whole thing actually work for a human."

## The three rules

### 1. Select by user-facing semantics, not structure

Users see roles, labels, and text — not CSS classes or DOM position. Selectors coupled to structure break on every refactor.

```ts
// ❌ brittle — breaks when markup/styles change
await page.click('.btn-primary.mt-4 > span');
await page.locator('div:nth-child(3) input').fill('a@b.com');

// ✅ resilient — survives restructuring, mirrors how a user finds things
await page.getByRole('button', { name: 'Sign in' }).click();
await page.getByLabel('Email').fill('a@b.com');
await page.getByTestId('cart-total');   // when there's no accessible handle
```

Priority: role/label/text → `data-testid` → CSS as last resort. If you reach for a CSS/XPath selector, that's a smell — usually the element needs a label or `data-testid`.

### 2. Wait on conditions, never on time

`sleep(2000)` is the #1 cause of flake: too short and it fails under load, too long and the suite crawls. Wait for the actual condition instead.

```ts
// ❌ arbitrary — flaky and slow
await page.waitForTimeout(2000);
expect(await page.locator('.toast').isVisible()).toBe(true);

// ✅ web-first assertion — auto-retries until true or times out
await expect(page.getByRole('alert')).toHaveText('Saved');
await expect(page.getByRole('row')).toHaveCount(3);
```

Web-first assertions (`await expect(locator)...`) poll automatically. Use them instead of reading state once. Never bump a timeout to "fix" flake — find what you should have waited for.

### 3. Isolate every test

Each test must pass alone and in any order. Shared state = order-dependent flake.

- Set up the data the test needs (API/fixtures/seed), tear it down after.
- Don't depend on another test having run first.
- Use unique data per test (`user-${Date.now()}@x.com`) so parallel runs don't collide.
- Prefer creating state via API over clicking through the UI to reach a starting point — faster and doesn't retest the same path twice.

## Quick reference

| Problem | Fix |
|---|---|
| Test flakes intermittently | Replace `waitForTimeout` with web-first `await expect(...)` |
| Selector breaks on refactor | Switch to `getByRole`/`getByLabel`/`getByTestId` |
| Tests pass alone, fail together | Isolate data; remove cross-test dependencies |
| Suite too slow | Push assertions down the pyramid; seed state via API |
| Login repeated in every test | Reuse auth state (Playwright `storageState`) |

## Common mistakes

- **Forcing green.** Weakening an assertion, blanket `test.skip`, or inflating a timeout to pass CI hides real breakage. Fix the cause or report the regression. See `e2e-runner`.
- **Asserting on implementation.** Checking a CSS class or internal state instead of what the user sees. Assert on visible outcomes.
- **One giant test.** A 40-step test that does everything fails opaquely. One journey per test; name it by the journey.
- **Testing third-party UI.** Don't E2E-test Stripe's checkout or an OAuth provider's page — mock/stub the boundary, test your integration point.
