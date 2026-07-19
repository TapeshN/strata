---
title: Porting a gate to a NEW sink must copy the sibling's FULL auth+audit+concurrency shape, not just its business rule
date: 2026-07-18
category: guardrails
tags: [security, owasp-a01, owasp-a04, sibling-parity, money-floor]
confidence: learned
source: private-work
---

**Trigger:** an entitlement-cap check was added to a new admin write path by copying the comparator from its canonical sibling. Three independent adversarial reviewers all flagged the same class of gap: the comparator was right, but the scaffolding AROUND it diverged — the sibling's authorization pre-check, its distinct audit-event emission, and its TOCTOU re-check were not carried over.

A mechanical authorization-coverage gate caught the ungated-read facet (the gate worked). The other facets (TOCTOU, audit-distinctness) are not mechanically gated — they need the sibling-parity discipline plus the money/auth double-adversarial-review floor, which caught all of them here. The playbook rule: porting a gate means porting the sibling's FULL shape — auth, audit, and concurrency — not just its comparison.
