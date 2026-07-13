---
title: An inferred cost or billing claim stamped into durable docs before it is verified propagates as fact everywhere it is copied
date: 2026-07-13
category: guardrails
tags: [cost, verify-dont-infer, docs, process]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

While wiring a new option into a dispatch path, an engineer needed to note whether the new choice would cost more to run than the existing default. Rather than asking or checking directly, they inferred an answer from an old, unrelated code comment nearby that happened to use similar wording about a different distinction, and wrote that inference into a code comment, a changelog entry, and two separate write-ups — as if it were a verified fact rather than a guess. It turned out to be wrong: the option in question was ordinary usage under the existing plan, not the extra-billed tier the old comment had been describing. By the time this was caught, the incorrect claim had already been copied into four separate durable places.

The fix was mechanical once caught: correct the claim everywhere it had been stamped, then re-verify. The generalizable rule is upstream of that: a cost, billing, or plan-tier claim should be checked against the actual source of truth — the vendor's own documentation, or whoever owns the account — before it is written into anything durable, never inferred from an adjacent, possibly-unrelated piece of context. When there isn't time to verify immediately, the claim should be written down explicitly as an open question rather than confidently asserted, because stating an assumption out loud is what let it get caught and corrected quickly in this case — a claim buried silently inside other work would have taken much longer to notice.
