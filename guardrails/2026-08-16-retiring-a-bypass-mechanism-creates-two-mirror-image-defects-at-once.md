---
title: Retiring a bypass mechanism creates two mirror-image defects at once
date: 2026-08-16
category: guardrails
tags: [gating, contracts, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a system that has a "skip/bypass" escape hatch on some gated milestone is later
hardened so that milestone must be reached through a real, non-bypassed event, two
opposite defects can appear at once, and fixing one exposes the other. On one side, a
row that reached the old bypassed state before the hardening lands can still silently
satisfy the new gate if the gate checks status alone and never inspects the flag that
produced it. On the other side, a row that legitimately reached the threshold through a
path that emits no gating event at all — a batch import, a manual correction, a state
seeded directly rather than produced through the normal flow — gets newly and wrongly
stranded below the bar the moment the bypass escape hatch is retired.

The fix that closes both sides at once is a single derived fact computed from BOTH a
genuine (non-bypassed) qualifying event AND the real threshold being met — never
satisfied by either alone. A bypassed-only row leaves the derived fact unset
(recoverable, correctly not-satisfied); a threshold-met-but-eventless row also leaves it
unset (recoverable, not silently stranded) until it is reconciled through the real path.

The generalizable point: retiring any bypass/skip escape hatch is a two-sided audit, not
a one-line change. It requires grepping every reader of the old bypass flag to confirm
none of them can be satisfied by a stale bypassed row under the new rule, AND
enumerating every path that can reach the gated state without going through the event
the new gate expects, so those paths get reconciled rather than orphaned. A single
reviewer tends to catch only one side; a milestone that touches money or eligibility is
worth two independent passes for exactly this reason.
