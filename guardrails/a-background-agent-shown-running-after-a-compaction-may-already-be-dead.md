---
title: A background agent shown "running" after a session compaction may already be dead — the status display and the real process can silently diverge
date: 2026-07-02
category: guardrails
tags: [autonomy, subagents, lifecycle, compaction]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two long-running background agents were reported as still running after several hours. Attempting to stop them returned "no task found," and a direct process check showed no matching process at all — both had actually died hours earlier. They only continued to display as "running" because a mid-session compaction event orphaned the harness's handle to them: the harness lost the ability to detect their completion, so the last-known status simply never updated.

The general risk: a detached, fire-and-forget background agent does not reliably survive a compaction or session-resume event. When the handle is lost, the UI status becomes a stale snapshot rather than a live signal, and there is no automatic mechanism that reconciles it — a dead agent can display as running indefinitely.

The fix has two parts. Diagnostically, never trust a "running" status after any compaction or resume event without independently verifying the underlying process is alive — a status chip is not a liveness check. Architecturally, work expected to run long or unattended should route through a substrate that survives compaction by design (a remote, queryable dispatch, or a journaled/resumable workflow) rather than a local fire-and-forget background task, so completion state lives outside the fragile session handle.
