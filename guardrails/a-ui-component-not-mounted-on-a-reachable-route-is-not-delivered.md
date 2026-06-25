---
title: A UI component not mounted on any reachable route is not delivered, regardless of how complete its implementation is
date: 2026-06-24
category: guardrails
tags: [lifecycle, verify-dont-trust, ci, gating]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A UI component can be fully implemented, have passing tests, pass every CI gate, and appear complete in a code review — and still be entirely invisible to any user navigating the application, because it was never imported or rendered on a reachable route.

The diff and the test suite both read as complete. The gap is undetectable from code review alone because the component definition file and its test file both exist and reference it. Only the application's route tree, not the component file itself, can tell you whether the feature is actually accessible.

The verify-tail for any new UI component is: search for the component's import across the application's page and layout tree. If the only files referencing it are its own definition and its own test, the component is orphaned and the feature has not shipped.

The live traversal check — navigating the real running application as an authenticated user, following the flows the feature is supposed to support — is the reliable catch for this class of gap. Static review and test coverage cannot substitute for it because neither requires the feature to actually appear on a rendered page.
