---
title: A refresh or copy-change request does not license adjacent system-level aesthetic changes — scope edits to the explicit ask and land system changes separately
date: 2026-06-29
category: orchestration
tags: [autonomy, hitl, docs]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When an operator asks for a copy, brand, or content refresh, the scope is the explicit ask — not any adjacent system-level change (typography system, color tokens, spacing primitives) that could also be improved at the same time. Bundling a high-blast-radius aesthetic-system change into a copy request overrides an existing deliberate system the operator may like and cannot review without having the diff called out separately.

The pattern that makes scope creep invisible is that the change is "obviously better" from the agent's perspective, and taste or aesthetic calls are otherwise in the agent's purview. The distinction is: micro-level taste choices on the items explicitly requested are the agent's to make; system-level changes that apply globally and replace a prior deliberate decision require an explicit proposal and confirmation.

The practical heuristic: if reverting the change would require touching files that the explicit ask did not touch, it is a system-level change and belongs in a separate, labeled step — not bundled into the ask's commit.

An additional property enables a clean revert: any system-level aesthetic change should be landed as its own isolated step (a separate commit, a separate replacement pass) rather than hand-applied inline per element. Isolation makes the revert surgical. When it is not isolated, the revert drags content changes with it.
