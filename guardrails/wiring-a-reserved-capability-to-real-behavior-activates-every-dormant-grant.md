---
title: Wiring a previously-reserved, no-op capability flag to real behavior instantly activates every dormant grant that was ever set while it was inert
date: 2026-07-14
category: guardrails
tags: [access-control, rollout, dormant-state, privilege-escalation, review-blind-spot]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A capability flag existed in an admin-facing permission editor for a long time as a documented no-op — selectable and storable, but not wired to any actual behavior. A later change gave that flag its first real consumer (a read it now gates). A code-level security review of the diff looked clean, because the new enforcement path itself was correctly scoped — but any account that had ever had the flag ticked while it was inert would silently gain the new capability the moment the change deployed, with no new action taken by anyone and nothing visible in the code diff itself.

The general rule: before deploying code that gives a previously-inert flag, capability, or config value its first real consumer, audit the LIVE rows already holding that flag or value — not just the code path that newly reads it — and explicitly decide whether each existing holder should keep it or be revoked and re-granted deliberately. A review of the code diff alone structurally cannot see this hazard, because it lives in already-stored state, not in the changed lines. This is the inverse of a feature shipping "wired but not working" — here the danger is a capability that was mintable all along but unwired, a loaded spring that fires the instant it's connected.
