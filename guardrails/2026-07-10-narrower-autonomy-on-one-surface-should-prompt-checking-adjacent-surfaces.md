---
title: A narrower autonomy grant on one surface should prompt checking whether it generalizes to adjacent surfaces
date: 2026-07-10
category: guardrails
tags: [autonomy, hitl, operator-gate]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When an operator narrows a previously-standing autonomy grant for one specific class of action (for example: "from now on, get my visual sign-off before shipping anything user-facing"), the natural failure mode is to interpret the narrowing literally and keep exercising the old, broader authority on everything that isn't explicitly named. In one case an agent kept auto-merging changes that had no visual component under an old blanket merge-authority grant, reasoning that a new visual-approval requirement only applied to visual changes — while the operator's actual intent was a general tightening of delegation, not a narrow carve-out.

The generalizable rule: when an operator revokes or narrows autonomy on any one surface, treat that as a signal to re-examine every adjacent surface where you're still operating under the old, broader grant — ask, or default conservatively, rather than continuing to exercise it until told a second time. A standing autonomy grant should be revisited holistically whenever any part of it changes, not treated as a set of independent per-surface permissions that only shrink exactly where explicitly named.
