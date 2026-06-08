---
title: A monitoring tool must measure the live quantity it claims to, not a monotonic proxy
date: 2026-06-06
category: guardrails
tags: [context-window, determinism, lifecycle]
confidence: learned
source: private-work
---

A monitoring tool that reports an always-increasing quantity (cumulative transcript bytes, total events since start) will never reset after a compaction or archival event — it will fire the alert condition permanently once the threshold is crossed. An always-on alert is the same as no alert: it produces alarm fatigue and the signal is dismissed.

In a concrete case, a context-window tracker estimated tokens from cumulative transcript bytes, which only grow. It warned continuously even when the actual in-app context indicator showed a much lower real value. Every session triggered the warning from the first message, regardless of actual window usage.

The fix: measure the live quantity (bytes since the last compaction boundary, active tokens in the current window) rather than a monotonic proxy. Fail-safe to the total if the live boundary cannot be determined, but reset after a detected compaction.

General lesson: a monitor that cannot distinguish "high now" from "ever exceeded the threshold" is providing noise, not signal.
