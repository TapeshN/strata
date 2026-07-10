---
title: A judge or evaluation step in an always-on pipeline that requires a metered key silently holds the whole backlog hostage
date: 2026-07-07
category: orchestration
tags: [cost, judge, model-tier-routing]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A background pipeline designed around a "collect continuously, process whenever convenient" model had one step — an LLM-as-judge evaluation gating what gets processed further — that only ran against a metered, pay-per-call model unless an explicit opt-in flag was set. With that flag unset by deliberate policy (the operator did not want ongoing metered spend for this pipeline), every item collected sat permanently held, waiting on an evaluation step that would never run under the pipeline's own default configuration. Nothing was lost, but the entire value of "collect now, evaluate and prioritize later at no cost" was silently defeated by one gated step buried inside an otherwise free pipeline.

The fix: reroute the judge step through a locally hosted, no-cost model as the default, treating a metered cloud model strictly as an optional quality upgrade a user can opt into, never as the only path to a functioning pipeline.

The generalizable design rule: any evaluation, scoring, or judging step embedded inside an always-on background pipeline should default to a free, locally available option, so the pipeline's core value proposition — processing a backlog without incurring per-item cost — cannot be silently defeated by one internal dependency on a metered resource. A pipeline whose backlog can only ever move forward by spending money is not actually a "collect for free, process at your convenience" pipeline, whatever it is named or documented as.
