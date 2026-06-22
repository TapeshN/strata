---
title: A gate can read green while doing nothing — witness both poles of every guard
date: 2026-06-11
category: guardrails
tags: [gating, preflight, ci]
confidence: learned
source: private-work
---

An end-to-end suite exited zero with every spec skipped: the database env var held a placeholder, each test's skip-on-missing-dependency path fired, and the run *looked* green while executing nothing. Skip-on-missing-dep is correct for genuinely optional surfaces; for the project class the dependency gates, green-by-skip masks total non-execution and is itself the defect.

The first fix introduced the opposite failure. A hard-fail guard added to catch the placeholder pattern-matched *all* local-host database URLs — and promptly mis-fired in CI, where a local-host URL is a real service container. Over-broad scoping, the same class of error the original silent skip was: a guard whose trigger doesn't precisely describe the bad state.

The rule that closes both poles: for any guard, witness both sides before trusting it. Prove it fires on the actual bad input (the literal placeholder credentials), and prove it passes on every legitimate environment — local dev, CI service containers, production-like. A skip path inside a gated project class must be loud or be an error. And when a guard over-fires, the fix is always to scope it tighter, never to bypass it.

A related failure mode: a gate that does structural-verification but implements it via a text-match — matching a name anywhere in a file, including comments and inert fields — can read green while the gate itself is absent. The tell is that a gate satisfiable by a *comment* is worse than no gate: it manufactures the feeling of enforcement while enforcing nothing. The fix is structural parsing (inspect the actual command table, not the bytes), and the witness for correctness is always the red pole: does deleting or breaking the registered item cause the check to fail? If not, the check is not checking what it claims to check.

Similarly, a gate that is *registered* but not *reachable* in a live path (an absolute path that resolves only on the dev machine, a hook wired to a primary checkout that never reaches worktrees, a callable whose CLI was never exercised end-to-end) reads as "wired" in a settings file while being inert in every real call. The two-question test: (1) is there a live caller? (2) does deleting the mechanism cause that caller to fail? Both must be yes for the gate to count.
