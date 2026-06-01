---
title: Separate PR hygiene from release integrity — and "looks unofficial" is a real signal
date: 2026-05-31
category: infra
tags: [release, oss, versioning, ci]
confidence: learned
source: private-work
---

A maintainer flagged a public package's PR as "looks unofficial — not tagged or labeled," and suspected the automation had been sloppy. Investigation showed the PR itself was clean and conventional; the real gaps were structural: (a) no PR-hygiene convention existed, so a whole run of prior PRs had zero labels/milestones and the flow just matched that bare pattern; (b) PR templates can't auto-apply labels/milestones (only issue templates carry that), so it's inherently procedural; (c) separately, the package published manually from a laptop, so artifacts were signed but carried no provenance/attestation — the actual integrity gap, distinct from the cosmetic label gap.

General lesson: two different concerns hide behind "this looks unofficial." PR hygiene (labels, milestones) is procedural — surface it in every handback. Release integrity (tags, signatures, *provenance* via tokenless OIDC publishing from CI) is mechanical — make it a workflow, not a habit. And a "looks unofficial" report is a real quality signal worth checking against repo history before attributing it to the agent.
