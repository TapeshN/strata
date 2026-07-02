---
title: A cleanup routine that snapshots its target set outside the transaction can permanently leak elevated privilege
date: 2026-06-30
category: guardrails
tags: [toctou, owasp-a04, money-auth, transaction-discipline, concurrency]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A subscription-teardown routine read the current member list with a plain lookup, then opened a transaction afterward to downgrade every member it had found. A new member who joined between the read and the transaction was never included in the snapshot — their join row was removed by the cascading delete, but their elevated access was never reset. The gap was invisible to any test that didn't race a concurrent join against the teardown.

This is a classic time-of-check/time-of-use (TOCTOU) race, but it is worth naming precisely because the fix is not "add a lock" in the abstract — it is that **the read of the mutable set and the destructive write against it must happen inside the same transaction that also excludes concurrent mutation of that set.** Locking the parent row for update and re-reading the child set from inside that lock serializes the teardown against any concurrent path that also touches the same row. Reading first and transacting second leaves exactly the race window an attacker (or an ordinary user with unlucky timing) needs.

The same shape recurs in adjacent forms: a capacity or quota check that re-reads the current count but compares it against a limit fetched before the lock is still racy, even though the count itself was re-read inside the lock — both sides of the comparison must be read from inside the same locked scope. Any destructive or privilege-reducing operation that first identifies "the set of things to act on" and then acts on that set in a separate step needs the same scrutiny: if another path can mutate membership in that set between the two steps, the identification step must move inside the same transactional boundary as the action.

The failure mode is also hard to catch with mocked tests, because a mock that serializes calls sequentially can't reproduce the race — proving the fix requires a real concurrency test against a real transactional store, not an assertion that the two steps were called in the right order.
