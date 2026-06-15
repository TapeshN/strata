---
title: A test that depends on a sibling checkout is a defect — witness hermeticity by poisoning the path
date: 2026-06-11
category: evals
tags: [ci, reproducibility, multi-repo]
confidence: learned
source: private-work
---

Two test suites in one night were green locally and red in CI for the same reason: each discovered a *sibling repository's* files at module-load time. On the dev machine, where every repo lives under one root, discovery silently succeeds; in a single-repo CI checkout the sibling doesn't exist, discovery silently nulls, and the test asserts the wrong thing or quietly skips.

The fix shape, both times: in-repo fixtures ship with the test — a temp-dir artifact standing in for the sibling's data in one case, a small conforming fixture script standing in for the sibling's CLI in the other — plus exactly one env-flag-guarded integration test against the real sibling that skips *loudly* when the flag is absent (CI included). The fail-open property that matters when the dependency is missing stays asserted unconditionally.

The hermeticity witness: run the suite with the sibling path poisoned to a nonexistent location and watch it still pass. "Passes on my machine, where the file happens to exist" is not a witness — it's the precise condition under which this defect class hides.
