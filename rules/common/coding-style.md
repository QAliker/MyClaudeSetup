# Coding style

Always-on. Language-agnostic.

## Immutability by default

- Prefer values that don't change after creation. Reassign only when it's the clearest option.
- Don't mutate inputs — arguments, shared state, or collections passed in. Return new values.
- `const`/`final`/`val` over mutable bindings unless mutation is the point.

## File organization

- One clear responsibility per file. When a file grows past what you can hold in your head, it's doing too much — split it.
- Name by what it does, not what it is (`retry-with-backoff` over `utils`).
- Colocate what changes together; separate what changes for different reasons.
- No dead code left behind. Delete it — git remembers.

## Small over clever

- Boring code someone reads at 3am beats clever code they decode at 3am.
- Shortest diff that works. Deletion over addition.
- No abstraction until there are two real callers. No config for a value that never changes.
