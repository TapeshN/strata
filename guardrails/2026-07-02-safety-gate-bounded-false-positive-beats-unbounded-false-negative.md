---
title: On a safety gate, a bounded false positive beats an unbounded false negative — if a fix cannot be proven airtight, drop it
date: 2026-07-02
category: guardrails
tags: gating, security, autonomy, rollback
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A proposal to reduce a destructive-action guard's false-positive rate (it was over-blocking some safe commands) went through three rounds of adversarial red-teaming before anyone trusted it near a merge. Each round found a fresh bypass of the guard's protected-branch and destructive-action detection: a heredoc piped into a shell, a process-substitution variant, and finally a branch-switch chained with a semicolon that lands on the protected branch because the shell does not short-circuit there. All three bypasses sailed straight through the existing local test suite — none of them were things the test suite was written to check for, because the fix's own author had not imagined them either.

The proposal was fully reverted rather than iteratively patched.

The generalizable rule: on a safety gate, the two failure modes are not symmetric. A false positive costs a developer a few seconds of friction and an obvious, visible failure — it is safe by construction. A false negative silently lets through the exact class of action the gate exists to stop, and it is invisible until something is already broken or exposed. When a proposed fix to reduce false positives cannot be shown to be provably airtight — and especially when successive rounds of adversarial testing keep finding new bypass shapes rather than converging to zero — the correct response is to drop the fix, not to keep patching around the latest hole. A gate that annoys is recoverable; a gate that silently fails is not.

The practical trigger for "drop it": if adversarial review round N finds a genuinely new bypass shape (not a variant of the same root cause already fixed), that is a signal the surface is larger than understood, and no amount of local unit testing would have caught any of the found bypasses — meaning the same is likely true of the next one.
