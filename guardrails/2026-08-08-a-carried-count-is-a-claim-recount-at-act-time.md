---
title: A count carried in a status note or ledger is a claim, not a fact — re-derive it immediately before the action that depends on it
date: 2026-08-08
category: guardrails
tags: [verify-dont-trust, preflight, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A running status note repeatedly described a small, fixed number of outstanding items waiting on a particular mutating action. Nobody had re-checked that number since the note was first written; it was simply carried forward and repeated in every subsequent summary. When a live, read-only status check was finally run immediately before performing the mutating action, the true count was an order of magnitude larger than what had been carried forward — the note had gone stale the moment new items accumulated after it was written, and nothing had re-validated it since.

Acting on the remembered number would have under-scoped both the action itself and the risk conversation that should have preceded it. The generalizable rule: any quantity that will drive a mutating action — an apply, a migration, a bulk update — must be re-derived from a live, read-only check taken immediately before the mutating step, never trusted from whatever was last written down, no matter how recently or how many times it has been repeated since. This is the same discipline as refusing to act on a stale task premise, applied specifically to counts and scope: a cheap read-only status check right before a mutating command is never optional.
