---
title: A drifted shared checkout is not uniformly unsafe to commit from — divergence is per-file, and can be bucketed
date: 2026-07-01
category: infra
tags: [git, worktree, drift, contracts]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When a coordinating checkout is found to be behind its remote while also holding a mix of genuinely new deliverables, pre-existing unrelated dirty files, and content belonging to an entirely separate repository nested inside the same directory tree, the instinct to treat "the checkout is drifted" as uniformly unsafe — and defer everything until a full reconcile — throws away real, immediately-landable work along with the risky part.

The better framing: fetch the remote and diff it against the local checkout on a per-file basis. Files the remote never touched merge cleanly regardless of how far behind the checkout is overall; genuinely new files are additive-safe; only files the remote actually modified need careful three-way merging. This turns one large "is it safe" question into several small, independently-answerable ones.

The safe procedure: create an isolated working copy from the remote's current state, copy in only the files verified as non-divergent or additive using explicit file paths (never a blanket "stage everything," which risks pulling in unrelated nested-repository content or files never meant to move), commit and land that subset, and leave the genuinely divergent files for a deliberate, separate reconciliation rather than guessing at a three-way merge under time pressure. The general principle: don't defer an entire drifted working set as "too risky" — bucket it by actual divergence and land the safe majority immediately.
