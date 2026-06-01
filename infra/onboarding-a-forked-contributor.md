---
title: Onboarding a forked contributor — snapshots, tracked telemetry, and ignore-rules
date: 2026-05-31
category: infra
tags: [forks, multi-repo, onboarding, contributor]
confidence: learned
source: private-work
---

A first external collaborator forked the workspace and hit a cascade of friction: (1) their fork showed a stale README — a fork is a point-in-time snapshot and does not auto-update; (2) sync kept demanding a stash though they'd changed nothing — high-churn telemetry/state files were *tracked*, and a hook rewrote them on every action, producing phantom local changes; (3) their sub-repo clones showed as untracked and blocked the sync — clones land under their short upstream names, but the ignore-file only ignored the maintainer's personally-prefixed local names.

Fixes at source: untrack and ignore the high-churn telemetry; make the ignore-file cover *both* the short canonical names and any local prefix scheme; document the fork-sync ritual in onboarding.

General lessons: operational telemetry must be gitignored, never tracked. Layout decisions must account for *both* how the maintainer names things locally and how a contributor's clone names them. And a fork needs explicit "keep your fork up to date" guidance — it will not self-heal.
