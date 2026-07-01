---
name: js-ts-testing
description: Use when writing or reviewing unit/integration tests in JavaScript/TypeScript — deciding what to test, whether to mock or use the real thing, testing async code, or fixing flaky/slow tests. Symptoms: about to mock everything, test asserts on implementation details, arbitrary setTimeout/sleep in a test, chasing coverage %, test passes but proves nothing, snapshot blobs, brittle tests that break on every refactor.
---

# JavaScript / TypeScript Testing

## Overview

A test suite can be green and still worthless — mocking so much it tests the mocks, asserting on internals so every refactor breaks it, or racing on timing. The gap isn't knowing how to call `expect` — it's testing the *behavior that matters* instead of the implementation. (For end-to-end browser flows use `e2e-testing`; this is unit/integration.)

Core principle: **test observable behavior through the public interface, with the fewest test doubles that still isolate what you're testing.**

## What to test (and what not)

- **Test behavior, not implementation.** Assert on the output/effect a caller sees, not which private method ran. If a refactor that preserves behavior breaks the test, the test was coupled to internals.
- **Prioritize by risk, not coverage %.** Money paths, auth, data transforms, edge cases (empty, null, boundary, error) first. 100% coverage of trivial getters proves nothing; a covered line is not a tested behavior.
- **Don't test the framework or the language.** No tests that React renders or that `Array.map` works. Test *your* logic.
- **One reason to fail per test.** A test that asserts ten things tells you little when it goes red. Arrange-Act-Assert, focused.

## Mock the boundary, not everything

Default to the **real** thing; mock only what you must:

| Mock it | Use the real thing |
|---|---|
| Network / external API (HTTP) | Pure functions, your own modules |
| Clock / randomness / UUID (make deterministic) | In-memory data structures |
| Filesystem / DB when slow or unavailable | The DB in an *integration* test (real or a container) |
| Third-party service with side effects | Anything cheap and deterministic |

Over-mocking is the top cause of tests that pass while the app is broken — you've replaced the code under test with your assumptions. If you mock the thing you're testing, you're testing the mock. Prefer a fake/in-memory implementation over a mock that asserts call order.

## Async without flakiness

- **Never `setTimeout`/`sleep(500)` to "wait" for async.** It's a race — slow CI fails, fast machine passes. Await the actual promise, or wait on a *condition* (element present, value changed), not a fixed delay.
- **`await` every async assertion.** A forgotten `await` makes a test pass regardless of the result. Use `findBy*`/`waitFor` (Testing Library) or return/await the promise.
- **Fake timers** for code that uses real delays — advance time deterministically instead of waiting.

## Common mistakes

- **Snapshot everything.** Giant auto-snapshots get blindly re-recorded on failure; they catch nothing and rot. Snapshot small, intentional output only.
- **Shared mutable state between tests.** Order-dependent tests and leakage. Reset in `beforeEach`; keep tests independent.
- **Testing through the DOM when a unit test fits.** Rendering a whole component to check a pure formatting function is slow and indirect. Test the function.
- **Asserting on CSS classes / DOM structure.** Query by role/text/label like a user; structure changes shouldn't break behavior tests.
- **Chasing a coverage number.** Writing tests to color lines green produces assertion-free tests. Cover behavior; let coverage be a byproduct.

## When NOT to add a test

- **Trivial one-liner with no logic** (a passthrough, a constant). YAGNI applies to tests too.
- **Throwaway spike** you're about to delete. Test the version you keep.
