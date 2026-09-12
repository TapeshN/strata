---
title: Two checks read green while each was quietly measuring the wrong thing
date: 2026-09-09
category: guardrails
tags: [lookahead-backtracking, scoped-gate-that-did-nothing, worktree-resolves-to-primary, positive-control, make-it-fail-first]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A scoping fix for a source-pattern gate used a negative lookahead intended to exempt one specific, correct call shape (a call that properly delegates a decision to an authorizing helper) from a rule that otherwise flags a broader dangerous shape. The exemption still fired on the correct shape anyway. The bug was in exactly where a whitespace token sat relative to the lookahead: written with the optional whitespace outside the lookahead, the lookahead itself matched zero characters and then ran from a position where the helper's name wasn't present, so it "succeeded" at rejecting the exemption instead of granting it. A scoping change that silently does nothing is worse than skipping the change entirely, because it now reads in every report as "handled."

Separately, setting up a real compiler/type-check pass inside a second working copy of a project — by symlinking that copy's shared internal package back to the same dependency the main copy uses, to avoid a slow reinstall — resulted in the type-checker resolving that symlink back to the original copy's version of the shared package, not the new copy's own edited version. The check reported clean and would have kept reporting clean for edits it structurally could never see, because it was checking the wrong tree the entire time.

Both failures share a shape with two earlier lessons from the same stretch of work: one about mechanisms that silently report success while doing nothing, where the fix was to add a negative control; and a separate one about a gate that correctly reported failure but whose result the calling command never actually consumed, where the fix was to put the check inside the command chain it's meant to guard. All three are instances of the same underlying trap — a mechanism runs, produces plausible-looking output, and is measuring something other than what it's believed to measure. The cheap, general defense: after scoping any gate, test it in both directions — the thing it must still catch, and the thing it must now allow — as part of the gate's own self-test; after any toolchain shortcut like a symlink, run a positive control by deliberately breaking the file you claim it reads and confirming it complains. Make it fail on purpose before trusting it to pass.
