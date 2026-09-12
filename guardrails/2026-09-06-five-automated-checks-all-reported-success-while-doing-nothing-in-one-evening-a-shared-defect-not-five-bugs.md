---
title: Five automated checks all reported success while doing nothing, in one evening — a shared defect, not five separate bugs
date: 2026-09-06
category: guardrails
tags: [negative-control, gate-scope-vs-claim, silent-no-op]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A single mild question about work volume, followed downstream, turned up five unrelated automated mechanisms that each silently did nothing while reporting success: a status-tracking script whose "ready" condition never actually inspected build or check results, so it called a conflicted item with failing checks "ready," and kept re-announcing the same item because its dedup key changed on every push; a paging/escalation script that read one environment setting when the host only ever set a differently-named one, so it logged "not run" and returned success; a documentation-pointer check that reported PASS against a target that had never existed; a safety gate whose own documentation claimed it covered every code path, when its enforcement mechanism structurally cannot see a scheduled or background job at all; and a periodic summary that reported "0 days waiting" in every row because its own trigger window was far shorter than the unit it was measuring in.

The shared shape: a mechanism whose real behavior and its stated behavior had quietly diverged, invisible to every happy-path test, because the happy path is exactly the part that still worked. The only thing that surfaces this is a genuine negative control — deliberately make the input wrong in the way the mechanism is supposed to catch, and confirm it actually notices. A documentation check against a target that doesn't exist, a "ready" verdict on a conflicted item, a page with no valid recipient — each was one deliberately-broken input away from being obvious.

The rule that falls out: a check that cannot run must never report PASS — it must report SKIP or WARN and name what went unverified. Two concrete instances the same evening: a type-check run inside a workspace copy with no installed dependency directory quietly executed a placebo package and printed zero errors, which would have shipped an unverified change as "verified"; a separately-written gate for a different problem was deliberately built to WARN, never PASS, on the same class of "cannot actually check" condition, and that one behaved correctly. Worth banking on its own: a sentence in a governing document asserting a gate's scope is itself a claim that needs the same evidence as code, not narrative trust — checked against a hostile case, it was false for exactly the situation it claimed to cover.
