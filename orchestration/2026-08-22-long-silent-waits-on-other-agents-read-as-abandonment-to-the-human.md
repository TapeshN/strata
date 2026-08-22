---
title: Long silent waits on other agents read as abandonment to the human — report status at every wake
date: 2026-08-22
category: orchestration
tags: [comms, coordinator]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A coordinating agent spent an extended stretch of a session cycling through wait loops for other in-flight agents, producing no visible output the whole time it waited. From the human's side, this was indistinguishable from the coordinator having stopped working entirely, and was called out directly as such.

General rule: while waiting on other agents or long-running processes, surface a brief status line at each wake — what's currently running, what just landed, what's next — rather than staying silent until there's a final result to report. If a message arrives from the human during a wait, answer it before resuming the wait rather than letting it queue behind the loop. Silence during a genuinely active multi-agent process is cheap for the agent and expensive for the human's trust that anything is happening at all.
