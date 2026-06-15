---
title: Two individually-green branches can compose red on the merge ref — emergent cross-lane interaction requires a merge-ref CI pass
date: 2026-06-11
category: orchestration
tags: [ci, gating, parallel-sessions, reproducibility]
confidence: learned
source: private-work
---

An invariant can fail on the merge ref even when both sibling branches pass CI individually. The failure mode: one branch silently narrows an invariant (e.g., makes a collection entry conditional), while a sibling branch newly wires a test that enforces the old invariant. Neither branch is red alone, but the merge ref exposes the contradiction.

**The class-level fix:**

1. **Merge-ref CI is non-negotiable.** This failure class is invisible to per-branch CI by construction — the only path that observes the interaction is a CI run on the actual merge commit.

2. **Declare conditions as queryable constants.** When a collection member is conditionally included (e.g., opt-in gated by an environment flag), declare the condition as a named, queryable constant alongside the collection. Tests can then assert both branches of the condition explicitly: 0 entries without the flag, 1 with it.

3. **Wiring orphan tests into CI is itself a behavior change.** The lane that wires previously-orphaned tests into CI discovery should run those tests against ALL open sibling branches as part of its own verification step — not just against its own changes. This catches cross-lane conflicts before merge rather than at it.

**The deeper pattern:** any change that moves a test from "exists but doesn't run" to "runs in CI" is a behavior-change commit with emergent interactions. Treat it with the same cross-lane awareness as a semantic change.
