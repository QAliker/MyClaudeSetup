---
name: frontend-patterns
description: Use when structuring frontend/UI component code and unsure whether a design pattern is warranted — composing components, sharing logic, choosing state location, data fetching, or optimizing renders. Symptoms: about to add global state, a context, a custom hook, a render-prop/HOC, or a memo "for performance"; prop-drilling pain; duplicated component logic; not sure if the abstraction earns its cost or is premature.
---

# Frontend Patterns

## Overview

The failure mode in UI code is not ignorance of patterns — it's reaching for the heavy one (global store, context, abstraction layer) before the lightweight one (props, local state, composition) has actually failed. Start at the smallest scope; widen only when a concrete pressure forces it.

Core principle: **state and abstraction live at the smallest scope that works. Lift or generalize only when a real symptom demands it.** (Framework-agnostic; React named for concreteness.)

For raw-HTML/XSS sinks and client-side secrets use `web-security` + `javascript-typescript-security`. This skill is about *structure*.

## Symptom → pattern (and the cost)

| Real symptom you have now | Pattern | What it costs |
|---|---|---|
| Passing the same prop through 3+ layers that don't use it | **Context / provider** | re-renders all consumers; overkill for one hop |
| Same stateful logic (fetch, form, subscription) in 2+ components | **Custom hook / composable** | one more unit; don't extract on first use |
| Component does layout *and* data *and* logic, hard to test/reuse | **Container / presentational split** | two files; skip for a trivial component |
| A component takes many boolean/config props to vary its shape | **Composition (slots/children)** over config props | rethink API; pays off as variants grow |
| State needed by many distant components, or complex transitions | **State manager / reducer** | boilerplate + indirection; local state first |
| Sync UI with an external/non-React system (timer, socket, DOM lib) | **Effect at the boundary** (`useEffect` etc.) | easy to overuse — see below |
| List/tree with variable item types | **Component polymorphism** (map type→component) | a registry; a 2-branch ternary is fine |

## When NOT to reach for a pattern

- **Prop-drilling one or two levels.** Just pass the prop. Context for a single hop trades a clear data path for a hidden one.
- **Global state for server data.** A fetched-and-cached query (React Query / SWR / loader) is not "app state." Don't dump API responses in Redux/Zustand.
- **Extracting a hook/component used once.** Wait for the second real use; premature extraction guesses the wrong API. (YAGNI)
- **You can't name the pressure.** "Reusable" / "clean" / "scalable" aren't pressures. Duplication you've hit twice, a prop threaded through five layers, a measured slow render — those are.

## Two frontend traps

- **Premature memo.** `memo`/`useMemo`/`useCallback` everywhere adds deps-array bugs and noise for no measured win. Add it after the profiler shows a real re-render cost, not before. Fixing a bad key or an inline object often beats memoizing.
- **`useEffect` as a catch-all.** Deriving state you could compute during render, or syncing props into state, creates extra renders and stale bugs. Effects are for *external* systems. Compute in render; lift state up instead of mirroring it.

## Common mistakes

- **Reaching for Redux/global store on day one.** Local state + a data-fetching lib covers most apps. Add a store when cross-cutting client state actually appears.
- **HOC/render-prop where a hook fits.** Modern shared logic is a hook. Reserve wrappers for cross-cutting render concerns.
- **Prop explosion.** 12 boolean props to configure one component = it should be several components or use composition.
- **Abstracting components that only look alike.** Two components with similar markup but different reasons to change should stay separate. Duplication is cheaper than the wrong abstraction.
