---
title: "A meter said three tests were bad; the tests were fine and the meter was blind"
date: 2026-09-06
category: guardrails
tags: ["meta-gate", "false-negative", "detector-vs-subject", "negative-control", "doctrine-16"]
confidence: learned
source: private-work
---

extended the detector to recognise the inline-runner shape, deliberately narrow (the callee must look like a runner) so `assertEqual(len(rows), 2)` cannot pose as block proof. Negative controls RUN, not assumed: a length of 2, an unrelated helper, a parser returning 2, and an assert of ALLOW all stay unmatched. 16/16 blocking gates now proven, up from 13/16.

when a meter says your work is bad, check the meter before changing the work — especially when the meter's verdict would be satisfied by making the work worse. The file's own comment records the mirror-image error (a first draft reported 22 unproven hooks for the same class of reason), so this was a known failure mode that recurred in the opposite direction.

a false negative in a gate is expensive precisely because the obvious remedy damages something real.
