---
title: A cloud-hosted dispatched build agent cannot amend an existing pull request — every re-dispatch opens a new one, so budget a reconcile step after each fix wave
date: 2026-07-14
category: orchestration
tags: [subagents, lifecycle, dispatch, pr-hygiene]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A cloud-hosted build agent works from its own isolated checkout and always opens its own pull request when it pushes — it structurally cannot amend or push additional commits onto an existing one, no matter how the dispatch instruction is worded. Across a batch of nine parallel build lanes plus their fix rounds, every fix-round dispatch that was instructed to "push to the same branch so the existing pull request updates" instead produced a brand-new branch and a brand-new pull request, whose starting point was the old branch (so it carried the old commits forward, plus the fix).

The root cause is structural, not a wording problem: a cloud build agent's execution environment is its own checkout, and its natural unit of output is "open a pull request from what I changed," not "modify someone else's already-open one."

The fix has two parts. Immediately: after each fix wave, confirm the lineage between the old and new branch (the new one should contain the old one's history), then close the superseded pull request with a note pointing at its replacement, so exactly one live pull request represents each build lane. At the instruction level: stop writing dispatch instructions that ask an agent to amend or push to an existing branch — that outcome isn't available to it. Instead, instruct it to branch from the correct reference and treat a fresh pull request as the expected, normal result, with reconciliation as a standing step the dispatcher budgets after every fix wave rather than a surprise to clean up afterward.
