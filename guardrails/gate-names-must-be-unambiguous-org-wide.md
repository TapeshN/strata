---
title: A check name must mean exactly one thing across all repositories
date: 2026-06-06
category: guardrails
tags: [gating, multi-repo, contracts, ci]
confidence: learned
source: private-work
---

When the same check name exists in multiple repositories with different implementations and different failure criteria, the name loses meaning. A check named for one purpose that requires a different file structure in each repository will confuse anyone running it cross-repo and will produce false-positive or false-negative results depending on which repo's definition is assumed.

Prevention: document a canonical check set that defines each check name precisely and unambiguously. Migrate per-repo checks to the contract deliberately — rename a gate only with a coordinated update to all documentation and allowlists in the same commit, because a rename mid-PR cycle breaks the allowlist and makes every PR fail.

General lesson: check names are an org-wide interface. Treat renames and semantics changes with the same care as an API change.
