---
title: Shipping user-facing error masking in the same change as an unverified fix hides your own diagnostic signal
date: 2026-07-14
category: guardrails
tags: [determinism, gating, verify-first, observability, diagnosis]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A single change bundled two things together: a friendly error message that replaced a raw failure in the user interface, and an underlying database fix that turned out to be silently ineffective (it targeted the wrong object and no-opped). Because both landed in the same change, the friendly message masked the fact that the real failure was still happening — the server log, the one place that could have shown it, recorded only the bland user-facing string with no discriminating detail, and one error branch logged nothing at all. Diagnosing the actual problem afterward required production build logs and direct database access rather than anything visible through the application.

It got worse before it got better: the test suite for that same change asserted that the log call was made with exactly that one bland string — which meant the test would have failed the moment someone tried to add the missing diagnostic detail, effectively locking in the undiagnosable behavior as "correct."

Three rules follow. Land a fix verified-first; add user-facing error masking only after the underlying fix is confirmed to actually work, never in the same change as an unverified attempt. A masked user-facing error must still log a safe discriminator on the server side — an error category, an error code, the name of the constraint or field involved — never the raw message, query, or connection details, since server logs must not become a channel that leaks one tenant's data to another. And treat a test that asserts "this logs nothing distinguishing" as itself asserting a defect, not a passing spec.
