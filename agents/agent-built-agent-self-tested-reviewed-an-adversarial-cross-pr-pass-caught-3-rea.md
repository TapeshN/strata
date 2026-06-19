---
title: Agent-built + agent-self-tested ≠ reviewed: an adversarial cross-PR pass caught 3 real bugs every local gate passed
date: 2026-06-16
category: agents
tags: [[adversarial-review], [self-test-isnt-review], [billing-correctness], [access-control], [webhook-retry], [review-before-merge]]
confidence: learned
source: private-work
---

no agent-built PR merges on its own green gates alone — an INDEPENDENT adversarial review (separate agent, "hunt for bugs", cite file:line, lens on cost/auth/error-paths) is mandatory before merge, especially for anything touching money, auth, or a ledger.
