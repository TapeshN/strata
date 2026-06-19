---
title: Parallel-built PRs touching a shared file conflict at merge; "canonical place + grep-noop" only works SEQUENTIALLY
date: 2026-06-16
category: agents
tags: [[fan-out-design], [stacked-prs], [shared-file-conflict], [parallel-not-sequential], [merge-order]]
confidence: learned
source: private-work
---

in a parallel fan-out, two phases must NOT both edit the same shared file. Either (a) give each phase DISJOINT files, or (b) assign ALL edits of a shared file (`.env.example`, a barrel/index) to exactly ONE phase the others depend on (sequential). "Grep-first, no-op if present" is a SEQUENTIAL guard — zero protection between parallel siblings. Scout shared-file ownership at plan time and make it disjoint. Also: merging an "independent" PR can silently break a stacked sibling's mergeability if they share a file — re-check stack mergeability after every merge.
