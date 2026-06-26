---
title: Agents doing feature or fix work are subject to the same repo gates as any other contributor
date: 2026-06-16
category: guardrails
tags: [agent-dispatch, changelog-gate, spec-completeness, ci, contributor-model]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A dispatched agent that opens a pull request is a contributor. It is subject to every gate the repository enforces — changelog requirements, lint rules, test coverage thresholds, format checks — exactly as a human contributor would be. If a gate requires a changelog entry for every feature or fix commit, the agent must produce one. The gate does not relax for automated contributors.

The failure mode is a dispatch specification that omits gate requirements, leaving the agent to produce technically correct code while failing the mandatory non-code checks. The agent is compliant with the brief; the brief was incomplete.

The fix belongs in the dispatch specification, not in a post-merge patch. Any brief for work in a repository that enforces a changelog gate must include an explicit instruction: add a changelog entry under the existing appropriate subsection in the unreleased section — never a duplicate section header, never a new top-level section unless none exists.

A practical checklist item: before drafting any dispatch brief, grep the repository's CI configuration for gating scripts. Identify every automated check that will run on the pull request, and embed the requirements for each in the brief. Gates the author knows exist but does not encode in the brief become guaranteed CI failures.

The broader principle: treat every gate as an implicit contributor requirement. A spec that satisfies the code deliverable but ignores the process deliverable will reliably fail CI.
