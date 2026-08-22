---
title: Six money-integrity lessons from one review pass: the witness is collection, not a written row
date: 2026-08-17
category: guardrails
tags: [money-integrity, verification, security-floor]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A financial-correction feature wrote an adjustment row dated "now," and the row existed with the
right amount — but the surrounding accounting logic only ever pulls adjustments into an
already-closed period if their effective date falls within that period, and "now" fell inside a
period that had already been closed out, so the correction could never be collected and could not
even be voided by an operator. A row existing with the correct amount is not evidence that money
actually moved; for any financial write, the true witness is the END STATE of the money (paid,
collected, or reversed), never the intermediate artifact. A correction dated "now" is worthless
whenever "now" happens to fall inside an already-closed accounting period — the effective date
must resolve forward into the next still-open period, and the corresponding test must assert that
the adjustment is actually included once a real run processes that future period.

A reversal (clawback) was derived from whichever prior line item the system happened to look up,
rather than being pinned to the specific party that was actually paid — letting a later, unrelated
actor trigger a second reversal against an innocent third party. Any reversal should refuse to
proceed unless the party it targets matches the party the original payment actually went to, AND
should be backed by a database-level uniqueness constraint per (payment record, adjustment kind) as
the real concurrency backstop — an application-level check alone can still lose a race.

A route trusted "this record names the current user" as sufficient proof of standing to bill a
resource, even though the same user's ROLE had since changed (they had been demoted) — the
framework re-checks role on every request, but this particular handler never asked. Being NAMED by
a record is not the same claim as CURRENTLY HOLDING the role that record assumes; a role predicate
should be checked before any identity match, and re-verified fresh within the same transaction.

A workflow correctly guarded its "submit" transition (checking the resource was in the right state,
not cancelled, and belonged to the right owner) but left its symmetric "accept" transition
completely unguarded — accepting a resource that had already ended, been cancelled, or fallen weeks
out of its valid window all succeeded and were billed. Any workflow with a submit/accept (or
similar forward/reverse) pair of transitions needs the SAME eligibility checks on both halves, not
just the one that was built first.

A newly-added invariant-checking gate had, until that point, only ever been run against already-
compliant code — which is indistinguishable from a gate that does nothing at all. The gate was
only proven real by deliberately planting a violation in a file the gate's author had never told it
to watch, and confirming the gate still caught it. Any new source-scanning gate deserves this same
proof: show it catching a violation it was not specifically tuned for, not just passing on
compliant input.

Finally, a feature flag that defaulted to ON whenever its configuration row was simply absent made
every account provisioned outside the standard seeding process default-reachable for whatever that
flag gated — amplifying an unrelated bug for exactly the accounts nobody thought to check. Any
default-on-when-absent flag should be audited as though the gate did not exist at all for every
account that was provisioned outside the normal path.
