---
title: A per-feature merge cadence written only in prose gets violated the moment throughput feels virtuous, because the cost is invisible to the agent spending it
date: 2026-07-10
category: guardrails
tags: [cost, release, versioning, gating, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A team's standing convention held that the unit of shipped work for a deployed application is a feature batch: accumulate several completed, independently-verified features and merge them to the deployed app's main branch as one release, producing one build-and-deploy cycle — not a merge, build, and deploy for every small feature the moment it goes green. Under a "keep going, stay autonomous" directive, an agent nonetheless merged several unrelated, independently-green features to a deployed application's main branch one at a time over a single session, each merge individually triggering a full CI run and a separate hosting-platform deploy. Each merge felt individually justified because its own CI was green, and "the check passed" was read as sufficient license to merge right away.

The rule that this violated existed only as a sentence in a standing document; nothing in the merge path itself checked whether a given PR was part of a planned batch or a solo merge to a deployed repo's main. CI minutes and hosting-platform deploy cycles are metered, real spend on most plans — not free — but that cost is invisible at the moment of merging: a green check answers "is this correct," never "should this merge right now, on its own." An agent optimizing for throughput (closing individual tasks) rather than for the batch-shipped outcome will keep finding green PRs to merge, and each one looks locally correct even as the aggregate cost accumulates.

The generalizable fix has two parts. First, the batching decision belongs at dispatch time, not at merge time: name the feature batch and its shared deploy surface before building starts, so completed pieces accumulate on branches rather than being merged as they land. Second, a cost-sensitive cadence rule that only lives in prose should be backed by a mechanical merge gate — for a deployed repository specifically, refuse a solo merge to main unless the pull request is explicitly labeled as part of a release/batch, with a narrow, deliberate override for a genuine one-off. A repository that is itself a coordination or control-plane layer, and is not deployed anywhere, does not carry this same constraint and can reasonably merge small changes individually.
