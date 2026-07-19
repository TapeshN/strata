---
title: a PR whose check-suite never attaches: fresh-PR fallback, then trigger-test the push path
date: 2026-07-18
category: infra
tags: [github-actions, check-suite, ci-budget-path-filters]
confidence: learned
source: private-work
---

When a PR's required check-suite never attaches (not pending, not red — simply absent), stop waiting: open a FRESH PR to re-trigger suite attachment, then trigger-test the push path itself (an empty-commit push) to prove the webhook flow is alive. An absent suite is indistinguishable from waiting forever — and path-filtered workflows can make "no checks" a legitimate state, so establish which case you are in before you wait on it.
