---
title: Directory rename migrations must sweep prompt and skill files, not just documentation
date: 2026-06-01
category: infra
tags: [multi-repo, docs, worktree]
confidence: learned
source: private-work
---

A directory rename migration must sweep not only documentation files but also prompt and skill files that hardcode the old directory name. Documentation sweeps catch prose references; configuration and prompt files are a distinct surface. After a rename, skill files that reference the old path will silently fail at runtime, not at write time — there is no type-check or build error, just a runtime stop.

This extends an earlier lesson (rename migrations must also sweep config and hook files) to a third surface. The full sweep after any rename now includes: documentation, config files, hook allow-sets, and prompt/skill files.

General lesson: prefer discovering a checkout path at runtime (glob for it, read from a config) over hardcoding its directory name in a skill file. A hardcoded path is a hidden dependency on directory structure that breaks silently.
