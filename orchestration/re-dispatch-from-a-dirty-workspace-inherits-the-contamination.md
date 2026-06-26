---
title: Dispatching to a cloud agent workspace that holds an open branch contaminates subsequent dispatches
date: 2026-06-23
category: orchestration
tags: [dispatch, cursor, contaminated-base, stacked-pr, fan-out, harvest-gate]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A cloud agent that retains workspace state between dispatches — branching each new task off the workspace's current HEAD rather than a clean checkout of the resolved starting reference — will contaminate subsequent dispatches when a large open branch is sitting in the workspace.

The contamination signature: a pull request's diff includes files from the open branch that the new task never touched. Planted markers, intentional bugs, or structural components from the in-flight branch appear in the new PR's diff alongside the intended changes. The new agent is working off a dirty base without being aware of it; from its perspective, those files were simply present in the project.

The harvest gate catches this: before merging any pull request, rescan the full diff for out-of-scope files and for removal of protected markers. A diff that is larger than expected, or that removes content the task had no instruction to change, is the signal.

Prevention at dispatch time: when a large or contentious pull request is open in a cloud workspace, either merge it first to establish a clean base, or explicitly reset the workspace to the target starting reference before firing the next dispatch. Do not fire parallel dispatches against a repository where a big open branch is sitting in the cloud workspace — parallel builds will each contaminate independently, and the resulting pull requests cannot be cleanly merged without rework.

The broader principle: a stateful remote execution environment is not equivalent to a clean checkout. Treat workspace state as a variable that must be verified, not assumed.
