---
title: A sanitizer's step ORDER is itself the security contract — and a pipeline should audit its own earlier stages as an attack surface
date: 2026-08-17
category: guardrails
tags: [security, gate-design, false-green]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A text-sanitizing function meant to strip a dangerous leading pattern was bypassed two different
ways: certain leading control characters sat outside the reach of its anchored search pattern, and
— more subtly — an EARLIER stage of the very same sanitizer (a step that collapses certain
whitespace sequences) transformed one dangerous prefix shape into a slightly different one that a
LATER stage's guard no longer recognized. The sanitizer was, in effect, manufacturing its own
bypass internally. The fix reordered the pipeline explicitly (strip dangerous leading bytes first,
then apply an exemption check to the now-cleaned candidate, then consume any interleaved trigger-
and-blank-line runs) with an inline note stating which specific defect each ordered step is meant
to prevent, so a later well-intentioned "tidy this up" pass cannot silently reorder the steps back
into an exploitable sequence.

The generalizable rule: in any sanitize-then-transform pipeline, ask whether an EARLIER
transformation step can manufacture the exact shape a LATER guard is supposed to catch — and never
let an inline comment assert that some input shape is "unreachable" unless the code actually
enforces that, rather than merely hoping it does.
