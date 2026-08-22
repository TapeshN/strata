---
title: Merging to a repo's main branch does not put the change on a deploy target that builds from a different branch
date: 2026-08-16
category: guardrails
tags: [release, gating, boundaries]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A deploy pipeline for a containerized or otherwise built application often builds each
target from a specific source branch pinned in a release script or a registry — not
necessarily the repo's default branch. Merging a batch of pull requests into the default
branch integrates the code into the mainline history but reaches zero running deploy
targets if none of those targets actually build from that branch. The gap is easy to
miss because "merge" and "deploy" are so often the same action in smaller setups that
it's tempting to treat them as one event; here they turned out to be separated by three
distinct facts — which branch the target's build step actually reads, whether that
branch is even reachable and clean for a rebuild, and whether a pending schema migration
also needs to run — and none of the three was checked before merging on an instruction
to "merge the deploy targets."

The generalizable rule: before merging or claiming a change is deployed, trace the
actual deploy path to the running artifact — read the release/build tooling and
whatever registry names the branch each target builds from, and check that branch's own
status — rather than assuming an instruction to merge is also authority to assume the
change is live. "Merged" and "running on the target" are two separate claims that each
need their own verification.
