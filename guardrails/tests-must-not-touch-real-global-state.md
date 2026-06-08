---
title: Tests with global side effects must isolate them to a temp location and assert the real path is untouched
date: 2026-06-03
category: guardrails
tags: [isolation, determinism, reproducibility, gating]
confidence: learned
source: private-work
---

A test that exercises a component with global side effects must redirect those side effects to a temporary, isolated location — never to the real global path. If the real path is written by a test (for example, writing a halt file to the actual fleet-wide stop location), any process that reads that path afterward will be affected, potentially freezing unrelated sessions.

The fix requires two parts: redirect the side effect to a tempdir via an environment variable or parameter override, and add an assertion that the real path was NOT modified. The redirect alone is insufficient — if the redirect silently fails, the test still passes while the real path is contaminated.

General lesson: the non-contamination assertion is as important as the redirect. A test that only redirects can re-introduce the contamination silently if the redirect mechanism breaks. Both checks are required.
