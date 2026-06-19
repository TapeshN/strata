---
title: Unresolvable identifiers demand confirmation, not substitution
date: 2026-06-16
category: guardrails
tags: [hitl, autonomy, gating, preflight]
confidence: learned
source: private-work
---

When an operator supplies an identifier — a port number, line reference, issue ID, file name, or similar token — that cannot be resolved unambiguously in the current context, the correct agent response is to pause and confirm, not to silently substitute the nearest plausible match.

The near-match case is the most hazardous: an identifier that looks close to something real creates false confidence. The agent proceeds, the work appears legitimate, and the mismatch is only discovered later — or not at all. A fix applied to the wrong target is strictly worse than asking a clarifying question.

The pattern that failed here: an operator reference that didn't resolve cleanly was interpreted as a likely typo pointing at a nearby artifact. The agent applied a fix to that nearby artifact. The fix may have been valid in isolation, but it was off-target relative to what the operator almost certainly intended.

The guardrail: before acting on any identifier, verify it resolves to exactly one unambiguous target in the current workspace state. If it does not, treat the ambiguity as a blocker. Re-examine the workspace, surface the candidates, and ask the operator to confirm which one they meant. Never advance past an unresolved reference on the assumption that 'close enough' is correct.
