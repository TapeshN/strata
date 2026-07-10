---
title: Mutation testing must mutate the file the runtime actually resolves
date: 2026-07-10
category: evals
tags: [mutation-testing, module-resolution, monorepo, false-green, test-verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

If your mutation-testing (or fault-injection) harness makes an edit to validate that a test suite would actually catch a regression, that edit must land on the exact file the runtime resolves at import time — not on a scratch copy sitting in a different directory. Anything less proves nothing, and worse, it reports as a passing gate.

**What happened:** In a workspace-style monorepo (npm/pnpm/yarn workspaces), a shared package is typically consumed through a symlink inside `node_modules` that points back at the real source directory. A verification pass tried to prove a safety check would be missed if removed, by deleting the check from a scratch copy of the shared module and re-running the test suite. The suite came back green — which looked like good news, or alternatively looked like proof the gate was broken. In fact neither was true: the test runner's module resolution followed the `node_modules` symlink straight to the original, un-mutated source file. The scratch copy was never loaded, so the test exercised the untouched code the whole time. The green result was a false signal that happened to look plausible in both directions, which is what made it dangerous — it took a second pass to notice the mutation and the resolved module lived in different files.

**How to apply:** Before trusting any mutation-testing or "did the test actually catch this" result, confirm the file you edited is the same file path the runtime's module resolver loads — trace the resolution (follow symlinks, check package aliases, check bundler path mapping) rather than assuming a sensible-looking directory is the live one. The safest pattern is to mutate the file in place inside the real workspace, run the suite, observe the failure, then revert — never mutate a copy elsewhere and infer results by analogy. This is a specific case of a broader principle: any verification witness (test, mutation, fixture) must share the exact runtime path — the same module resolution, same production code path — as what it claims to validate, or its "pass" and "fail" are both meaningless.
