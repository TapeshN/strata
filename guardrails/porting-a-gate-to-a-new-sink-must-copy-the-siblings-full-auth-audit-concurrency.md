---
title: Porting a gate to a NEW sink must copy the sibling's FULL auth+audit+concurrency shape, not just its business rule
date: 2026-07-18
category: guardrails
tags: [security, owasp-a01, owasp-a04, sibling-parity, money-floor., **Mirror:**]
confidence: learned
source: private-work
---

**Trigger:** Batch G G4 — I added the free-version cap check to `adminCreateIteration` by copying the comparator from the canonical `adminGenerateRevision` (`freeVersionsUsed >= freeVersionsAllowed`). Three independent adversarial reviewers ALL flagged the same class of gap: the comparator was right, but the scaffolding AROUND it diverged.

the mechanical `admin-grants-scope-coverage` test already catches the ungated-read facet (it fired here — the gate worked). The other facets (TOCTOU, audit-distinctness) are NOT mechanically gated → they need the sibling-parity discipline + the money/auth double-adversarial-review floor (which caught all of them here). Healed `prompts/loop-orchestration.md`.
