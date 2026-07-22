---
title: "Build-ahead, hold-merge: when work depends on an unresolved external answer, build and preview at full speed but never merge past it"
date: 2026-07-20
category: orchestration
tags: [coordinator, decision-tracking, external-dependencies, release]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Work proceeded on a whole content/direction pivot and was merged and deployed the same day an internal stakeholder was enthusiastic to ship — while the actual external conversation that the direction depended on ("does this stay the primary surface, or does something else take over") was still unresolved. The external answer landed hours later and it was the opposite of the assumption baked into the merge, forcing a section-level rework. The root cause: the open question HAD been named out loud at planning time, but naming a fork isn't the same as resolving it — internal enthusiasm to ship was mistaken for the external party's actual answer.

**The rule:** when a piece of work's direction depends on an answer only an external party can give, build and preview it at full speed (nothing is lost by having it ready), but treat merge/publish/deploy/send as gated on that specific external answer, tagged explicitly with who is expected to answer and by when. Release only once the answer actually arrives — matching, contradicting (convert and salvage what's still durable), or via an explicit, recorded override that accepts the rework risk. Never let a named-but-unresolved fork merge by default or by momentum. As a side effect, keep genuinely durable underlying work (data models, content inventories, non-surface-level assets) separable from the surface-level work that depends on the pending answer, since the durable layer usually survives a pivot intact even when the surface has to be reworked.
