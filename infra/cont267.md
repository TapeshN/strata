---
title: "Two sibling PRs hardening the same transition from different bases are a merge-order hazard by construction"
date: 2026-09-12
category: infra
tags: ["sibling-prs", "cas-predicates", "reconciliation-test"]
confidence: learned
source: private-work
---

when retargeting siblings onto one batch, merge-forward the later one ONTO the earlier one's function and add a test that asserts the reconciled predicate; a green suite on either branch alone proves nothing about the merge.
