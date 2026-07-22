---
title: A safety/merge gate that infers its target repo or branch from ambient local state misfires when invoked from a different working context
date: 2026-07-19
category: guardrails
tags: [gating, ci-cd, tooling, git]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two separate internal safety gates showed the same failure shape: one inferred which repository a merge command targeted from the session's own current working directory rather than an explicit flag, so a legitimately-granted merge got refused as "no grant recorded" simply because it was invoked from a different local directory than usual. Another gate's allowlist for a labeled release-branch naming convention checked the invoking session's LOCAL branch name rather than the actual pull request's head branch — so merging the exact same, correctly-named PR failed the check when run from a different local branch, even though the PR itself was fully compliant.

**The rule:** a safety gate that determines "is this the allowed case" should key off the EXPLICIT target (an argument, the PR's own head ref) rather than ambient state of the environment it happens to be invoked from. When using such a gate, always pass the explicit identifier rather than relying on it to infer correctly from wherever you happen to be running.

A related trap in the same family: a safety hook kills the WHOLE chained command the instant it matches, so if a guarded step and a preparatory step (like adding a required label) are combined into one call, the preparatory step never actually runs even though the call appeared to execute. Sequence a gated action and anything it depends on as separate calls.
