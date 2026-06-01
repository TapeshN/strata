---
title: Config an agent's hooks depend on must be set at process launch, not after
date: 2026-05-31
category: guardrails
tags: [gating, process-env, ip-boundary, lifecycle]
confidence: learned
source: private-work
---

A boundary gate depends on an environment variable pointing at its term list. That variable was exported in the interactive shell's profile, so the shell — and per-call tool subshells that source the profile — had it. But the agent process itself was launched without it, so the *hook* (a child of the agent process) saw it unset for the entire session. Environment set *after* a process starts does not propagate into that already-running process's children.

General lesson: any gate or hook that reads configuration from the environment must have that configuration present in the launching process's env *at start*, not merely in an interactive profile. Provisioning — and any headless or VM launch — must export gate config at process start. Treat a startup report of "config missing" as a hard constraint until relaunched, and design the gate to fall back safely rather than fail open.
