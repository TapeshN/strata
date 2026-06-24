---
title: Read the artifact before flagging a gap — a collapsed diff view is not evidence of absence
date: 2026-06-24
category: guardrails
tags: [verify-dont-trust, docs, evals]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A reviewer flagged the same class of defect three times in one session — and retracted all three after reading the actual source file. In each case, the suspicion came from a collapsed diff view or a worker's narration of changes: the surrounding code that resolved the concern was hidden, so the reviewer fired on absence-of-visible-evidence rather than evidence-of-absence.

The two errors look like opposites but share the same root: shallow proof. "Wired does not mean working" catches the case where shallow proof confirms a bug is fixed; this pattern is the inversion — shallow proof raises a false alarm that something is missing.

**The rule:** before asserting a defect or gap, open the real file at the precise lines the claim is about and read it. State the gap only when the artifact itself shows it is absent. "I cannot see X in the collapsed diff" is not the same as "X is missing."

The review discipline cost here is low — one file read per claim — and the benefit is proportionately high: avoiding the coordination cost of a retracted flag, a blocked merge, or a re-dispatch to fix a non-existent problem.
