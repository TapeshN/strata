---
title: Gate scripts must be tested against real file formats before shipping
date: 2026-06-02
category: guardrails
tags: [gating, release, verify-dont-trust]
confidence: learned
source: private-work
---

A release-gate script that checks a text format (changelog entry, version field, CI output) must be tested against an actual example of that format before it ships. Writing a regex from memory of the format, without running it against the real file, will often produce a pattern that doesn't match.

A false-negative gate that blocks valid releases is worse than no gate — it halts legitimate work while providing no real protection. In a concrete case, the gate pattern anchored at the start of the line but the actual format included a section header prefix, causing the gate to always fail on valid changelogs.

Prevention: run any grep or regex gate against the real target file in the same session it is written. Include at least one negative probe (a line that should NOT match) alongside the positive case. A gate that has only been tested against its own expected inputs may pass on invalid inputs that match accidentally.
