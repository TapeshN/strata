---
title: A coding agent's fix round reliably introduces a new defect of its own — budget and adversarially review every round, not just the first
date: 2026-07-02
category: orchestration
tags: [model-tier-routing, double-verification, gating, autonomy]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A security fix dispatched to a coding agent took three rounds to land clean. The first round correctly closed every finding from the original review — but introduced a new, different defect in the process (a uniqueness constraint that dropped a scoping field, plus an unrelated functional regression in header handling). The second round fixed those, but needed its own follow-up fix before it was actually clean.

The pattern held across every round: given a precise list of findings to fix, the agent reliably introduced at least one new issue per fix pass rather than converging cleanly in one shot. The new defects were not random — they clustered around the same kinds of surfaces each time (uniqueness/scoping keys, ordering-sensitive configuration), suggesting the model's fix strategy has a structural blind spot rather than an occasional slip.

The generalizable rule: treat every fix round from a coding agent as a new, unreviewed build, not as a diff that only did what the brief said. Budget at least one extra review round beyond what the fix count implies, and make the re-review adversarial — explicitly hunt for the kinds of surfaces a fix is likely to disturb (scoping/uniqueness keys, ordering-dependent config, anything adjacent to what changed) rather than only re-checking the original findings list.
