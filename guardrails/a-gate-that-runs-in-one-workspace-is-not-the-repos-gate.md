---
title: "A gate that runs in one workspace is not the repo's gate — and data parity is not render parity"
date: 2026-08-12
category: guardrails
tags: [verification, gates, cross-surface-parity, ui-truth, monorepo]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

# A gate that runs in one workspace is not the repo's gate

A monorepo with two applications had been type-checking cleanly for weeks. One
of the two apps had not compiled in any of them. The type-check was being run
from inside a single workspace directory, and the hosted build only compiled the
app it deployed — so the second app had **no mechanical gate at all**, and a
type error sat there through several green batches until someone happened to run
the root command.

**Prevention.** Before calling a batch verified, list the surfaces the change
touches and name the command that covers each one. When the hosted build only
compiles one app, the other app's absence of a gate *is the finding*, not a
detail to note in passing. Run the gate from the repository root, never from the
directory you happen to be standing in.

## Parity of data is not parity of what a person sees

Two surfaces shared a theme definition, and a test asserted that both held the
same values — which it did, and passed. Then one surface stopped *using* one of
those values in its rendering path. The data still matched. What people saw did
not. The test was checking the warehouse, not the shop window.

**Prevention.** For any pair of surfaces meant to look alike, ask what the test
would say if one of them stopped *consuming* a value they both still hold. If
the answer is "still green", the test is not protecting the thing you care
about.

## A guided tour has to be looking at the same screen the reader is

A walkthrough step said "tap the key to open it" — about a panel that renders
already expanded. The copy was written from the design intent rather than from
the component's actual initial state, and nobody walked the tour end to end
before shipping it, so the one feature whose entire value is *matching what is
in front of the person* was the feature verified least.

**Prevention.** Before writing copy that names a control's state, read that
component's initial state. Then walk the whole thing in a browser.

## A fallback exercised by most inputs is the design

A placement rule put an element on the preferred side "with a fallback when it
would collide". For the real targets, it collided almost every time — so the
fallback *was* the normal path, and the element kept landing somewhere nobody
had designed. The fix was to stop treating one branch as preferred and reserve
space unconditionally.

**Prevention.** When a layout rule has a preferred branch and a fallback, work
out which one the **real** inputs take. A fallback exercised by most inputs is
the design; the "preferred" branch was the special case.

## Retire the affordance that stopped scaling, don't shrink it

A step indicator drawn as one dot per step was fine at eight steps and
unreadable at twenty-four. The instinct was to shrink the dots. The right move
was to ask what the component was *for* — telling someone roughly how far
through they are — and replace it with a progress bar plus a section label,
which answers that question at any count.

**Prevention.** When a component's count grows several-fold, re-ask what the
component was for before adjusting its size.
