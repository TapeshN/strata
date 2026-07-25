---
title: A stuck-queued CI job during a platform outage should be triaged against the platform's own status feed, not retried
date: 2026-07-20
category: infra
tags: [ci, gating, latency]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A required check sat "queued" for well over 45 minutes with no obvious cause — the runner queue was empty, no other jobs were competing for capacity, and the workflow configuration itself was unchanged and had run cleanly moments before. The instinct in that situation is to cancel and re-push, or retrigger the job, on the theory that something local to the run is wedged.

Checking the CI platform's own public status feed (its status-page API, not the vendor's marketing status page) showed an active partial outage on exactly the affected component. The stuck job was a symptom of the outage, not of anything in the repository or the job configuration.

General rule: before cancelling, re-pushing, or retriggering a run that is stuck in a way that doesn't map to any local cause, check the CI platform's own status feed for the affected component first. If there is an active outage, retrying is close to pure wasted spend — the queue will not drain any faster for having more jobs added to it. Instead, park the run with a wakeup paced to the platform's typical recovery cadence (not a tight per-minute poll) and only merge once the queue is observed to actually drain. This generalizes to any managed platform dependency: a symptom with no local explanation is a good trigger to check the provider's own status surface before assuming the fault is yours.
