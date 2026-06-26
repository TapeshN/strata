---
title: Dispatch quality must be measured at the brief level, not assumed from the result
date: 2026-06-23
category: orchestration
tags: [dispatch, eval, brief-quality, route, model-tier-routing, dispatch-quality, learning-loop]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A dispatch pipeline that routes work to an execution agent may still bypass the steps that make the pipeline defensible: brief enrichment, pre-send quality evaluation, and post-result quality scoring. Without these three steps, the pipeline is a transport mechanism — it moves work from requester to executor — but it produces no signal about whether the brief was well-formed or whether the result met the delivery standard.

The specific failure: when the orchestration layer has a brief-composition step (enrichment from a learning corpus, relevance-matched context injection, model-appropriate framing), bypassing it means every brief is a raw hand-written description with scaffolding wrapped around it. No pre-send rubric evaluates whether the brief is specific enough for the executing model. No post-result score feeds back into a dispatch-quality ledger.

The consequence is that the only signal improving over time is coarse model selection. The brief-quality flywheel — the mechanism that would make dispatches better with each iteration — never turns.

The fix is to route every dispatch through the enrichment and evaluation path, not to treat it as optional or a future phase. A dispatch is not done at the transport layer; it is done when the brief has been composed for the executing model, evaluated against a quality rubric, and the result has been scored and recorded. Evaluation applies to the dispatcher itself, not only to the agent it dispatches.
