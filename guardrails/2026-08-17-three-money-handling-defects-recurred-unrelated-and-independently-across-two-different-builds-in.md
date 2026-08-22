---
title: Three money-handling defects recurred, unrelated and independently, across two different builds in one day — bake known traps into every dispatch brief
date: 2026-08-17
category: guardrails
tags: [money-integrity, dispatch, gate-design]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Two different builds, built independently by different people at different times, shipped the
exact same three defects: a payment-provider callback URL derived from the in-process request's
own perceived origin (which can be an internal, non-public address rather than the real public
one); a monetary field expected in a smaller unit (such as cents) but parsed as though it were
already in the larger unit (such as dollars), silently inflating amounts by two orders of
magnitude; and a money-related setting change that failed silently and reported success rather
than surfacing an error. Separately, a feature that had originally been curated as purely cosmetic
was later, quietly, turned into a real charge-triggering surface by an unrelated change, without
anyone re-running the audit that determines what counts as a "money-adjacent" feature.

Known traps that have already bitten more than once belong in the WRITTEN BRIEF handed to every
future builder, not only in a reviewer's private memory of past incidents — a trap caught for the
second time is an instruction to add to the standard brief, not merely a review finding to log
once more. Relatedly, any change that adds a new charge-triggering path to an existing module
should automatically re-run whatever audit determines membership in the "money-adjacent" set,
rather than relying on someone remembering to re-curate it by hand.
