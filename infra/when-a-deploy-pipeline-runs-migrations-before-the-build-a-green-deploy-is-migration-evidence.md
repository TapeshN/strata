---
title: When a deploy pipeline runs migrations before the build and fails the build on migration failure, a green deploy IS sufficient migration evidence
date: 2026-07-21
category: infra
tags: [deploy, migrations, prod-witness, release]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

The general caution that a merged migration isn't applied to production until the deploy pipeline actually runs it has a useful flip side: if your deploy pipeline is built so that applying pending migrations happens BEFORE the application build step, and a failed migration fails the whole build (so a failed migration can never result in a new deployment — the old code just keeps serving), then a successful "deploy ready" status on a migration-carrying merge is itself sufficient evidence the schema change applied. No separate manual verification step is needed, once you've confirmed that specific ordering-and-fail-behavior invariant holds for your pipeline.

**The rule:** verify ONCE, explicitly, that your deploy pipeline runs migrations before build and fails the build on migration error — then you can trust "deploy succeeded" as proof of a successful migration going forward, rather than re-checking it by hand on every migration-carrying release.
