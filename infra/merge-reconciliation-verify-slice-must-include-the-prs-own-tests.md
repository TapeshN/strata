---
title: merge-reconciliation verify slice must include the PR's OWN tests
date: 2026-07-18
category: infra
tags: [merge-drift, test-slice, mocks]
confidence: learned
source: private-work
---

When reconciling a branch into a moved main (merge trains, conflict resolution), the post-merge verification slice must include the PR's OWN tests — not just the repo's headline suite. Reconciliation can silently dilute the PR's specific assertions (mock drift, a transaction wrapper swallowing a call) while the global suite stays green; the PR's own tests are the only witness bound to that PR's intent.
