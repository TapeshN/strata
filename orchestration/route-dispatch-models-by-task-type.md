---
title: Route dispatched coding-agent models by task type, not a single default — completeness-critical security work needs a stronger model
date: 2026-07-18
category: orchestration
tags: [subagents, roles, autonomy, cost]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A single default model applied uniformly across all dispatched coding-agent tasks (chosen mainly for cost reasons) produced a fix that closed only 2 of 4 structurally-identical sites needing the same auth-hardening change — the model was solid on the sites it happened to touch first and simply incomplete on generalizing the pattern to every remaining instance, even when nothing about those remaining sites was hidden or obscure. A second, independent adversarial review of the fix caught the gap by name — both reviewers flagged the same missed sites.

**The general lesson: not every dispatched task should route to the same default model.** A cheaper, faster default model is a reasonable choice for mechanical, narrowly-scoped work, but security-completeness-critical tasks — anything of the shape "apply this fix everywhere the pattern occurs," or anything where an incomplete fix is worse than no fix (a false sense of closure) — should route to a stronger model by default, not as an escalation after a first attempt already shipped incomplete. Re-dispatching the identical task to a stronger model, with no other change, closed all remaining sites and added a structural test enumerating every site so a future regression or a newly-added site fails the build automatically rather than depending on a human noticing.

**Practical routing heuristic:** classify dispatched work by shape — security- or completeness-critical work routes to the strongest available model; purely visual/design work routes to a model tuned for that; mechanical, narrowly-scoped changes can use a cheaper default — rather than letting cost pressure collapse all task shapes onto one model tier. Keep an explicit allow-list of which stronger models are opt-in for which task shapes, so an unlisted or unrecognized model identifier fails closed to the cheap default rather than silently escalating to an expensive one.
