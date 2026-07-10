---
title: A long-running dispatch's completion poll can outlive a foreground timeout and leave state orphaned
date: 2026-07-07
category: orchestration
tags: [orchestration, durable-execution, dispatch]
confidence: learned
source: private-work
---

A tool that dispatches a real, multi-file coding task to a remote agent and then blocks locally, polling until that agent finishes, works fine for a small task but breaks down for a substantial one: a genuine multi-file feature can easily take ten to twenty minutes or more, which is far longer than a typical interactive foreground command is allowed to run before being killed. When the local process is killed mid-poll, the remote agent keeps working and eventually succeeds — opening a real pull request with everything it was asked to build — but locally, the task never gets marked as handled: it's left sitting in a "not yet dispatched" state (risking a duplicate dispatch if retried blindly) and a cost/usage record that a later step was supposed to write never gets written, even though the underlying work genuinely completed and shipped.

The recovery is to check the remote system directly (did a pull request actually land for this task) before assuming anything, and to manually reconcile the local bookkeeping to match reality — moving the task out of its "pending" state, and separately reconstructing any missing usage/cost record.

The durable fix: a dispatch expected to take a long time should never be foreground-polled to completion inside a process with its own hard timeout. Fire the dispatch, record that it fired, and then check on its progress on a SEPARATE cadence — either by polling asynchronously outside the timed-out process, or by running the dispatcher itself as a detached, resumable job that checkpoints its own progress to disk. Treat "the foreground poll got killed" as "this task's local state may now be inconsistent with reality" and always reconcile explicitly rather than assuming either success or failure.

A separate, security-flavored lesson from reviewing a different real dispatch around the same time: a function that accepts BOTH a trusted, already-verified scope (say, the calling user's own session) AND a second, caller-suppliable identifier for the same resource is a latent authorization gap — even if, today, the only place that calls it happens to pass identical values for both. A future caller that passes a different value for the second parameter would silently bypass the intended scoping. The fix is structural: remove the redundant caller-suppliable parameter entirely so the identifier can only ever come from the trusted scope, rather than trusting every future caller to remember to pass the "safe" value — and add a test that specifically exercises the cross-scope case to confirm the guard actually short-circuits before any sensitive operation runs.
