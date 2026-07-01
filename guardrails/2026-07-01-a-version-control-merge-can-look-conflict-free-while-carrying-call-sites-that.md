---
title: A version-control merge can look conflict-free while carrying call sites that are semantically stale against a changed contract
date: 2026-07-01
category: guardrails
tags: [git-merge, determinism, contracts, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Reconciling a long-stale branch against a base where a function's signature had since changed elsewhere produced real, visible conflicts in the files that both branches had touched — those were resolved normally. But several sibling files that also called the now-changed function, yet that the incoming base branch had never itself edited, merged with zero conflict markers at all, because merge conflict detection is purely textual and positional: if a file wasn't touched on both sides, it merges cleanly regardless of whether its content is still semantically correct against a contract that changed somewhere else in the same merge. Every call site in those quiet files was now wrong against the new function signature, and nothing in the merge output looked unresolved.

Only running the type checker immediately surfaced the problem, file by file, with exact locations — a plain review of the diff or the merge status would not have, since nothing there appeared incomplete.

The general lesson: when reconciling any stale branch against a base where a function signature, a renamed field, or a narrowed type changed, "no conflict markers" must never be read as "no work needed." The safe procedure is to search the entire codebase for every call site of anything that changed — not only the files version control flagged — and run the type checker (or the closest equivalent static check available in a given stack) before running the test suite, since a merge algorithm is structurally blind to contract drift that a type checker will catch immediately. The riskier the reconciliation (multiple already-merged branches each touching related contracts, a long staleness window), the more of this class of silent breakage accumulates.
