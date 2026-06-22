---
title: Multi-agent dispatch must check file ownership of open PRs before firing a new agent
date: 2026-06-16
category: orchestration
tags: [multi-agent, dispatch, merge-protocol, isolation, boundaries]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When multiple agents are dispatched in parallel, each branches off the same base (typically main). If two agents touch the same file, their pull requests will conflict at merge time. This collision is invisible at dispatch time — no error is raised, the agents build successfully, and the conflict surfaces only when the second PR tries to merge.

The fix belongs at dispatch time, not at merge time. Before dispatching a new agent to fix or modify a set of files, list the files already owned by open pull requests. A file owned by an open PR is a single-writer resource until that PR merges.

The dispatch decision then has two branches:
- If the new agent's files are disjoint from all open PR file sets, dispatch in parallel.
- If there is overlap, either sequence the new agent (merge the blocking PR first, then dispatch off the updated base), or flag the overlap explicitly and require a sequencing decision.

The practical check: retrieve the touched-files list for all open PRs before composing the dispatch batch. The merge-gate discipline applied at the dispatch layer is far cheaper than resolving a conflict after an agent has spent time on an incompatible base.

The adjacent trap: when a wave of agents is dispatched against the same base, and one of them lands a change to a file that a later agent in the batch was also going to touch, the later agent will conflict not because of an pre-existing open PR but because of a sibling dispatch in the same batch. Sequencing agents that touch overlapping files — even within a single batch — eliminates this class of conflict without requiring a rerun.
