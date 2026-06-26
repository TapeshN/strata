---
title: A merged pipeline can be code-complete and key-valid yet have never completed a live run
date: 2026-06-16
category: guardrails
tags: [ci, release, monorepo, compiled-dist, stale-build, wired-not-working, integration-witness]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A pipeline can be fully coded, merged, properly credentialed, and configuration-correct — every unit test green, every type check passing — yet have never completed a single live execution. When that pipeline finally fires for real, a latent integration bug surfaces that no local gate caught.

A common instance in monorepos: a shared package is updated at the source level, but its compiled distribution is gitignored and never rebuilt. The primary checkout pulls the new source correctly; the runtime executor loads the compiled distribution, which was built before the update and does not contain it. Unit tests pass because they run against fresh source via a TypeScript transpiler; the runtime consumes the stale compiled output. Pulling from the remote does not rebuild compiled distributions — that step must be explicit.

The general form: any artifact that is (a) derived from source, (b) not tracked in version control, and (c) consumed by the runtime — not by the test harness — is a candidate for this failure. The test suite is immune because it bypasses the artifact; the real execution is not.

Prevention: before declaring an integration "working," execute a full end-to-end live run and confirm the result at the authoritative source (the downstream system's status API, not local stdout, which may buffer or truncate). For monorepos with compiled shared packages, include a workspace rebuild step in any preflight or "before first dispatch" checklist. Mark integration lanes as done only after a live execution witness — not after CI green on unit tests.
