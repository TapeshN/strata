---
title: Surface bloat recurs because every gate is local, and coherence is a global property
date: 2026-08-25
category: infra
tags: [architecture, information-architecture, gate-design, recurring-failure]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A product's most visible screen accumulated overlapping features until a stakeholder observed — for the second time in a month — that it had returned to exactly the redundancy it had already been cleaned up from once. The question they asked was the right one: why is this periodic rather than structural?

Because every unit of work is scoped as "add X" and verified as "X works". A brief says build the feature, the acceptance says the feature works, the review checks the feature. Three honest successes, and the assembled experience is worse — because no step in the loop ever asks what got WORSE. The objective function is per-feature; the damage is systemic.

Three structural reasons it recurs. Surfaces have no owner and no budget: code has owners, screens do not, so appending to the most visible surface costs nothing and it is appended to until ruined. Placement is decided at build time by whoever is nearest the code, with no authority to consult — asked "where does this go?", a builder picks the most visible surface, and the home screen always wins. And every gate is LOCAL: tests, type checks and diff review all answer "is this change correct?", while none answers "is the system still coherent?".

What would make it structural: a per-surface budget enforced by a counting test, so adding a section means removing one and scarcity forces the argument at the right moment; placement decided at BRIEF time by whoever is looking at the whole, and stated so the builder does not choose; a whole-experience check that renders every surface, tests each against its declared job, and flags the same data queried by two destinations, because duplicate detection is mechanisable.

The generalizable form: when a quality is restored only by a human noticing, it is not a property of the system — it is a property of that human's attention, and it decays the moment they look away. Anything you find yourself re-fixing on a cadence is a missing gate, and that gate must measure the GLOBAL property, because local correctness is exactly what was already passing while the whole degraded.
