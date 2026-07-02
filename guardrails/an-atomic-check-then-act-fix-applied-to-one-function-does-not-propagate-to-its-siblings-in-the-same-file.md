---
title: An atomic check-then-act fix applied to one function does not propagate to its siblings in the same file
date: 2026-07-02
category: guardrails
tags: [determinism, contracts, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An independent security review of a claim/lease-style buffer found that one function used a classic "read, then decide, then write" pattern — a race condition letting two concurrent callers both believe they'd won the same claim — even though a sibling function in the very same file had correctly used an atomic conditional-update pattern for an equivalent state transition.

The root cause was applying the safe pattern to one function and pattern-matching the others as "probably fine" without independently re-checking each one. A check-then-act race is scoped per function, not per file — getting it right once does not make it right everywhere nearby.

The fix: rewrite the unsafe transition as a single atomic conditional update guarded by the exact precondition (not a separate read followed by a separate write), and verify with tests that specifically simulate concurrent callers. The generalizable rule: whenever a file contains multiple state-transition writes, audit each one for atomicity independently — never assume a sibling's correctness transfers just because it's the same file or the same author.
