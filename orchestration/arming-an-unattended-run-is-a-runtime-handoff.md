---
title: Arming an unattended run is a runtime handoff — prove the runway, not just the prompt
date: 2026-06-10
category: orchestration
tags: [autonomy, scheduling, locks, headless, park-dont-stall]
confidence: learned
source: private-work
---

A scheduled overnight session fired exactly on time, oriented correctly from disk, and then did zero work — for two stacked reasons. First, the daytime coordinator session had been context-compacted but never *exited*: its process stayed alive all night holding the single-writer coordination lock, so the overnight session's collision guard (correctly) refused to proceed against a live holder. Pausing a session is not ending it; its locks outlive its usefulness. Second, even past the lock, the overnight session's first permission-gated tool call raised an interactive prompt at 2 a.m. with no human awake to answer — a headless run dies at its first non-pre-approved tool.

The lesson is that staging the prompt is the easy half of arming an unattended run; the hard half is proving the runway. The arming ritual must (1) dispose of locks — release the coordination lock and actually end the holding session, verifying the lock is free; (2) confirm the permission envelope is satisfiable headlessly — every tool the run needs is pre-approved; and (3) give the run a park-don't-stall fail path — on any blocker, post a one-line status to the team channel and exit cleanly, never wait on input that cannot come. An armed schedule is not a working schedule until the runway is proven, the same way a registered gate is not a working gate until it has been seen to fire.
