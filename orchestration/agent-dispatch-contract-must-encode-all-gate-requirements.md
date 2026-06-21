---
title: The dispatch contract must encode every gate requirement; agents cannot infer what the prompt omits
date: 2026-06-20
category: orchestration
tags: [parallel-sessions, contracts, ci, gating, subagents]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A fan-out of background agents produced near-uniform CI failures across lanes that had nothing in common at the code level. Audit identified four distinct root causes, each traceable to a missing or ambiguous item in the dispatch prompt:

**Gate requirements not stated.** A mandatory changelog gate blocked every code change that lacked a corresponding entry in the shared changelog file. The dispatch prompt used the phrase "update the changelog if convention requires" — too soft to be actionable. Agents interpreted it differently or ignored it. A requirement that a CI gate enforces must appear as a hard imperative in the dispatch contract, not as a soft suggestion.

**Spec files referenced but not committed.** Prompts pointed agents at spec documents by filename. Those files existed as uncommitted work on the local primary. Agents working in branches cut from the remote reference never saw them. A dispatch prompt must cite only committed, addressable paths, or instruct agents to fall back to the live specification source.

**Working directory assumed but not verified.** A guard tool resolved the current branch from the process working directory. When agents ran a commit command using a flag that redirected git to a different path, the guard saw the primary's branch rather than the worktree's branch and blocked the commit as a protected-branch violation. The lesson is not to avoid the tool — it is to run all git operations from within the worktree's working directory rather than redirecting via path flags.

**Branch filters excluded parallel branches from CI.** Workflow triggers scoped to a specific target branch caused every pull request that targeted an intermediate branch (rather than the main branch) to produce zero CI results. A passing status with no checks is not evidence of correctness; a workflow filter that silently drops entire categories of pull requests is a structural gap that must be caught at contract design time.

The generalizing principle: agents cannot infer unstated requirements. Every constraint that a gate, hook, or CI job enforces must appear explicitly in the dispatch contract. When a new gate is added to the environment, the dispatch template that reaches agents must be updated in the same change.
