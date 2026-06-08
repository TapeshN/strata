---
title: Inline cross-repo contract assertions into builder prompts; the file cannot be read from a foreign worktree
date: 2026-06-06
category: orchestration
tags: [multi-repo, contracts, fan-out, worktree]
confidence: learned
source: private-work
---

Validation contracts for one repository's lanes cannot be read by builders working in a different repository's worktree. A builder dispatched to sub-repo A cannot open a file from the coordination layer to read the contract — the file is not in its worktree.

Fix: inline the lane's contract assertions directly into the builder and reviewer prompts for cross-repo lanes. The coordination layer reads the contract file directly; cross-repo builders receive it as part of their instructions.

Also learned: the coordination plan's assigned zone for a lane may be wrong. When the plan says a lane belongs in one repository but the contract's actual deliverables (file modifications, settings changes) land in a different repository, retarget the worktree to match the contract — the contract is authoritative, the plan is a hypothesis.

General lesson: before building, verify which repository the contract's deliverables actually modify. Dispatch the builder to that repository.
