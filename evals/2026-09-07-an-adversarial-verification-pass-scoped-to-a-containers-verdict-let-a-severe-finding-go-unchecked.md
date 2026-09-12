---
title: An adversarial verification pass scoped to a container's overall verdict let a severe finding inside a mildly-labeled container go unchecked
date: 2026-09-07
category: evals
tags: [fanout-design, verification-grain, asymmetric-repair, overclaim-correction]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A large multi-item audit asked, for each item, "would acting on this undo already-shipped work?" — with an adversarial second pass on every risky flag, because a false "this would undo real work" flag can retire genuinely good work for no reason. The summary reported that every flagged item had been checked and none actually would undo shipped work. That summary was wrong: the pipeline routed items to the adversarial pass based on each container's overall verdict, not on the individual finding inside it — so a real "would-undo-shipped-work" problem sitting inside a container whose overall verdict was something milder was never sent to the adversarial pass at all. One of the missed cases: a refresh routine would have overwritten the only copy of a large amount of real production data, and the guard meant to prevent that couldn't fire because it compared build freshness while the source and the target were, in that case, the same build.

The fix at the source: in any pipeline that classifies first and verifies second, route to verification at the grain of the individual finding, not the grain of the container's summary label — a severe finding can ride inside a mild verdict and disappear from view if the routing only looks at the outside of the box.

A useful asymmetry falls out of the repair, worth keeping as its own rule: adding a safeguard to a plan is cheap even when the underlying concern turns out to be overstated, but removing or retiring a safeguard is not — that is exactly the action a false positive would wrongly recommend. When a verification budget runs out partway through, apply the safe, additive response to everything left unverified, rather than the unsafe, subtractive response to only the subset that was actually checked.
