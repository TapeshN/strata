---
title: In a multi-agent adversarial review, the value is in the refutation layer — adjudicate by reading the code, never by counting votes
date: 2026-07-22
category: orchestration
tags: [review, adversarial, adjudication, security]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Running several independent review agents in parallel over the same change surfaced a double-digit number of findings across multiple risk dimensions; on independent verification, the large majority were refuted and only a small handful of low-severity items actually survived. Two of the refuted findings were simply wrong on the facts — one claimed a capability's implementation had been deleted when it had actually been relocated and remained fully enforced elsewhere. Trusting either "most agents agree" or a reviewed change's own self-reported "review passed" summary would have been trusting a vote count, not a verified fact.

**The rule:** the real value of running multiple adversarial reviewers isn't their raw finding count, it's the REFUTATION pass that follows — a human or coordinator must personally read the actual code for every disputed or high-risk finding and adjudicate based on what the code actually does, rather than trusting how many reviewers raised (or didn't raise) a given concern, or trusting a change's own self-assessment of its review status.
