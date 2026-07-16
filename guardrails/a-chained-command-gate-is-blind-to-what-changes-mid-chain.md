---
title: A command gate that pattern-matches a whole chain against current state is blind to what changes mid-chain
date: 2026-07-16
category: guardrails
tags: [gating, command-chaining, guard-design, preflight]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A pre-execution safety gate that inspects an entire shell command line as one string and compares it against the CURRENT state of the system has at least three characteristic blind spots, all found within the same review pass. First, when a single command line chains a state-changing step with a guarded step — for example, switching to a new branch and then committing, all in one chained line — the guard evaluates the chain against the state that held BEFORE the chain ran, so a chain that first exits a protected context and only then performs the guarded action looks, to the gate, exactly like performing the guarded action while still in the protected context, and gets blocked even though it is actually safe; the mirror-image case, a chain that looks safe at the start but ends up inside a protected context, is the more dangerous direction and deserves at least as much scrutiny when auditing a gate. Second, a gate that scans the literal text of a command for dangerous-looking patterns will also match those patterns inside a heredoc body, meaning prose that merely describes a gated operation — for a commit message, documentation, or a written report — can trip the same gate as actually running the operation. Third, a pattern meant to catch bulk or recursive destructive operations can misfire on an operation that is narrow in actual effect but textually similar to a broad one, such as an index-only, single-entry removal that happens to use a recursive-looking flag.

The general fix is to make the gate state-aware rather than purely textual: evaluate each step of a chained command against the state that will hold at that step, not only the state before the whole line runs; treat heredoc bodies as data rather than as commands when scanning for dangerous patterns; and scope destructive-operation matches by what is actually affected (a single tracked entry versus a whole directory subtree) rather than by surface flag syntax. Any audit of a command-level safety gate should include chained commands, heredoc-embedded text, and narrow-but-textually-similar operations as an explicit part of its test set, not only the single, standalone command case.
