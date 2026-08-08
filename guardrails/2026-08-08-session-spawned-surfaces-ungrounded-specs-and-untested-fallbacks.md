---
title: A session-spawned surface outlives its session; an ungrounded spec must say so; an unexercised fallback fails its first real batch
date: 2026-08-08
category: guardrails
tags: [client-surface, teardown, session-boundary, spec-grounding, fallback, execution-witness]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Any surface an external party — a client, a stakeholder — could load, such as a preview tunnel, a demo server, or a temporary deployment, that was spun up inside an ephemeral working session does not automatically die when the session ends. If nothing explicitly owns tearing it down, it can keep serving — and keep failing, once whatever kept it alive disappears — for days after the session that created it is long gone, with the party who was given the URL never told otherwise. Any such surface needs either a lifetime provably bounded to its spawning session, or an explicit, monitored owner responsible for its liveness. Any repository a client-facing surface is built from should be a properly registered checkout, not an ephemeral clone living inside a session's own scratch space, which is never a substitute for "the checkout."

A specification authored by an agent or session that cannot see the actual target repository will faithfully transcribe the requirements it was given while simultaneously, confidently re-deriving the codebase's actual shape wrong — reusing the name of a model that already shipped with the opposite structure, reviving a status or label a prior change deliberately retired, proposing a design that conflicts with an existing architectural convention, or listing as "open questions" things the shipped code already answers. Because the prose reads fluently and the requirements are faithfully captured, this class of error is easy to miss. A spec written without direct repository access should carry an explicit banner naming itself as ungrounded and naming the exact branch it must be reconciled against, and a mandatory grounding review — comparing the spec against that real branch, not against general familiarity with the project — must happen before the spec reaches anyone downstream.

A degraded fallback code path that exists for when a primary path can't run has no evidence behind it just because it "exists and passed its own isolated test" — the only real evidence is running it against a real, current batch of the data it will actually face. A fallback that had never been exercised against real data, when finally run for the first time by an evaluator specifically checking it, was found to corrupt a majority of its output in ways an isolated unit test never surfaced. Before any unattended or automated channel is armed, or re-armed, to rely on a degraded fallback, execute that fallback against a real, current batch first — passing in isolation is not evidence it survives today's actual data shapes.
