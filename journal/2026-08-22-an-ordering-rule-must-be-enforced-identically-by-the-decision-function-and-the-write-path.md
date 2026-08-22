---
title: An ordering/precedence rule must be enforced identically by the function that decides the winner and by the write path beneath it
date: 2026-08-22
category: journal
tags: [money, tests]
confidence: learned
source: private-work
---

A review round added a comparator function to decide which of two competing pending changes should win when both apply to the same record, and wired it into the approve/move/apply paths. An independent follow-up review found that after the comparator correctly picked the higher-value change as the winner, the write path underneath it used a guard clause that expected a specific prior state to already be cleared — and because the losing, earlier change hadn't cleared that state, the guard matched nothing and silently re-marked the actual winner as skipped instead. The record ended up on the losing value, a different flavor of the same underlying bug class the comparator was built to fix, just relocated one layer down.

General rule: for any "X beats Y" precedence rule that spans a decision function and a separate write/apply step, the test matrix needs both possible input orders crossed with both possible outcomes, and the write path itself must actively supersede a losing incumbent — never merely refuse because a slot looks already occupied. A guard clause written for one call order can silently invert the very rule sitting next to it.
