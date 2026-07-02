---
title: An action with an external paid side effect must be presumed to have fired until remote evidence proves otherwise — silence at the local process is not proof of no effect
date: 2026-07-02
category: guardrails
tags: [autonomy, cost, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An earlier stall in a dispatch pipeline — a long period of zero output before any confirmation of success — was diagnosed and written up as a pre-dispatch, environment-level failure (the request never actually went out). The next day, evidence surfaced that three separate "failed" attempts at the same dispatch had each, in fact, completed the outbound network call successfully and each produced its own independent piece of downstream work — the local process had simply hung AFTER the remote call succeeded but BEFORE it recorded that success locally, so each retry looked identical to "never dispatched" from the local vantage point alone.

The root cause of the misdiagnosis: an outbox or task-queue entry that hasn't moved, combined with zero local output, was pattern-matched to "the request never fired" without checking for independent, remote-side evidence of the opposite.

The fix and the durable rule: after ANY hang or stall in a pipeline step that has an external, paid, or otherwise real-world side effect, the first action is to check for remote evidence of that side effect (open work items, dashboards, logs on the receiving system) BEFORE trusting local state or firing a retry — "the local record hasn't moved" only proves the local record is stale, never that the remote call didn't happen. A pipeline step with this risk profile should also write a durable local receipt immediately after the outbound call succeeds, before any further local processing, so "dispatched but not yet finalized" becomes mechanically distinguishable from "never dispatched" without needing to check remotely every time.
