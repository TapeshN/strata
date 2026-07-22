---
title: When a fresh analysis conflicts with a previously recorded decision, follow the recorded decision rather than re-litigating it
date: 2026-07-21
category: orchestration
tags: [coordinator, decision-tracking, recorded-decisions]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Two genuinely separate features had drifted to look like one blurred feature in the product's own presentation — same label used for both, one of the two looking noticeably less developed than the other. A fresh read-only analysis, reasoning from what it observed in the moment, recommended merging them into a single unified surface. But a decision to keep them as two DISTINCT, separately-identified surfaces had already been made and recorded earlier, for reasons the fresh analysis wasn't aware of.

**The rule:** when an agent's newly-generated proposal conflicts with a decision that was already made and recorded, the recorded decision wins by default — a fresh analysis reasoning only from present-moment observation doesn't know what the recorded decision already accounted for. Revisit a recorded decision deliberately and explicitly if there's genuine reason to, but don't let a plausible-sounding new proposal silently override it just because it wasn't checked against the record first.
