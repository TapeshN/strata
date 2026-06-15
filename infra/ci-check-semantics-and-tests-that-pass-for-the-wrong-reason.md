---
title: CI-check semantics, tests that pass for the wrong reason, and cache-the-data-not-the-error
date: 2026-06-11
category: infra
tags: [ci, testing, cache]
confidence: learned
source: private-work
---

A batch of mechanics from a six-lane build fan-out, each generalizable:

- **PENDING takes precedence over FAILED when reading a CI check set.** A still-running check can clear an earlier failure on re-run; a merge gate that red-stops on any FAILED while siblings are PENDING acts on unsettled state. Only a *settled* check set (nothing pending) is a verdict.
- **Two error paths sharing an exit code let a test pass for the wrong reason.** A CLI argument-parsing change (newer language runtime made subcommands non-optional, so positionals got eaten) produced the *expected* failure exit — from the *wrong* failure. Adversarial verification must distinguish "correct path taken" from "coincidentally same observable"; assert on the error message or behavior, not just the code.
- **Cache the data, retry the error.** A dashboard aggregating multiple sources must never cache an error result inside its TTL window — otherwise one transient failure pins an "unavailable" chip for the full TTL. The test that locks this in: fail the source once, then assert the *second* call hits the source again.
- **Monkeypatching binds to the defining/calling namespace.** A refactor that moves call sites into a new module silently breaks every existing patch-based test (they patch a name nobody calls anymore). Either keep the authoritative module stable or migrate the patches in the same change.
