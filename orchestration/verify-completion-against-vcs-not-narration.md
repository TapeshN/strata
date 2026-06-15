---
title: A status report written to disk is still narration — verify completion against the VCS
date: 2026-06-11
category: orchestration
tags: [autonomy, gating, proofs]
confidence: learned
source: private-work
---

An unattended overnight run's own morning report asserted total failure — zero deliverables, agents stalled. Version-control ground truth showed seven green pull requests created during the window, each with a companion verification branch. Acting on the report, the coordinator's first recommendation was to re-run the whole wave; the operator caught it.

A status report persisted to disk feels authoritative because it survived the session, but it stales exactly like conversation memory. Re-orientation after any gap must come from the source of record — open PRs, branch state, merge history — never from narration, even narration the system wrote about itself. Fix at the producer too: a report generator must query for the deliverables' existence before it is allowed to write a "nothing shipped" verdict.

Two adjacent lessons from the same episode. First, a blanket "finish the work" directive authorizes the in-scope merges, not the standing hard floors (publishing, schema migrations, version bumps stay gated) — floors are re-checked per action, and each merge gets an independent adversarial re-verification before it lands. Second, an open PR branch can be updated without force-pushing: branch from the PR's tip, merge the mainline there, resolve, and push the result back to the PR branch — the remote sees a fast-forward, CI re-runs, and no history is rewritten.
