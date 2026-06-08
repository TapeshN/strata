---
title: Scope the destructive-action bypass to the provably-recoverable subset; keep the broad bypass human-only
date: 2026-06-06
category: guardrails
tags: [gating, autonomy, rollback, isolation]
confidence: learned
source: private-work
---

A broad destructive-action bypass token that permits any destructive operation conflates provably-recoverable operations (pruning merged, clean branches that exist on the remote) with genuinely dangerous ones (hard-resetting a dirty working tree, deleting unmerged branches). Using the broad bypass for the recoverable case normalizes bypassing the gate for the dangerous case.

The safer design: create a narrow, scoped bypass for the recoverable subset only, with a re-check of the safety conditions at removal time to close the race between planning and execution. The broad bypass remains a human-only action at every autonomy level — an agent should never set it on its own behalf.

General lesson: when a safety gate fires on an in-bounds operation, the fix is to use the narrower in-bounds equivalent of the operation, not to reach for the bypass token.
