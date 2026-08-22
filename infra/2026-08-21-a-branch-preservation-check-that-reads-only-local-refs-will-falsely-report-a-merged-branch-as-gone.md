---
title: A branch-preservation check that reads only local refs will falsely report a merged branch as "gone" — the remote is the actual source of truth
date: 2026-08-21
category: infra
tags: [tooling, verification, git]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An inventory sweep flagged several branches as having no remote copy at all, based on the local
checkout's own remote-tracking references — every one of those branches, however, was in fact
present on the remote; the local remote-tracking refs were simply absent because the platform
automatically deletes a branch's LOCAL tracking reference after it merges or its pull request
closes, while the branch itself may still exist remotely, or its history may still be reachable
through the merge commit. A tool that treats an absent local tracking ref as proof a branch is
gone will produce false "branch lost" alarms exactly for the branches that were successfully
merged and cleaned up — the opposite of actually lost work.

The generalizable rule: any check whose job is to confirm a branch (or any other artifact)
genuinely still exists should query the REMOTE directly (the platform's own API, or an explicit
remote listing) rather than relying on a local checkout's tracking references, which are routinely
stale or deliberately pruned and are never the actual source of truth about what exists remotely.
