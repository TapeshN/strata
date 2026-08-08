---
title: A brief that says "port or reuse this feature" must pin the exact branch it lives on
date: 2026-08-08
category: orchestration
tags: [briefs, cross-repo, branch-pinning, coordinator-doctrine]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A feature can be real, correctly built, and thoroughly tested — and still be completely absent from the branch an agent is told to build from, because it only exists on a different, unmerged feature branch. When a brief says "port X" or "reuse the Y we built" without naming the exact branch X or Y lives on, it silently assumes the referenced work is on the default branch, which is often not true for recent or in-progress work. An agent that correctly finds nothing, refuses to fabricate a substitute, and reports the absence honestly has still spent a real, wasted recon pass chasing something the brief implied was present. The fix is cheap and mechanical: any brief that names a feature to port or reuse must cite the exact repository and branch it lives on, or explicitly instruct the executor to confirm presence on the default branch first. This generalizes beyond deliberate porting briefs to any cross-repo or cross-branch reference to "what we already built" — the reference is only actionable once it is pinned to a specific ref.
