---
title: A long planning session's output scattering across many docs is the exact redundancy a single typed handoff event exists to prevent
date: 2026-07-02
category: orchestration
tags: [docs, layering]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A long, substantive planning conversation produced a decision and its rationale — genuinely valuable output — but that output ended up copied, in overlapping form, across more than half a dozen separate control-plane documents by the time the session closed: a vision document, a spec, a running-state file, a queue of next steps, a durable ledger, and an agent's own memory. This is exactly the kind of redundancy a handoff mechanism is supposed to prevent, and it happened precisely because there was no routing discipline — every session simply appends to whichever flat documents feel relevant, and nothing decides that a given piece of output has one canonical home.

The fix that was dogfooded in the same session: collapse the session's output into one terse, typed handoff entry that *points at* the durable artifact where the substance actually lives, rather than re-narrating that substance again in a new location. A handoff should function as a router to the one canonical place a decision lives, not as another copy of it.

The generalizable practice for any team running multiple overlapping coordination documents: at the close of any session that produces durable output, write exactly one typed pointer event naming what happened and where its durable record lives, and resist the urge to also restate the substance in every document that feels adjacent. Redundant restatement of the same decision across documents is a symptom of missing typed routing, not a substitute for it.
