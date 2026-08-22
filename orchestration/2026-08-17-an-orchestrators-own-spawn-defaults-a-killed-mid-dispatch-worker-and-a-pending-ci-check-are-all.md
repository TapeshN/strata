---
title: An orchestrator's own spawn defaults, a killed-mid-dispatch worker, and a pending CI check are all trust boundaries a coordinator must own explicitly
date: 2026-08-17
category: orchestration
tags: [subagents, dispatch, cost, ci]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A coordinator agent spawned an entire day's worth of builder and reviewer sub-agents without ever
passing an explicit model override, so every one of them silently inherited the coordinator's own
(expensive) model tier — discovered only when a usage dashboard showed most of a weekly budget
consumed in a single day. "Inherits from the parent when no override is passed" quietly turns an
expensive coordinator into an expensive fleet; every sub-agent spawn should pass its model tier
explicitly rather than relying on inheritance.

Separately, a background dispatch process was killed mid-flight by an unrelated timeout, but the
underlying remote job it had already submitted kept running: a receipt existed on disk recording a
live remote agent, even though the local process that submitted it was gone. Re-running the same
work without first checking for that receipt would have double-dispatched the same task under a
different identifier — a dedup guard keyed only on a local task id, not on the underlying unit of
work, does not catch this. Any interrupted dispatcher run should read its own receipts FIRST; a
receipt for a live remote job means that job is still in flight and the envelope should be left
for reconciliation, not resubmitted; and duplicate envelopes covering the same unit of work should
be treated as a double-dispatch to be merged, not a harmless retry.

Finally, a change was pushed while its continuous-integration run was still in flight, and the
platform reported the pull request as "mergeable" (no textual conflicts) while a separate field
reported the checks themselves as still pending — merging on the first signal alone would have
defeated the entire purpose of having added CI. The generalizable rule: "mergeable" answers whether
there is a textual conflict; a separate check-status field answers whether the required checks
have actually passed — read both, and treat a pending or unstable check-status as a hard blocker
that the coordinator, not the builder, is responsible for waiting out.
