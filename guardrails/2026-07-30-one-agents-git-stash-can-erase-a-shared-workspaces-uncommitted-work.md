---
title: One agent's index-mutating git command in a shared workspace can silently erase every other agent's uncommitted work
date: 2026-07-30
category: guardrails
tags: [subagents, parallel-sessions]
confidence: learned
source: private-work
implementation_target: agent-guardrails
efficacy: load-bearing
---

Several agents worked in parallel inside one shared workspace on disjoint sets of files. One agent, trying to determine whether a test failure was pre-existing, ran a command that stashes all uncommitted changes — which by definition reverts every uncommitted change in that shared workspace, including the other agents' in-flight, uncommitted work. It happened to survive this time (the agent reported the risk candidly and nothing was actually lost), but nothing in its instructions had forbidden the command, and nothing would have detected a silent loss if one had occurred.

The gap: instructions for a shared-workspace fan-out commonly forbid the publishing verbs (commit, push) but say nothing about the verbs that mutate the index or working tree in place (stash, checkout, restore, reset, clean) — which are far more dangerous in a shared space precisely because they're invisible: no commit, no remote trace, just another agent's edits silently gone. The fix: any brief that shares one workspace across multiple agents must forbid every git verb that touches the index or working tree, not merely the publishing ones — and must supply a safe alternative for whatever question the agent was actually trying to answer (checking a file's pristine state without disturbing the workspace, or simply reporting an observation and letting a human or coordinator adjudicate it). Prefer one isolated workspace per agent whenever the work might overlap; accept a shared workspace only for provably disjoint file sets, and then police the git surface explicitly rather than assuming good behavior.
