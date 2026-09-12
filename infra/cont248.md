---
title: "A CI red had two causes. I found one, fixed it, and told three workers the red was explained"
date: 2026-09-09
category: infra
tags: ["two-causes-one-fix", "skipped-is-not-success", "positive-control-on-green-history", "converging-workers-are-evidence", "overruled-them-on-partial-truth"]
confidence: learned
source: private-work
---

a green history is not evidence until you confirm the job RAN. `gh run view <id> --json jobs` and read `conclusion`, because `skipped` and `success` are both "not a failure" and only one of them means anything.

when several independent workers converge on the same cause, that is data. I treated their agreement as a shared misreading because I had found *a* real bug — but finding a true cause is not the same as finding the only one. **Say "this explains part of it" until the check is green, not "this explains it" because the check changed.**
