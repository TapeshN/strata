---
title: Lowering a database transaction's isolation level was the correct money fix — a stricter isolation level was destroying completed payments
date: 2026-08-17
category: guardrails
tags: [money-integrity, concurrency, verification]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A batch of many concurrent, financially-independent transactions (settling distinct paid records
at the same moment) lost a large fraction of them under the strictest available transaction
isolation level — the actual conflict trigger was a notification insert plus commit happening
inside the same transaction, not the read that the isolation level was ostensibly protecting.
Restructuring the reads first improved the loss rate only marginally. Switching to a lower,
read-committed isolation level, combined with a conditional update keyed to the record's own
primary key and a per-scope database uniqueness constraint, recorded a clean result with the
"exactly once" property intact under every deliberately-engineered concurrent attack tried
afterward, including same-record and distinct-record concurrent bursts and provider-callback races.

The generalizable lesson: when the actual invariant that must hold is a single row's own
conditional state transition, a LOWER isolation level combined with an explicit conditional update
and a database-level uniqueness constraint can be STRICTLY SAFER for money than a stricter
isolation level whose automatic conflict-abort-and-retry machinery ends up aborting transactions
that had already committed real, distinct, correct payments. More retry attempts cannot rescue a
workload whose conflicts are triggered by an insert the transaction itself performs; the fix is
architectural (lower isolation plus an explicit conditional claim), not "retry harder." Any change
to a transaction's isolation level should be evaluated against two adversarial scenarios before
being trusted: many concurrent attempts against the SAME key (must resolve to exactly one winner)
and many concurrent attempts against DISTINCT keys (none should be lost).
