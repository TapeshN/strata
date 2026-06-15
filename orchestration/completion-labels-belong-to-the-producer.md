---
title: Board state is the producer's output — completion labels ride the PR, not a coordinator sweep
date: 2026-06-11
category: orchestration
tags: [roles, contracts, docs]
confidence: learned
source: private-work
---

Two lanes shipped real features to production, yet their tracking issues sat open in the to-do column for hours — the PRs lacked the auto-close reference, and the rule requiring it existed only as prose in a doc nobody re-reads mid-lane.

This is the route-at-the-producer principle applied to project boards. The lane that ships the work labels its own completion: the auto-close reference goes in the PR body at authoring time, and the platform then closes the issue and moves the card on merge — zero-cost automation that already exists. The coordinator owns claiming and column moves during the lane's life; a session-start drift check flags any board/reality mismatch. A coordinator sweeping boards after the fact is the same smell as a downstream triage step compensating for an unlabeled producer.

Make the constraint travel mechanically: it belongs in the worker launch prompt and in a drift check, not in the coordinator's memory.
