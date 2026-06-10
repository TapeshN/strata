---
title: Model-tier routing must be applied at the spend point — platform defaults silently override org doctrine
date: 2026-06-10
category: orchestration
tags: [model-tier-routing, cost, fan-out, doctrine]
confidence: learned
source: private-work
---

An organization can hold a clear cost doctrine — small models classify, mid-tier models build and audit, flagship models strategize and judge — and still burn flagship rates on routine work, because the doctrine was never applied where the spend actually happens: the individual agent-spawn call inside an orchestration script. A 27-agent housekeeping audit (cross-referencing board state, deduplicating issues — squarely mid-tier work) ran every agent at flagship cost because the spawn calls omitted an explicit model and the platform's default guidance ("omit unless confident") silently won over the house rule.

Two fixes travel together. First, make the tier explicit at every spawn site: recon, audit, cross-reference, and refutation agents get the mid-tier model by name; pure classification gets the small model; only the final synthesis or judge inherits the session's flagship. Second, notice that nothing *metered* the mistake — a cost gauge that stamps a flat constant per turn produces zero signal when a fan-out runs ten times overpriced. A cost discipline without a true cost gauge is a vibe, not a control; the human noticing the bill is not a monitoring strategy.
