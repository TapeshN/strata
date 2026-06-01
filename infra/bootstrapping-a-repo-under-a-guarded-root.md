---
title: A guard keyed on directory presence fires before a new repo is registered
date: 2026-05-30
category: infra
tags: [worktree, guardrails, boundaries, bootstrapping]
confidence: learned
source: private-work
---

A workspace runs a guard that blocks direct edits to any primary checkout, forcing work into isolated worktrees. The guard keys on directory presence under the controlled root — so the moment a brand-new repository directory exists (with a `.git/`), edits to it are blocked, even though it has no remote and isn't registered anywhere yet. This makes the normal bootstrap (create dir, write initial files, first commit) impossible without a deliberate bypass.

This is correct behavior, not a defect — the mitigation is awareness. New-repo setup is a known, bounded exception: create + init, write all initial files, take one bypass-flagged commit, push, and from that first push onward work only in worktrees.

General lesson: a presence-keyed guard cannot distinguish "not yet bootstrapped" from "established primary checkout." Plan the bootstrap as an explicit short bypass window rather than fighting the guard or weakening it.
