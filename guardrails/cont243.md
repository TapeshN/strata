---
title: "Four attempts to dispatch one batch of reviews, three different contract mismatches, and every one was caught by a gate that failed CLOSED"
date: 2026-09-07
category: guardrails
tags: ["dispatch-contract", "silent-vs-loud-failure", "hitl-partial-preview", "known-bug-cost"]
confidence: learned
source: private-work
---

read the handler's field contract before composing an envelope — `agents/Executor/src/handlers/brief-builder.ts` declares the shape, and one grep would have replaced four round-trips. Keep dispatch context SHORT and put the long method in a PR comment, which has no bridge limit.

note which of these were GOOD. The stale-`dist` refusal, the repo-shape refusal and the HITL length refusal all failed closed and cost only time; the id collision failed OPEN and silently destroyed work. **A gate that refuses loudly is cheap; one that drops input silently is the expensive kind** — and the silent one is the one with an unmerged fix. When a known-bug PR is blocked, ask what that bug is still costing while it waits.
