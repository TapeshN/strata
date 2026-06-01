---
title: Gate your results, not just your inputs — the missing read-only auditor
date: 2026-05-30
category: guardrails
tags: [gating, verify-dont-trust, evals, roles, governance]
confidence: learned
source: private-work
---

A deep audit of a heavily-gated agent workspace found the governance was lopsided: it gated *inputs* (pre-action hooks blocking dangerous edits) but trusted *outputs*. Nothing read a produced artifact — a diff, a PR, a test run, a release — and emitted a typed PASS/WARN/FAIL/SKIP verdict that steered control flow. Every quality decision was a human eyeballing, or an agent asserting "looks good." The single most load-bearing pattern — a read-only judge, separate from the actor, invoked at a named gate — was entirely absent.

Worse, "verify-don't-trust" was missing at the deepest point: planned auto-merge believed "tests pass" rather than independently re-running the verifier and comparing a result certificate. An autonomous loop that trusts its own actor's claims is unsafe to ship.

General lesson: input gates are the easy half. The half that makes autonomy safe is a *results* gate — re-run the check independently, compare, and let a typed verdict (not a vibe) decide what proceeds. A system that gates inputs and trusts outputs has weak governance exactly where it matters most.
