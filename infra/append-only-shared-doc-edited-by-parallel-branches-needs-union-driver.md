---
title: Append-only shared docs edited by parallel branches need a union merge driver plus a normalizer
date: 2026-06-20
category: infra
tags: [parallelism, merge, ci, worktree, parallel-sessions]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Every parallel branch in a fan-out appended an entry to the same shared changelog file. Merging them serially produced the same conflict at the same location every link: git's default merge driver sees two branches that both added content inside the same region and raises a conflict. In addition, git's union resolution sometimes duplicates section headings — two branches each adding a subsection of the same name produce two identical headings, which a downstream format gate then rejects.

Both problems are solved by making the tool match the access pattern:

- **Union merge driver**: declaring `CHANGELOG.md merge=union` in `.gitattributes` tells git to accept all additions from both sides without raising a conflict, and this works transparently on the remote as well. The driver is built in; no external tool is required.
- **Normalizer**: a gate script that collapses duplicate section headings into one (keeping all their entries) prevents the accumulation that a naive union allows. The normalizer runs as part of the CI format check so it cannot be skipped.

The general rule: any append-only shared document that multiple parallel branches legitimately edit requires a union merge driver so additions compose rather than conflict, plus a normalizer to collapse any structural duplication the union creates. Hand-resolving these conflicts does not scale — by the time a fan-out reaches ten branches, the merge coordinator pays a linear tax on work that should be zero-cost.

Scope the union driver to files that are genuinely append-shaped. Code files where ordering and interleaving matter should not use union merge; it resolves the conflict by including all content without regard for semantic correctness.
