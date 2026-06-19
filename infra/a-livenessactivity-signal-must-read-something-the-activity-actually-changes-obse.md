---
title: A liveness/activity signal must read something the activity actually changes (observe factory_state UNKNOWN during a live grind)
date: 2026-06-16
category: infra
tags: [observe-dashboard, liveness-signal, heartbeat, container-vs-host, signal-wiring, wired-not-working]
confidence: learned
source: private-work
---

when wiring an "is X active?" signal, verify the source actually mutates during X — a heartbeat must beat. Prefer a per-turn-written artifact (or an explicit touch) over incidental ledgers; container liveness can't use host PIDs — use a mount-visible freshness file. The same dashboard's worktree tile lied 0-in-container for the same class of reason (host CLI vs mount).
