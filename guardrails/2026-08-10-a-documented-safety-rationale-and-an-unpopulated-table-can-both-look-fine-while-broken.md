---
title: A documented safety rationale and an unpopulated table can both look fine while broken
date: 2026-08-10
category: guardrails
tags: [read-artifact-before-flagging, docs, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

We saw a permanent navigation destination — one of a handful of top-level entries rendered for every user of a product — carry an explicit code comment justifying why it was safe to link to unconditionally: the destination itself rendered a calm, well-designed empty state whenever nothing was configured. That justification is true for a page a user chooses to visit, and false for a permanent navigation entry, because a nav entry is itself a claim about what the product contains for this user — and for the overwhelming majority of live accounts, that claim was false. The comment's presence was part of the problem: because a plausible, written reason already existed, nobody re-examined it. So now: a documented reason a piece of UI is safe is not a verified one — when a comment explains why something is safe, check what it assumes about who is calling it, and gate any navigation entry on the same resolver its destination page uses, so the two can never disagree.

We also saw a single database table with zero rows across an entire live product silently disable three unrelated features that each read from it — a review-gate check, a summary line in a user's own greeting, and an entire secondary page — every one of them degrading independently to its empty or false branch, with nothing surfacing why. A script existed to populate that table; it was idempotent, well-gated, and correct — it had simply never been run, and its absence was invisible precisely because every reader of the table failed soft instead of loud. So now: a table that a product feature depends on for its default behavior needs an explicit zero-rows check that fails loud, because a backfill that exists but was never executed is otherwise indistinguishable from a missing feature.
