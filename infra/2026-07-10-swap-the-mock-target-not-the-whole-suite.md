---
title: When a mocked function is renamed, swap the mock target — never blanket-replace across the test suite
date: 2026-07-10
category: infra
tags: [testing, mocking, refactoring, access-control, test-fixtures]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When you rename or replace a function that many tests mock (an auth gate, a queue writer, any widely-mocked internal API), the resulting test fallout is predictable and mechanical: re-point each mock's target — module path plus function name — to the new symbol. Do not blanket find-and-replace across the test suite, because some of those tests are intentionally asserting an unrelated code path that still calls the old symbol on purpose, and a blind replace would silently break the thing the test exists to protect.

What happened: a project tightened an access-control gate from a broader "portal access" check to a narrower "owner access" check, and separately swapped a direct write call for a queued-write call as part of a storage migration. Each change broke a batch of test fixtures — three dozen in one case, over a dozen in the other — because the fixtures' mocks still pointed at the old function names. The fix in both cases was the same mechanical move: update the mock target to the new function, leaving any fixture that was correctly scanning for the old symbol on a genuinely unrelated read path untouched. One case also needed a companion fix: a fixture supplying a generic user object needed an explicit elevated-role field added, because the gate now checked for that role specifically, not just presence of a user.

How to apply: when a refactor changes a function's name or call site, treat the test-suite breakage as a triage problem, not a search-and-replace problem. Diff each failing test against the rename to answer one question — is this fixture asserting the code path that changed, or a different path that happens to share the old symbol? Only update mocks in the first group. This preserves tests that exist specifically to catch the old symbol lingering somewhere it shouldn't, which a blanket rename would erase along with the bug it protects against.
