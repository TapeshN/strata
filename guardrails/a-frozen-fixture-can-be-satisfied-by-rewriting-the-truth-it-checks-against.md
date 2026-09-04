---
title: A frozen fixture can be satisfied by rewriting the truth it's checked against, and a fingerprint gate that only scans tagged regions is blind to anything placed outside them
date: 2026-09-02
category: guardrails
tags: [governance, golden-fixtures, surface-contracts, gate-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Two separate incidents in one review pass showed a governance gate reading green while the thing it was supposed to govern had actually been bypassed — caught only by a human reading the change, not by CI.

First: a change added real functional surface to an area governed by a frozen/golden fixture that explicitly forbids net additions, by hand-editing the frozen fixture itself to match the new state and citing an "escape hatch" that the fixture's own header explicitly rules out. The freeze test stayed green because the truth it compares against had been rewritten to agree with the change — the gate correctly confirmed "nothing changed since the fixture," having missed that the fixture itself was the thing that changed.

Second: a fingerprint-style gate enforcing a declarative contract — verifying that every declared field has a corresponding, governed UI element — only walks specifically tagged regions of the interface. Two new panels, and the declared fields advertising them, passed CI untouched because the panels were placed outside any tagged region the gate actually scans. "The fields are declared and CI is green" was not evidence the fields were governed — only evidence they sat outside the gate's field of view.

General rules: (1) any change that touches a frozen or golden fixture must be evaluated against that fixture's OWN stated rules before trusting the change's justification for touching it — a fixture that can be regenerated to match new behavior has stopped being a freeze. A legitimate capacity increase should go through an explicit, audited, bounded mechanism, never by rewriting the reference truth itself. (2) When a change adds to a declarative contract, verify the corresponding real markup or code actually sits inside the boundary the enforcement mechanism scans — a scanner that only walks tagged regions is blind by construction to anything placed outside them, and "declared plus green" can mean "invisible to the gate," not "covered by it."
