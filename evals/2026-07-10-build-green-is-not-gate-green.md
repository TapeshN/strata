---
title: Build passing and CI gate passing are different claims — run the exact test command
date: 2026-07-10
category: evals
tags: [ci-verification, test-gates, architecture-migration, accessibility, verify-dont-claim]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**The rule:** treat "the build passed" and "the CI gate passed" as different claims. If your CI job runs a specific test command (say, a `vitest`/`jest` suite invoked via a `test` script), then "typecheck clean" or "the production build compiles" is not a substitute proof — it exercises a different, narrower subset of the codebase. Always run the *exact* command CI runs before claiming green.

**What happened:** An engineer shipped a UI refactor claiming "typecheck + production build green," but the production build doesn't execute the test suite at all. When the change was pushed, CI's actual test job surfaced three failures that a single local run of the real test command would have caught. Digging into the three: two were tests that had encoded assumptions from the *old* architecture (e.g., asserting each page individually rendered a navigation component that the refactor had since centralized into a shared shell) — those needed to be rewritten to assert the new invariant, not deleted, because the property they guarded (no page can silently diverge from the shared nav) still mattered. The third was a genuine regression: ported UI markup used sub-11px text, tripping an accessibility floor the existing test suite enforced — the porting had silently imported a source design's accessibility violations into a codebase with stricter standards.

**How to apply:** (1) Before claiming a change is verified, run the literal command your CI pipeline invokes — not a proxy step that happens to compile or typecheck. (2) When you make an architectural change, expect it to break tests that encoded the *prior* architecture; budget time to update those tests to assert the *new* invariant as part of the same change, rather than treating red tests as noise to silence. (3) For every red test surfaced this way, ask "is this obsolete, or did I actually regress the thing it guards?" — the answer can differ test by test in the same batch. (4) When porting a reference design or pattern from elsewhere, audit it against your own project's floors (accessibility, security, etc.) — an external source's aesthetic choices are not exempt from your destination's standards.
