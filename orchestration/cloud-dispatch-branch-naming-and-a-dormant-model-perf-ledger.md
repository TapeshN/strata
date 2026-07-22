---
title: A cloud coding-agent dispatch may push to its own branch name, not the one requested — and a performance ledger with the right schema but no producer is still decoration
date: 2026-07-18
category: orchestration
tags: [subagents, contracts, determinism, roles]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

**A cloud-hosted background coding agent can push to a branch name IT chooses, ignoring the branch name a dispatch request specified.** Polling for the requested branch (a direct fetch of that specific ref) then false-negatives — the branch never appears, because the agent actually pushed to its own auto-generated branch name and opened its pull request as a DRAFT. A downstream step that assumes "the spec branch exists, and any open PR against it is ready to merge" will incorrectly conclude the dispatch failed, or will try to merge a still-draft PR and get refused. The durable fix: poll for a dispatched agent's output by listing open pull requests against the target repository and matching on the agent's own branch-naming convention, rather than assuming the requested branch name landed — and explicitly mark a PR ready for review before attempting to merge it, rather than assuming "PR exists" implies "PR is mergeable."

**A tracking ledger with a correct, well-designed schema is still worthless if nothing writes to it and nothing reads from it.** A ledger meant to record which model handled which task shape, and how that attempt turned out (review verdict, whether CI passed, cost, latency) already existed with a schema capable of supporting real model-routing decisions — but had gone dormant: a handful of stale rows from an earlier session, and nothing in the live dispatch-and-review loop feeding it new rows or reading from it to inform routing choices. As a result, model routing decisions were being made heuristically, off a single remembered incident, rather than off any aggregated evidence — despite the infrastructure for evidence-based routing already existing on disk. The general lesson: a data structure with the right shape is not a flywheel until BOTH halves are wired — something in the live loop must write a row on every relevant event, and something must actually read the aggregated data to make a decision — the same failure class as a safety gate that exists but was never actually invoked. Auditing whether a "learning loop" artifact is real should mean checking both the producer and the consumer sides are live, not just that the schema looks sensible.
