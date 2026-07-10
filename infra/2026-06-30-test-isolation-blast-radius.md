---
title: A mechanical fix's own test suite polluted the production artifact it protected
date: 2026-06-30
category: infra
tags: [test-isolation, side-effects, testing, regression-prevention]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When you add a new side effect (a file write, an API call, a ledger append) to an existing function that already has many callers and many tests, isolate that side effect at the test-module level by default — never rely on each individual test author noticing that a new environment variable or resource now matters.

What happened: a team fixed a staleness bug in a maintenance/close routine by having it also re-stamp a small tracking file. The engineer correctly isolated that new file path in the one new test class written to exercise the fix (pointing it at a throwaway temp path in setUp/tearDown). But the function being modified was called by eight pre-existing test classes that had never heard of this new tracking file, because it didn't exist when they were written — they only isolated the older resource the function used to touch. Once the routine started unconditionally writing the new file, every one of those older tests fell through to the real default path instead of a temp path. The suite was run repeatedly while verifying the fix — locally, across two working copies, before and after merge — and each run appended a fabricated entry to the real production file, which had already been merged. The pollution was discovered only by chance, when a human noticed a stray unexplained entry in the file's tail.

How to apply: when a fix widens what an existing, widely-called function touches, isolate the new resource once at the top of the test file (setUpModule/tearDownModule, a shared fixture, or equivalent) so every test — old and new, present and future — is redirected away from the real resource by default, rather than isolating only in the new test class. Any test that legitimately needs to inspect the real default path should save it, use it, and explicitly restore it afterward. Also re-run the full suite from a clean shell with no leftover exported environment variables, since a previously exported variable can mask exactly this kind of leak.
