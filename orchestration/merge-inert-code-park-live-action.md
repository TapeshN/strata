---
title: Merge inert code with CI green; park the live irreversible action as an operator handback
date: 2026-06-07
category: orchestration
tags: [hitl, autonomy, gating, release]
confidence: learned
source: private-work
---

Code that performs an external side effect (posting to a service, creating a resource, installing a cron job) can be verified in tests using in-memory mocks or stub clients. Once the tests pass, the inert code can merge with CI green. The live side effect — which requires a real credential and is irreversible — is held as an operator handback: a single documented command the operator runs when ready.

This separates what can be verified (the code's logic, thoroughly tested against mocks) from what is irreversible (the external call). It allows the code to ship while the operator retains control over the live action.

General lesson: the pattern for external-side-effect lanes is: build the inert code → verify against mocks → merge green → park the live action as a named operator command. Never auto-execute the live action; the code merging is not the same as the action happening.
