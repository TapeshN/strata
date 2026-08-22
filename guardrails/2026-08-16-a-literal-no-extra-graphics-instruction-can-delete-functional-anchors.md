---
title: A literal "no extra graphics" instruction can delete functional anchors — flag the conflict, don't weaken the test
date: 2026-08-16
category: guardrails
tags: [gating, contracts]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Asked to render "only the core view, no extra graphics," a literal interpretation
removed a set of interactive controls that looked decorative but were in fact
functional anchors — a separate guided-tour feature and a recently-fixed test both
depended on those exact elements being present and addressable. Stripping them broke
both, even though the instruction was followed to the letter.

The generalizable read: an instruction like "no extra graphics" or "clean this up"
almost always means the decorative clutter, not the functional controls other features
are wired to. Before deleting or hiding an element to satisfy a cosmetic request, check
whether anything else in the codebase depends on it being present — tests that
reference it, other features that assume it exists.

When following the literal instruction would break an existing passing test, the
correct move is to stop and flag the conflict for a decision — never to weaken or
delete the test so the literal instruction can proceed unopposed. A test that quietly
gets loosened or removed to force a change through is a worse outcome than an
instruction that takes one more round to clarify.
