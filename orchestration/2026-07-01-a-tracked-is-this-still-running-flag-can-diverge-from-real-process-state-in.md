---
title: A tracked "is this still running" flag can diverge from real process state in either direction, not just one
date: 2026-07-01
category: orchestration
tags: [lifecycle, subagents, process-tracking, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A session-tracking layer reported a long-running agent session as no longer active. A direct check of real operating-system processes found a genuine, still-alive process — matching the session by its working directory and an identifying path baked into its own command line — that had been running for hours, unaccounted for by the tracking layer. This is the mirror image of an already-recognized failure mode (a tracked session reported as "still running" when the underlying process had actually already died); here the divergence ran the opposite direction — tracked state said stopped while the real process was very much alive.

The process itself was mostly idle (near-zero CPU, only idle helper processes as children), so the practical cost was a resource leak (memory, open file handles) rather than runaway computation — but it was still genuinely invisible to the tracking system that was supposed to account for it.

The general lesson: a lifecycle-tracking flag can desync from ground truth in both directions, not only the direction that has already been documented. When investigating any "is this actually still running" question, cross-check real operating-system process state (process list filtered by elapsed time, matched against working directory or an identifying path in its command line) against whatever tracking layer claims to know the answer — never trust the tracked flag alone in either direction. Checking a suspicious process's children before assuming the worst distinguishes a harmless idle leak from something actively consuming resources, and any process that isn't clearly identified as the observer's own should be reported rather than unilaterally terminated.
