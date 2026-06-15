---
title: Adversarial verification of a parallel build batch — recurring test-blindness patterns that evade per-branch CI
date: 2026-06-11
category: evals
tags: [evals, golden-sets, determinism, reproducibility, ci, gating]
confidence: learned
source: private-work
---

Running an adversarial verification pass over a batch of parallel build lanes surfaces a recurring cluster of test-blindness defects that per-lane CI does not catch. Common patterns:

**Registry / default-entity tests:** a test for a registry's default-entity lookup must assert the *exact expected default*, not just "something was returned" (`assertEqual(expected)` not `assertGreater(0)`). Using an arbitrary first entry as the default silently mis-assigns entities whenever the registry order changes. Fixtures must contain the specific entity the code defaults to, or the test exercises a path production never takes.

**Full-suite contamination from new constants:** a builder adding a new module-level path constant that participates in writes (even idempotent ones) must run the FULL test suite, not just the new file. A new constant can contaminate sibling test fixtures that do not redirect it, causing failures that only appear in the full run.

**Mock-patch on pre-bound references is a no-op:** `mock.patch` on a function that was already bound at import time (a pre-cached reference) does not intercept calls. Registries that feed dispatch must store callable names and resolve via `getattr` at call time. Aggregators that cache state across calls need explicit `setUp`/`tearDown` cache clears so fixture state does not bleed across test files.

**Environment-seam hermeticity:** an empty-string environment variable must be treated as unset (pop it, never set-to-empty in teardown). The canonical hermeticity witness is "poison the seam" — point the env var at a nonexistent path and assert honest degradation. Module-level constants read at import time do not see `os.environ` changes made after import; patch the attribute, not the env var.

**Fail-open side-effect scripts:** every side-effect write must be gated by a dry-run flag AND independently try/except-guarded when it follows a successful external action. A bookkeeping crash after a successful external call un-fails-opens the script.

**End-to-end spec coverage for superseded behavior:** specs asserting superseded behavior can hide in sibling suites outside the primary spec directory. Before calling a route or behavior change done, grep ALL spec directories for the old assertion.
