---
title: A substring-based source-assertion test can fail because a code comment, not the code itself, contains the searched text
date: 2026-07-01
category: evals
tags: [testing, determinism, contracts]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A regression test asserted that one function call occurs earlier in a file's text than a second, sibling function call — a common pattern for verifying call-order without needing a full runtime harness. The test failed even though the real call order in the code was correct, because a prose comment elsewhere in the same function — written to explain a design decision in plain English, and mentioning the sibling function's name — contained the literal substring being searched for, positioned earlier in the file than the real call. A plain substring search has no concept of "inside a comment versus inside executable code"; it simply finds the first textual occurrence.

The general trap: any source-assertion test that searches for a function or identifier name as a plain substring is vulnerable to the file's own comments, not just its code — a comment written for a human reader that happens to name a sibling function can silently break an ordering or position assertion, and this includes comments the same author writes while making the very change the test is meant to verify.

Two mitigations, either sufficient on their own: avoid naming other functions in prose comments placed near code that an ordering-sensitive test inspects; or make the text-extraction step comment-aware (strip comment lines before searching) if a codebase's comment density near sensitive code makes the first option impractical. This is worth calling out explicitly to whoever authors this class of test, since the failure mode is easy to reintroduce by habit.
