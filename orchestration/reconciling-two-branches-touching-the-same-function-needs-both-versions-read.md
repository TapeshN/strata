---
title: Reconciling two branches that touch the same function requires reading both full versions, not a mechanical merge
date: 2026-07-16
category: orchestration
tags: [parallel-sessions, contracts, worktree]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When two feature branches are developed in parallel and one branches off before the other lands, and both happen to modify the same underlying function, a naive "keep both changes" merge can silently produce code that is neither branch's intended behavior — each branch's edit assumed the OTHER branch's change did not exist yet. In one case, branch A had added a filtering condition to skip a certain category of items during a maintenance pass (closing a regression where those items were being incorrectly reprocessed); branch B, unaware of A's fix, had refactored that same maintenance pass and, in doing so, dropped a separate call that requeued a different category of previously-parked items. A mechanical merge of both diffs would have silently reintroduced A's regression (the filter never made it into B's refactored version) while also leaving B's requeue gap unfixed — neither branch's tests would catch this, because each branch's tests only exercised its own version of the function.

The correct reconciliation is manual and semantic: pull the FULL text of the function as it exists on each branch (a straightforward "show me this file as it exists on branch A" / "...on branch B" comparison), read both versions side by side, and hand-wire the union of intended behavior into one final version — re-adding the filter, folding the requeue call into the new structure — rather than trusting an automated merge driver to combine them correctly. A generic union-style automated merge is particularly unsafe for structured code with matching braces or blocks (such as a test file's set of grouped test blocks): it can interleave partial blocks from each side and produce code that doesn't even parse, let alone run correctly. The safer reconstruction pattern is to start from the common ancestor's clean version of the block and manually append each side's complete, self-contained addition, rather than diffing at the line level.

A secondary but easy-to-miss consequence of this kind of reconciliation in a workspace with a symlinked dependency install: after resolving conflicts in a schema-adjacent file, regenerate any code-generation artifacts derived from that schema (an ORM client, a generated types file) before trusting a type-check — a stale generated client from before the merge will pass a type-check against the OLD shape and hide a real mismatch. Treat CI running against a genuinely fresh, non-symlinked dependency install as the tie-breaking truth for whether the reconciliation actually compiles.
