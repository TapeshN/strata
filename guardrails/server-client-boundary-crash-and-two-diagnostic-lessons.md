---
title: A new green-locally, crashes-in-production class — calling a client-module export from server code
date: 2026-07-16
category: guardrails
tags: [testing, layering, boundaries, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

In frameworks that support a "server component" / "client component" split (code explicitly marked as client-only versus code that renders on the server), EVERY export of a module marked client-only becomes a client reference at build time — including plain, pure helper functions that have nothing to do with rendering. A server-rendered page that imports and directly CALLS one of those exports (rather than rendering it as a component) throws a runtime error the moment that code path executes, because the framework has replaced the export with a reference meant only to be invoked from the client. This is invisible to type-checking, unit tests, and a production build, because none of those actually render a dynamic, auth-gated page the way a real request does — so the bug can ship, sit latent for weeks, and only surface when a real user hits the exact page. The fix is structural: any pure function needed by both a server page and a client component must live in its own server-safe module (no client marker) that both sides import — never export a plain helper from a client-marked file and call it from server code.

Two diagnostic lessons from tracking this down, both broader than the specific bug:

**An audit that comes back all-clear while the system is live-failing is a clue that the hypothesis is wrong, not that the bug is fixed.** A fanned-out audit checking many similar code paths for one specific hypothesized failure mode (a null-dereference on sparse data) returned "safe" on every path — including the exact path that was actively crashing in production. That contradiction should be read as evidence the audit tested the wrong theory, not as an all-clear; re-probing with a different, well-formed input reframed the bug as a completely different, more universal class. Don't let a clean audit of the WRONG hypothesis close out a live, reproducing bug.

**When changing behavior shared by multiple test files, run the exact test-discovery command CI runs — not just the one file that seems obviously related.** A scoped local test run targeting the file that seemed most directly relevant passed cleanly, but CI's broader auto-discovery command (which walks an entire test directory rather than one named file) caught a SECOND file that also asserted on the old behavior and had gone untouched. The fix: either grep for every test that exercises the changed symbol/behavior before declaring done, or simply run the identical discovery command CI uses, locally, rather than a manually-scoped subset.
