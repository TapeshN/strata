---
title: A health-checker must apply the same fail-closed stance as the action it guards — an unknown or unevaluated state is never "in sync"
date: 2026-06-14
category: guardrails
tags: [gating, determinism, judge, evals]
confidence: learned
source: private-work
---

A read-only health-checker (a CI gate, a sync-status reporter, a preflight script) that inspects a `passed / held / blocked` split has a subtle false-green failure mode: if the gate that generates "passed" entries could not run (e.g., a required API key is absent, a dependency is unavailable), the "passed" bucket is empty — and an empty "passed" bucket looks identical to a fully-synced state where there is simply nothing to do.

**The fix:** distinguish three hold states, not two:

1. **Ran and excluded** — the gate ran and determined the entry should not proceed (e.g., a quality gate scored it below threshold, a deduplication gate found a near-duplicate). This is a positive verdict: the gate worked. Report as clean.
2. **Ran and blocked** — the gate ran and detected a hard violation (e.g., an IP leak). This is also a positive verdict: the gate worked. Report as clean or as a known blocked entry.
3. **Could not run** — the gate was skipped because a required resource was absent (API key, network dep, corpus). This is an UNKNOWN state. Report as UNVERIFIED, never as "in sync."

**The principle:** a checker must apply the same fail-closed stance as the action it guards. If the action would refuse to proceed on an unknown gate state, the checker must surface "unknown" as a distinct, non-green status. "Nothing auto-qualified" ≠ "everything is journaled."

**Witness requirement:** verify a gate fix by running it against the real false-state that exposed the bug, not just against a unit fixture. A gate that passes a fixture but still false-greens on real state has a scope mismatch between the test and the production path.
