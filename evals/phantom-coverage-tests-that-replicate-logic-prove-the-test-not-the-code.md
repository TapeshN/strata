---
title: Phantom coverage — tests that replicate production logic prove the test, not the code
date: 2026-06-10
category: evals
tags: [evals, determinism, verify-dont-trust, gating]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A test suite can read green while providing no protection against the mutation it claims to guard. This happens when a test re-implements the production rule inline — duplicating the logic in the test body rather than importing and driving the real unit — so that any change to the production rule produces a green test that is now testing a different, independently-maintained copy of the rule.

A concrete pattern: route-dispatch tests evaluated a fallback model and a lane-cap comparison by writing those expressions directly into the test body, because the function under test was not exported. Thirteen tests passed. Two production mutations — changing the fallback model string and changing the cap comparison operand — survived all thirteen without a red. The suite was validating its own copy of the logic, not the production code.

Detection is the mutation protocol: introduce a deliberate break in the production code and demand that a test fail. If no test fails, the suite does not protect against that mutation. Each production rule that test assertions parallel should have a mutation-trigger proof.

The structural fix is dependency inversion: export or inject the unit being tested, and drive the real production path in the test. A test that cannot reach the production code through a named interface is not testing that code.

Two related failure modes worth naming alongside this:

- **Replicated enumerations**: a test that maintains its own list of valid values parallel to a production list will silently fall out of sync when the production list is extended. Drive the test from the production list, not a duplicate.
- **Inlined thresholds**: a budget or limit test that hardcodes the threshold value in the test body will not catch a regression that changes the production threshold to a different hardcoded value. The test must derive the threshold from the production source or accept both as parameters and assert the relationship.

The common thread: a test that knows the answer independently of the code under test is not a test of the code.
