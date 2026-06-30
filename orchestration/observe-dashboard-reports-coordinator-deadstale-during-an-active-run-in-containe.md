---
title: observe dashboard reports coordinator "dead/stale" during an ACTIVE run (in-container blind spot)
date: 2026-06-23
category: orchestration
tags: [observe, dashboard, heartbeat, in-container]
confidence: learned
source: private-work
---

liveness must key off a signal the coordinator actually emits, never a host-only PID check that's blind in-container.
