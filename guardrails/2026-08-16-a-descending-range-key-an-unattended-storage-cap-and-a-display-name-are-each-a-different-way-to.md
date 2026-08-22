---
title: A descending range key, an unattended storage cap, and a display name are each a different way to trust the wrong signal
date: 2026-08-16
category: guardrails
tags: [contracts, idempotency, boundaries, security]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A lookup table encoded a directional range using a simple "low, high" pair, but some ranges were
stored in DESCENDING order (high value listed first) — a naive `low <= n <= high` bounds check
silently matches nothing at all for those rows, so an overlap search over the whole table quietly
skipped them until a specific failing pair forced the bug into the open. Any range-key parser
should min/max the two endpoints explicitly before comparing, rather than trusting stored order.

A usage cap on a shared resource was implemented as three separate steps — check the current
count, and only if it is under the limit, create a new record — run as independent round trips
rather than one atomic operation. A burst of concurrent requests can each pass the check before
any of them commits its creation, so the real count ends up above the intended cap. Any
accumulation limit is the same class of correctness problem as money: it needs an answer to "what
happens when many requests check the limit at the same instant," using the codebase's existing
atomic-transaction pattern, not a prune-then-count-then-create sequence.

A feature correlating repeat visits "by device" actually keyed its lookup on a user-supplied
free-text display name, so continuity of history survived even if a stronger identifier was lost
— but the same design meant literally anyone who typed the same first name inherited a stranger's
history, which was independently confirmed exploitable. The tell was that the feature's own
happy-path regression test PASSED, because the code has no way to distinguish "the same person
came back" from "a different person typed the same string" — a continuity test can look
indistinguishable from a working exploit. The fix pattern: continuity must be keyed to a separate,
high-entropy, server-issued token compared by exact match (hashed at rest, timing-safe compare);
free-text attributes may LABEL an identity for display but must never WIDEN which records match it.
