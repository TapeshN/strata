---
title: Dispatching faster than agents merge causes branch stacking; extract only the relevant files onto a clean branch to fix it
date: 2026-06-22
category: orchestration
tags: [multi-agent, dag, dispatch-sequencing, git-hygiene]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When multiple agent tasks are dispatched in rapid succession and each branches off the same base, each agent inherits any commits made by earlier agents that have already pushed. PRs show up carrying unrelated files from prior tasks, appear dirty, and require manual cleanup before they can merge cleanly.

For tasks whose output files are strictly disjoint — no shared components, no common registration files — a reliable fix is clean-file extraction:

1. After the agent finishes, identify only the files that belong to this task (known in advance from the spec).
2. In a fresh worktree branched off main, check out only those files from the agent's branch.
3. Commit and open a new PR against main. Close the stacked original.

Because the files are disjoint, the extraction is a conflict-free three-command operation. The resulting PR is clean and reviewable.

For tasks whose output touches shared files (shared components, registration tables, global configuration), the clean-extraction approach does not apply — those require a proper three-way merge resolving all concurrent changes. Prefer dispatching shared-file tasks sequentially rather than in parallel.

The deeper principle: a dispatched agent's branch should be treated as a working artifact, not a finished deliverable. The coordinator extracts the clean signal from that artifact rather than merging the artifact directly.
