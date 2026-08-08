---
title: The deployed artifact is the baseline, not any local checkout
date: 2026-08-08
category: guardrails
tags: [deploy, rollback, verification, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A checkout named in a handoff or task description is a claim about a repository's state, not a claim about what is currently running in production. Deploying from a locally-known branch tip can silently overwrite a live deployment that was built from a newer, unlisted branch elsewhere — the deploying agent has no way to know this unless it checks. Two cheap checks prevent it: before any deploy that overwrites a live target, list the platform's own deployment history (creation timestamps, version identifiers) and compare it against your build's base commit — a stale local branch reveals itself immediately as older than what's currently serving traffic; and list all remote branches, not just the ones a handoff mentions, since an unlisted branch is often exactly where the newer work lives.

Equally important: know your deploy platform's rollback mechanism before you need it. Most serverless or edge deploy platforms keep a version history and offer an instant rollback to a prior version. Knowing the exact command in advance turns an accidental overwrite of a live, client-facing surface from an emergency into a one-command fix executed within minutes — verified by a served content marker flipping back to the prior version's.
