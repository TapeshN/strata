---
title: Probing a dispatch command with an unrecognized flag can silently run it in its default live mode
date: 2026-07-01
category: orchestration
tags: [autonomy, side-effect, contracts, cost]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An attempt to inspect a dispatch tool's available flags by passing a help flag it didn't actually support resulted in the tool ignoring the unrecognized flag entirely and running in its ordinary default mode — which, for this tool, meant continuous operation with autonomous action enabled. It polled its work queue and genuinely dispatched a queued task to an external agent, incurring real cost and opening a real pull request, discovered only when the resulting artifact appeared.

The root cause: a command whose argument parser has a non-erroring path for unrecognized flags, combined with a continuous, autonomous-by-default mode when invoked with no explicit bounding flag, means any invocation — including one intended purely as a safe probe — is a live dispatch. There was no error message signaling that the "help" request had been silently discarded.

The general lesson: to understand a side-effectful tool's options, read its source directly rather than invoking it experimentally, especially when the tool's own help path is unverified. When such a tool does support an explicit single-pass or bounded-run flag, always pass it for any exploratory or diagnostic invocation. And know, before invoking any autonomous dispatcher, what its default action-permission level is when no explicit override is given — a default that permits real dispatch with no human check is exactly the condition under which an accidental probe becomes a real, costly action.
