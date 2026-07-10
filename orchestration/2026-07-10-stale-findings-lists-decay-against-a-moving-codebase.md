---
title: A captured bug list is a hypothesis, not a work order — re-verify before fixing
date: 2026-07-10
category: orchestration
tags: [stale-data, code-review, process, re-verification, team-coordination]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A captured list of bugs, gaps, or findings goes stale the moment other work lands on top of it. If you treat that list as a work order and start fixing items straight off it, you risk re-fixing things that are already done, or worse, shipping a "fix" for a problem that no longer exists — wasting effort and potentially introducing a regression into code that had already moved on.

**What happened:** A bug-capture pass produced a list of issues to address before a client-facing release. Before acting on it, a fresh traversal of the current codebase (not the list) found that most of the captured items — formatting inconsistencies, navigation issues, a gating check, a composition step, permissions handling, an intake flow — had already been fixed by unrelated work that shipped in between. Had the team gone straight from the captured list to writing fixes, a chunk of that effort would have been wasted re-solving solved problems, and there was real risk of regressing the newer, correct behavior.

**How to apply:** Treat any captured list of findings — a bug triage doc, a code review's output, a stale ticket backlog, an audit report — as a *hypothesis about the current state*, never as ground truth to execute against. Before starting work from such a list, re-verify each item against the current state of the system (current branch tip, current deployed build, current running app) and only act on what is still actually true. This matters most whenever there's a gap in time between when a list was captured and when someone acts on it, and especially on fast-moving codebases where other people or automated agents are shipping in parallel. The rule generalizes beyond bug lists to any point-in-time artifact — audits, coverage reports, security scans — whose findings can be silently invalidated by intervening changes.
