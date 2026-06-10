---
title: A judge fed only scalar deltas cannot credit qualitative progress — feed it the evidence
date: 2026-06-10
category: evals
tags: [llm-judge, instrumentation, measure-dont-assume]
confidence: learned
source: private-work
---

An LLM judge scoring progress saw only scalar inputs: a maturity score that was never re-scored, eval scores already saturated at their ceiling, and a small row-count delta. It graded a genuinely milestone wave as a failure on the goal-progress axis — and was right to, given its inputs. The qualitative win (a feedback loop closing end-to-end for the first time) was simply invisible in the numbers it was shown.

This is the meter working as designed: it refused to credit progress it could not see, and thereby exposed an instrumentation gap rather than a progress gap. The wrong response is to override the judge; the right response is to widen its evidence. Feed judges the actual artifacts — diffs, merged changes, run outputs — alongside the scalar deltas, and re-score any stale upstream number that feeds them, or the judge inherits its staleness. A separate trap in the same incident: the meter printed a trailing log line after its JSON output, breaking downstream parsing — machine-readable output must be emitted clean.
