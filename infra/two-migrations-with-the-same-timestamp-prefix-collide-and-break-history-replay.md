---
title: Two migrations generated with the same timestamp prefix collide and silently break history replay
date: 2026-07-25
category: infra
tags: [migrations, determinism, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A schema-migration tool that names migration files by a timestamp prefix can produce two files with the IDENTICAL prefix when two migrations are authored in parallel, or scripted, within the same time-resolution window. Migration tooling that replays history in filename order treats this as an ordering ambiguity, and a replay-based drift or integrity test can then fail on an operation that looks completely unrelated to either of the colliding migrations — the failure surfaces downstream of the actual cause, which makes it harder to diagnose than a same-named-file conflict would be.

The fix in the moment is mechanical: rename one migration to a later timestamp so the ordering is unambiguous. The generalizable lesson is to add a preflight check — alongside whatever automated sweep already looks for other latent, time-dependent issues — that scans migration filenames for duplicate timestamp prefixes before they can land, since the collision is invisible in a normal diff (each new migration file is unique content, just sharing a name-prefix) and only manifests later, in an unrelated-looking test failure.
