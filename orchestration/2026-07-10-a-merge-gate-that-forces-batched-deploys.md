---
title: A merge gate that forces batched deploys instead of one-per-commit
date: 2026-07-10
category: orchestration
tags: [ci-cd, deploy-cost, merge-gates, batching, migrations]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

**The rule:** when a repo auto-deploys to production on every merge to its main branch, put a merge gate in front of main that blocks a solo, ad-hoc merge unless the branch or PR is explicitly labeled as a release/batch. That single mechanical constraint forces engineers to assemble small, file-disjoint feature branches into one integration branch, get one green CI run across the whole batch, and land one production deploy — instead of many tiny deploys, one per commit.

**What happened:** a team had unlimited deploys-on-merge to a production app, which meant every small fix triggered its own full CI run and its own production deploy — burning CI minutes and deploy slots on work that could have shipped together. They added a gate that refuses a merge into the deploy-triggering branch unless the branch name or PR carries an explicit "batch"/"release" marker. To merge at all, engineers now have to combine several feature branches that touch disjoint files into one integration branch (a clean, conflict-free merge is itself proof the branches don't overlap), open a single labeled pull request, and let CI verify the combined batch once. As a side benefit, if that batch includes an additive-only database migration that runs automatically at deploy time before the build, a green production deploy becomes proof the migration applied cleanly — because a failed migration fails the build, and a failed build never deploys.

**How to apply:** if your infrastructure auto-deploys on merge and you're paying per-deploy or per-CI-run, don't rely on discipline to keep merges batched — encode it as a gate that literally can't be satisfied by a lone small PR. Require a label or branch-prefix convention that only makes sense for genuine multi-change batches, and let the label do double duty: it forces batch assembly, and it becomes an honest record that the merge really was a coordinated release rather than a bypass of the cost control. Pair it with a deploy-time step (migration, schema check, smoke test) that fails the build on error, so "deploy succeeded" is itself a verified claim, not an assumption.
