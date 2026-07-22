---
title: Trigger-test the consume half of a queue, not just the enqueue half
date: 2026-07-19
category: guardrails
tags: [gating, queue, ci, testing]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A retry/drain queue had two code paths reading it: one mode consulted a cached verdict and reported "ready to proceed," the other mode ignored that same cache and re-queued the same items every time it ran. Every existing test exercised only the enqueue side — item goes in, item is present — so the queue always looked healthy while one of its two consumers silently never drained it.

The general failure class: a queue (or any shared state two different code paths read) can pass every test that only proves items go IN, while the path that's supposed to take them OUT never actually does. A green enqueue test says nothing about whether the consumer half will ever fire.

**The rule:** write the trigger-test around the full round-trip a queued item is meant to complete — enqueue → the specific consuming code path → the expected terminal state — not just "the item appears in the queue." Run it against every consuming mode/path that reads the same queue, and make it red-witnessed on the unpatched behavior before trusting the green.
