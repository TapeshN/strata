---
title: A single-machine process lock cannot arbitrate an invariant that spans multiple machines; only a committed, shared marker can
date: 2026-07-06
category: guardrails
tags: [split-brain, cross-machine, ownership-marker, pidfile, fail-closed]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A lock file that records a live process ID and is checked with a kernel-local liveness call correctly prevents two sessions on the *same* machine from both believing they hold exclusive ownership of a shared role. It provides no protection at all once a second machine enters the picture, because a local liveness check has no way to observe a process running on a different host — each machine can independently conclude it holds the lock, with neither aware the other exists, producing a split-brain where two owners issue conflicting writes to shared state.

The fix that actually spans machines is a marker committed into shared version control, naming the current legitimate owner by hostname, checked by every session at startup and by every write-guard before a mutation. Ownership changes only through a deliberate, auditable commit that updates the marker, never through a race between two local processes. Two failure-mode asymmetries matter here: if the shared marker is simply absent, treat that as the legacy single-machine state so a bug in the new mechanism cannot itself wedge a legitimate existing owner; but if the marker is present and unreadable or malformed, fail closed rather than treating an ambiguous signal as permission — an agent should never self-grant ownership from a marker it cannot cleanly parse.
