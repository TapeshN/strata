---
title: A workflow lane that "failed" may have ALREADY pushed a PR → duplicate + conflict on re-run
date: 2026-06-16
category: orchestration
tags: [orchestration, workflows, idempotency, duplicates, merge-hygiene]
confidence: learned
source: private-work
---

in any merge/drain, survey ALL open PRs first (not just the ones you think you created). Treat a transient-erroring lane as "may have partial side-effects", not "no-op".
