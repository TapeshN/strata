---
title: A "read must not write" regression guard is only real if its setup reaches the state where the write would actually fire
category: journal
date: 2026-08-22
tags: [tests]
confidence: learned
source: private-work
---

A regression test existed to guard against a GET/read endpoint having an unintended side-effect write. The test's setup never advanced the clock to the point where the underlying condition that would trigger the write becomes true — so when an unrelated fix restored the offending write path, the test found nothing due yet, ran cleanly, and reported green. The recurrence happened inside the very pull request meant to close out the original defect.

General rule: a "this operation must not mutate state" regression guard needs to actually place the system in the state where the mutation would fire if the bug were present — moving a simulated clock forward, seeding a due record, whatever the trigger condition requires — not merely call the operation and check nothing changed in a state where nothing was going to change anyway. As a reviewer discipline: deliberately restore the original defect and confirm the guard goes red before trusting that it protects anything; a comment asserting "this would be due after the change" is not the same as the test actually reaching that state.
