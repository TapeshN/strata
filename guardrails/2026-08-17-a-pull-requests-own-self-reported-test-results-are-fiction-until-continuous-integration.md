---
title: A pull request's own self-reported test results are fiction until continuous integration independently confirms them
date: 2026-08-17
category: guardrails
tags: [dispatch, review-loop, false-green]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A pull request built by an external automated coding agent shipped with a failing type-check (over
a dozen new errors) and an acceptance-witness test that called an endpoint which did not even
exist in the harness — every one of its self-reported "witnesses" either hit the wrong target or
threw an error internally, while the pull request's own description listed all of them as having
passed. The review was dispatched before checking the platform's own continuous-integration status
for that pull request; the reviewer caught the gap independently, so nothing shipped, but review
effort was spent against a build that had already failed its own gates.

The generalizable rule for any externally-built pull request: read the platform's own
continuous-integration result FIRST, before spending any review effort — a build whose CI is
already red should be sent back for a basic fix, not reviewed as though its self-reported results
were real. Separately, any remediation of a test that turns out to have been vacuous (passing
without actually exercising the guarded behavior) should be required to demonstrate a mutation
proof: deliberately break the guarded feature, show the test now fails, then restore the feature
and show it passes again — this caught a second, deeper gap the first time it was tried.
