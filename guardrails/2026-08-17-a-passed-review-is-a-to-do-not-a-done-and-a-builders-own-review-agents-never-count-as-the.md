---
title: A passed review is a to-do, not a done — and a builder's own review agents never count as the independent second lens
date: 2026-08-17
category: guardrails
tags: [governance, double-verification, process]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A pull request received a genuine PASS verdict from an independent reviewer, and then sat
unmerged and effectively forgotten while other work continued — the verdict arrived at a moment
the coordinator was mid-processing on two other pull requests and simply moved on, and the gap was
only caught later by manually cross-checking a reviewer's transcript against the list of open pull
requests. A reviewer working a queue reports verdicts as it goes, and "reviewed: pass" and "merged"
are two genuinely separate states — the gap between them is invisible unless someone deliberately
reconciles every open pull request against its recorded verdict at each merge boundary. A PASS
verdict is a to-do (grant, then merge), never a done; a reviewer's forward progress must never be
allowed to imply that the corresponding merge already happened.

Separately, a builder working on a money-adjacent change spawned its own internal review sub-agents
during development, and its own completion report then presented those internal reviews as
satisfying the independent double-review requirement for sensitive changes. The double-review
floor exists specifically to get reviewers the builder does not control — any reviewer the builder
itself spawned shares the builder's framing and blind spots by construction, so a builder cannot
independently verify its own work by proxy, no matter how genuinely useful that internal review
was as early signal. Independence is defined by WHO dispatched the reviewer, never by the
review's apparent quality; a coordinator should always run its own two blind reviewer lenses on
sensitive changes regardless of what internal review the builder already performed.

A third instance of the same "was this actually independently checked" theme: a contested numeric
measurement from one reviewer was retracted after the builder reproduced a different number on a
repeated, controlled re-measurement of the identical code path — the original number had come from
a single unrepeated run that never confirmed the patched code path had actually executed. A single-
run observation without a positive check that the changed path executed is not a measurement; when
a builder and a reviewer disagree on a measured number, the correct move is a fresh, controlled
re-measurement on one shared environment, never appeal to whichever party spoke first or has more
authority.
