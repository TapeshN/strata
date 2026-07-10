---
title: Hung-vs-Working: Liveness Checks Miss Stalled Processes and Orphaned Resource Drains
date: 2026-07-07
category: infra
tags: [incident-triage, orphaned-process, liveness-vs-progress, process-monitoring, cpu-accounting]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When a long-running system "keeps freezing," don't stop investigating once you confirm the suspect process is alive — liveness (a PID responding, a lock file held) is not the same as the process doing useful work. A hung process can sit at near-zero CPU indefinitely while still holding a lock or resource that blocks everything downstream, and the actual resource drain causing the freeze can be a completely separate, orphaned process you haven't looked at yet.

What happened: an orchestration session that coordinated work kept freezing. The obvious suspect — the coordinating process — was alive and correctly holding its lock, so a naive check ("is it running?") said everything was fine. But inspecting accrued CPU time (not just liveness) showed it had done almost no work in the last 25 minutes — it was hung, not busy. Meanwhile the real drain was a separate development server, orphaned to the OS's root process after its parent session ended, that had been running unnoticed for over 30 hours, continuously eating CPU via file-watching and recompilation.

How to apply: when triaging a "frozen" long-running system, check accrued CPU/work time for the suspect process, not just process-alive status — a stalled process looks identical to a busy one under a simple liveness check. Separately, sweep for orphaned child processes (reparented to PID 1 / the OS init) that may be the actual resource drain, independent of whatever you're debugging. Build both checks into your standard incident-triage runbook so you don't have to rediscover this distinction under pressure next time.
