---
title: A deadline guarding one hop of a fail-closed path leaves sibling hops exposed
date: 2026-07-16
category: guardrails
tags: [deadline, fail-closed, concurrency, cost]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A fix added a short deadline to the read step of a fail-closed spend-limiting path — the step that checks current usage before allowing an expensive downstream call. The same change also introduced several write steps further down the same path: a conditional update that atomically claims the spend, a batch insert, and an event write, all awaited with no deadline of their own. Under the exact concurrent-burst scenario the atomic claim exists to handle, one of those write steps can queue behind a database row lock indefinitely — so the request hangs and eventually times out at the outermost layer instead of failing closed quickly. The step that got the deadline was, ironically, the one least likely to contend; the step actually vulnerable to contention was left bare.

The general rule: a deadline added to make a path fail closed only holds if every I/O call in that path — including calls inside error-handling branches — carries its own bound. Adding a timeout to the first hop a reviewer happens to look at, without auditing the full call graph the request traverses, produces a guarantee that looks complete but silently excludes exactly the hop most likely to be slow under the load the fix was meant to survive. Before declaring a path fail-closed, enumerate every awaited call between the entry point and the response, not just the one that prompted the fix.
