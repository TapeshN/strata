---
title: Run a read-only recon before scoping a fix for any "X is not working" report
date: 2026-06-02
category: orchestration
tags: [verify-dont-trust, roles, subagents]
confidence: learned
source: private-work
---

When a user reports that something "isn't working" or "isn't live," the instinct to add or change data is often wrong. In a concrete case, a read-only multi-agent recon found the underlying system was fully wired and functioning — the real problems were a hard-to-find entry point and shared per-session state that made it feel dead, not a missing data setup.

Prevention: for any "X is broken" or "X isn't ready" report, run read-only recon agents before scoping a build or schema change. Map the actual runtime state first. The fix is frequently access, session isolation, or UI, not new data or new code.

General lesson: a "data not live" feeling often means "I can't find the entry point" or "my session is competing with others." Recon the live state before concluding the data is absent.
