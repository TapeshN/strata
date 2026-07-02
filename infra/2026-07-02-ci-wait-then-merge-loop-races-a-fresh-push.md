---
title: A wait-for-CI-then-merge loop can race a fresh push — the old run settles before the new one registers, and the merge gate correctly refuses on stale-pending
date: 2026-07-02
category: infra
tags: ci, gating, preflight
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A background loop that polls "are all checks non-pending yet, then attempt merge" was run immediately after pushing a fresh commit. Repeatedly, the loop observed the checks from the PREVIOUS push finish and settle to green, concluded all checks were done, and attempted a merge — at which point the merge gate correctly refused, because the NEW push's checks had by then registered as freshly pending and the gate's job is specifically to never merge while anything is pending. This is the gate behaving exactly as designed; the waste was entirely in the polling loop racing its own push.

The fix: after any push, sleep for a fixed short interval (long enough for the CI provider to register the new commit's check runs) before starting the "wait until non-pending" poll. Without that pause, the poll loop's first few iterations are structurally guaranteed to see stale state from the prior commit, not the new one, and will either merge prematurely against the wrong commit's checks (if the gate is naive) or spin through a wasted refuse-retry cycle (if the gate is correctly conservative, as here).

The generalizable rule: any "push, then poll CI, then merge" automation must treat "checks are non-pending" as ambiguous immediately after a push — it could mean either "the new checks finished" or "the new checks have not registered yet, so there's nothing pending to see." A short fixed delay before the first poll closes that ambiguity cheaply; polling immediately does not.
