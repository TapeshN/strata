---
title: A test can pin a defect as the contract — then fixing the defect makes the test look like the regression
date: 2026-07-30
category: evals
tags: [evals, determinism]
confidence: learned
source: private-work
implementation_target: shared-prompts
efficacy: decorative
---

Twice in one work session, an existing test turned out to be asserting the exact broken behavior a user had reported as a bug — one test asserted that a particular fallback mechanism fired before another one, encoding the wrong order as the intended contract; another asserted the presence of an error state that was itself the reported defect. Both tests were green before the fix, and both went red the moment the actual bug got fixed — reading, on the surface, exactly like a regression.

The pattern: each test had been written at a time when the buggy behavior was the shipped behavior, and each described a mechanism ("does X before Y," "shows this specific state") rather than a user-visible guarantee. A mechanism-level assertion structurally cannot distinguish "this is how it's supposed to work" from "this is merely how it currently happens to work," so it quietly becomes a ratchet that holds a known defect in place. The fix is to rewrite such tests to assert the user-visible guarantee instead of the internal mechanism, and to treat a test that goes red exactly when a reported bug gets fixed as evidence you found the right code — read it, confirm it was pinning the old, wrong behavior, and rewrite it in the same pass rather than either ignoring the red or deleting the coverage outright.
