---
title: A merged pull request whose headline change never shipped
date: 2026-08-25
category: infra
tags: [acceptance-criteria, verification, false-merge, gate-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A brief called for a new top-level navigation destination. The pull request was titled after that split, was independently reviewed, was remediated against the review's findings, merged, and deployed. A stakeholder then opened the application and saw the old navigation. Checking the merged trunk afterwards confirmed it: the navigation table still held the single combined entry. The headline change had never existed in the diff at all.

What makes this worth recording is that nothing in the chain malfunctioned. Every check was local and every one of them passed honestly. The diff was reviewed — for audience leakage, tenancy, redirect stubs and dead links, all real concerns, none of them "does the claimed destination exist". The remediation closed the findings it was given; it was never given this one. The tests passed, because the tests had been updated to match what was built rather than what was briefed. The build and deploy were green, because the code compiles perfectly well without the change.

The brief's acceptance criteria did name the outcome. But nothing mechanical ever read the brief. Acceptance criteria that live only in a document are aspirations; the things that actually gate a merge are the tests, and the tests described the implementation.

The rule: a pull request's HEADLINE CLAIM must be pinned by an assertion that fails when the claim is false — not by a review that checks the diff is correct, and not by tests written afterwards to match what was built. When a brief says a destination, a surface or a control will exist, the first commit should be the test asserting it exists, and everything after is making that test pass. Without that, "merged" means "the code that was written is correct", which is a materially different claim from "the thing we asked for is there".

The sharpest form of a more general failure: local correctness was fully verified while the global claim was never checked once. The gap is not carelessness — every actor did their job. It is that no actor's job was the whole.
