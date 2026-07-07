---
title: A real first-time human user catches information-architecture and terminology defects that no amount of the agent's own traversal testing surfaces
date: 2026-07-06
category: evals
tags: [real-user-test, naive-user, ia-terminology, first-run, empty-state]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An agent that traverses a freshly-shipped, entered/authenticated product experience end to end — clicking through every page, exercising the actual logged-in flow rather than just the marketing front door — can still come away reporting everything is fine while real defects remain completely invisible to it. In one case, a product surface went fully live, was traversed thoroughly by the building agent, and read as clean. Within minutes, a genuine first-time, non-technical user surfaced multiple real problems: a returning user being shown a card referencing a feature before any of its prerequisite data existed; two different labels in the product meaning the same thing to a user despite being built as separate surfaces; internal jargon surviving into user-facing copy; unintuitive navigation; and a piece of state silently disappearing on navigation.

The reason an agent's own traversal misses this class of defect is structural: the agent already knows the product's internal model, so it reads labels and flows as correct because it understands the intent behind them. A first-time user has no such context and reads everything cold. The general lesson: for any client-facing surface, a real first-time-user test — or, failing that, an explicit simulation of one, deliberately reading every label and flow as someone who has never seen the product before, starting from a genuinely empty first-run state — is its own distinct verification tier that must be budgeted separately from the agent's own traversal. Terminology, information architecture, first-run coherence, and empty-state handling deserve first-class treatment as review dimensions in their own right, not as a byproduct of a functional walkthrough.
