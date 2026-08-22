---
title: A command classifier that blocks a compound command carrying one sensitive intent is working as intended — split it and let the human authorize explicitly
date: 2026-08-22
category: guardrails
tags: [harness, gates, autonomy]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Several compound shell commands (stop-then-report-status, pull-then-remove-a-worktree, apply-with-a-production-write-flag) were denied by a permission classifier during an agentic session, while the identical work expressed as single-purpose commands went through cleanly. The one denial that actually mattered — a write against a production data store — was correctly a human decision; surfacing the exact command and letting the operator flip the switch was the right outcome, not a failure of the harness.

The general pattern: a classifier gate that inspects command text works best on one intent per command. When a compound line bundles a sensitive action (a production write, a destructive delete, a merge) together with routine housekeeping, the classifier can only refuse the whole line — which reads as friction, not as the gate doing its job. The fix isn't to fight the classifier; it's to write commands with one intent each, so routine work passes freely and the sensitive intent stands alone where a human decision is actually being requested. Treat a denial on a genuinely sensitive compound command as confirmation the gate is scoped correctly, not as a bug to route around.
