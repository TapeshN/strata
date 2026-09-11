---
title: Client-brand fidelity is stage zero — extract the client's own assets and layout priorities first, and grade review against their site, not your own direction
date: 2026-08-30
category: guardrails
tags: [design-fidelity, extraction-first, review-grading, client-work]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A client-facing site rebuild shipped with an invented visual identity — a different accent color, a simplified wordmark — and quietly dropped two of the client's existing features, one of which had held a prominent, dedicated position in the original site's layout. Two separate failures produced this. First, the scout stage that gathered source material captured copy and access details but never captured brand assets (logo files, exact colors) or a full inventory of existing sections with an explicit keep/drop judgment for each. Second, and more structurally: the adversarial review meant to catch this graded the output against the team's own design direction rather than against the client's actual site — a review that shares the same baseline as the thing it is reviewing can never flag an omission that direction itself introduced.

A related, smaller failure surfaced in the same piece of work: an internal briefing mischaracterized one of the client's existing features as minor, and only a separate step that actually inspected the real artifact caught that the premise was wrong. Treating a stale or unverified premise as suspect applies just as much to a team's own briefing of its own plan as it does to a plan inherited from someone else.

The generalizable fix: for any project rebuilding something a client already has, run brand and layout extraction as an explicit first stage — logo assets, exact colors sampled from those assets rather than guessed, and a full section inventory with a keep/drop decision for every existing element — before any design or build work starts. Make the verification stage grade against the client's own current site as the source of truth, never against the same direction the build stage used. And treat every distinct client asset — a signature piece of content, a flagship feature — as needing exactly one clear home in the rebuilt structure, checked mechanically rather than assumed.
