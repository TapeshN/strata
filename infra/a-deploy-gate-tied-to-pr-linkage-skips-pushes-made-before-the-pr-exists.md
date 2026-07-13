---
title: A deploy gate that only builds pushes carrying a pull-request identifier silently skips every push made before the PR exists
date: 2026-07-13
category: infra
tags: [ci, release, preview-deploys]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A workspace's deploy budget policy configured its build platform to skip any branch push that isn't either the main branch or one already associated with an open pull request — a sensible way to avoid billing a preview build for every intermediate commit. The workflow most teams actually use, though, is: create the branch, push it, then open the pull request. Under that ordering, the very first push — the one that would otherwise trigger the preview a reviewer needs to look at — always lands before the PR exists, so the build platform silently cancels it as an ignored step, and nobody sees a preview until they realize they have to force one.

The reliable fix is a small standard tail step: once the pull request is open, push an empty, no-op commit to the branch so the platform's next build carries the PR association and actually runs. A better fix at the source is to reorder the habit itself — open the pull request immediately after the first push, before any more work happens on the branch — or extend the gate's own logic to also build branches that have an open PR even if the specific push predates it. Any CI/CD system that conditions builds on PR linkage should be treated as having this blind spot by default until proven otherwise.
