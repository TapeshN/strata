---
title: Two green branches can compose a red merge ref when one adds an opt-in behavior and the other newly enforces an invariant over that collection
date: 2026-06-11
category: evals
tags: [ci, determinism, gating, reproducibility]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two branches each pass CI independently. On the merge ref, CI fails. The failure is not a conflict — the branches merge cleanly — but an emergent interaction: one branch narrowed a behavioral invariant (adding a conditional member to a collection with opt-in semantics, so the new member seeds zero times by default) while the other branch newly enforced that invariant in CI discovery (moving orphan tests into the test-runner's scope so they now execute and assert).

Neither change is wrong in isolation. Together they compose a failing state that per-branch CI is structurally incapable of detecting, because per-branch CI never sees the intersection.

The generalizable prevention:

1. Running CI on the actual merge ref is non-negotiable for this class. A green per-branch run is necessary but not sufficient.
2. When adding a conditional member to a collection that an invariant iterates, declare the condition as a queryable constant alongside the collection. The invariant can then assert the correct count for both the conditional and the unconditional cases.
3. When a lane wires orphan tests into CI discovery, that wiring is itself a behavior change. The wiring branch should run the newly discovered orphan tests against all open sibling branches in its own verify step — making the emergent interaction visible before either branch merges.
