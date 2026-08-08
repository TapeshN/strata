---
title: A client-reported bug is verified in the reporter's own role, on the reporter's own path — a parallel surface rendering correctly is not the witness
date: 2026-07-30
category: guardrails
tags: [hitl, roles]
confidence: learned
source: private-work
implementation_target: coordinator-layer
efficacy: load-bearing
---

After a fix shipped and was verified, a client continued to report the same underlying symptom. A closer audit found the verification had happened on the nearest convenient surface — an internal view of the same data, which rendered perfectly — rather than the actual path the client uses, and that the client-visible symptom was in fact three separate, stacked failures along a pipeline: an upstream feed had gone cold, several outputs sat unpublished pending a review step, and a genuine render bug remained on the client's own route. Fixing and verifying only the first-guessed layer left the other two untouched, and the client's experience never changed.

The generalizable rule: for any client- or user-reported defect, the definition of done is reproducing the fix in the reporter's own role, on the reporter's own path — not a parallel surface that happens to be easier to check. And because a single visible symptom can be produced by any of several independent points of failure along a pipeline, triage must enumerate every layer between the source and the reporter's view before deciding which one to fix; "the internal view renders fine" is explicitly not evidence that the user-facing path does too.
