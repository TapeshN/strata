---
title: When two open PRs touch the same file, merge the foundational one first and rebase the dependent before the other's rebase finishes
date: 2026-06-22
category: orchestration
tags: [multi-agent, parallel-sessions, gating, dag]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When two open PRs both modify the same file, a coordinator instinctively merges whichever goes green first. This is the wrong ordering. Merging the first invalidates the second's rebase immediately. If the second agent's rebase is already in flight when the first merges, it resolves against a stale base — the resulting branch is dirty even if it looks clean from the outside. Recovering takes multiple additional dispatch rounds.

The correct discipline at harvest time is:

1. Before merging any PR in a wave, compare each open PR's changed-file set. Identify overlaps.
2. For a same-file pair, determine which is foundational (introduces the structure the other depends on) and merge that one first.
3. Rebase the dependent PR onto the updated main before dispatching any rebase agent — never do both rebases concurrently.
4. Cap retry attempts per lane (no more than two attempts for the same failure class). On the third failure, hold for human decision rather than spawning additional agents.

A global-token or layout change carries a long verification tail that extends well beyond its own diff. Accessibility contrast regressions propagate to every surface that inherits the token, and structural behavioral tests (navigation, mobile layout) break silently. Pre-empt the tail by scoping the verify work into the original brief.
