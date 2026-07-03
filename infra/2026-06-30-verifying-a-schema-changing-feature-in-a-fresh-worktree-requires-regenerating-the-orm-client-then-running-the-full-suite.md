---
title: Verifying a schema-changing feature in a fresh worktree requires regenerating the ORM client against that worktree's own schema, then running the FULL suite
date: 2026-06-30
category: infra
tags: [worktree, prisma-generate, stale-primary, local-green-not-ci-green, full-suite]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A fresh worktree has no dependency install of its own, so a common shortcut is to symlink `node_modules` from another checkout to avoid a full reinstall. When the schema changed on the worktree's branch but the symlinked checkout was behind, type-checking failed on model fields that genuinely exist on the current branch — the generated ORM client baked into the symlinked dependencies was stale relative to the schema actually under test. The failures looked like a broken branch; they were really a stale generated artifact imported by the symlink.

The fix has two parts. First, symlink dependencies from a sibling checkout that is current (at or near the shared trunk), not from whichever checkout happens to be sitting around parked on an old commit — a stale symlink source reintroduces the exact drift the worktree was meant to isolate away from. Second, and more importantly, regenerate the ORM client against the worktree's OWN schema before trusting any type error — a generated client is a build artifact, not source, and it must be regenerated whenever the schema it targets changes, independent of whatever a symlinked node_modules happens to contain.

A second, unrelated trap showed up in the same pass: widening a query's field selection (or return shape) is not a local change. Existing tests elsewhere in the suite that pin an exact call signature, or that mock a return shape, can silently break the moment a shared function's selected fields or method calls change — even though the file that changed compiles fine and its own new tests pass. Both traps share one root cause: running only the new file's tests, or only `tsc` on the touched file, proves nothing about the rest of the codebase. The antidote in both cases is the same — after any schema or shared-function change, regenerate build artifacts against the current schema, then run the FULL type-check and FULL test suite in the worktree, not a scoped subset, before treating the change as verified.
