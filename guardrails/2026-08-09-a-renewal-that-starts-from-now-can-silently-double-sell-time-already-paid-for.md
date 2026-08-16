---
title: A renewal that starts from "now" can silently double-sell time already paid for
date: 2026-08-09
category: guardrails
tags: [evals, golden-sets, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A purchase or renewal flow for any time-bounded access product (a subscription, a pass, a membership term) that stamps its new start date as "now" will silently discard any remaining time on an account that already has active, unexpired coverage — the new term begins immediately instead of after the existing one ends, and the customer loses the overlap they already paid for. This was found unprompted while reviewing an unrelated part of the same flow, not flagged by any existing test, because every test in the suite purchased from a clean, no-prior-coverage account.

The fix is to compute the new start date server-side from the account's own latest-ending unexpired coverage, so a second purchase queues behind the first with no overlap and no gap. The generalizable test for any recurring-access product: purchase twice in a row within the same test and assert that no paid day is ever consumed twice — a single-purchase-from-a-clean-state test will always look correct regardless of whether this bug is present.
