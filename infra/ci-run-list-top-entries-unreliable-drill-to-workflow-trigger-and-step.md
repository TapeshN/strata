---
title: A CI run list's top entries can misrepresent branch health — drill to the right workflow, trigger, and failed step before declaring a regression
date: 2026-06-13
category: infra
tags: [ci, gating, preflight]
confidence: learned
source: private-work
---

The most recent entries in a CI run list are unreliable as a proxy for branch health. Two distinct failure modes:

**1. Bot workflows crowd out product CI.** Automated comment-triggered workflows (bots, proposal generators, status reporters) each generate a run entry. When the main branch receives many comments, these entries fill the recent-run list, burying the actual build or test workflow. A repo showing only skipped bot runs at the top of its run list is not "green" — it may simply have no product CI triggered on push to that branch (because the real CI runs only at the pull-request gate, not on push to main).

**Triage rule:** confirm the trigger for the relevant CI workflow before interpreting the run list. If the product tests run on `pull_request` (not `push`), then the main branch's run list will never show a green product-CI pass — the evidence lives on the PR's check suite, not the branch run list.

**2. A workflow-level failure may be a non-product step.** A red workflow icon on a scheduled run means one or more jobs or steps failed, not necessarily that product tests failed. The failed step may be a post-test artifact uploader, report-merger, or notification step — all of which can fail while every test shard passed. Inspect the failed job and step explicitly (`run view --json jobs`) before calling the failure a regression.

**Conservative posture:** a CI-health verdict drawn from the run list surface is preliminary. Filter out skipped and non-product triggers; for any red, confirm the failed step's nature before concluding there is a product regression.
