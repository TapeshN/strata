---
title: Verify process identity directly before taking any action against a running process
date: 2026-06-06
category: guardrails
tags: [autonomy, hitl, lifecycle, verify-dont-trust]
confidence: learned
source: private-work
---

Inferring a process's identity from a subshell variable or a stale lock file is unreliable. A subshell reports its own process ID, not the parent session's. A lock file may hold a process ID from a session that already terminated. In both cases, acting on the inferred identity means acting on the wrong process or on a process that no longer exists.

Before taking any action against a running process (signaling, killing), enumerate the actual running processes with their identity attributes (name, parent chain, working directory) and match against them. An agent should never autonomously kill a peer session — that action is human-gated at every autonomy level.

General lesson: process identity must be verified at the moment of action, not inferred from indirect signals captured earlier.
