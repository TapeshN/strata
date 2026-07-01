---
title: A read-only task does not stop a subagent from reaching for a mutating command against a shared checkout
date: 2026-07-01
category: guardrails
tags: [worktree, subagents, isolation, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A worker agent given a narrowly read-only task — inspect the exact content of one specific commit on a shared, non-isolated checkout — used a version-control command that both stages and overwrites the working tree to materialize that commit's content, rather than a non-mutating equivalent that would have shown the same content without touching the working tree at all. The worker caught its own mistake immediately, reverted losslessly, and verified the checkout was byte-for-byte back to its prior state — and a second, independent check by the coordinating layer confirmed that claim rather than trusting the self-report at face value.

The general lesson has two parts. First, an isolation discipline stated as "never mutate a shared checkout directly" is usually framed around file edits, but the same risk exists in command-line operations issued against version control — a command described in a task briefing as "just inspect X" can still, in its actual mechanics, stage or overwrite a shared working tree, and a worker optimizing for convenience may reach for the familiar mutating form without recognizing the distinction. When briefing any task that touches a shared, non-isolated checkout, spell out which specific non-mutating commands are acceptable rather than assuming "read-only in intent" is understood as "non-mutating in mechanism."

Second, a subagent's own report that it "caught and fixed" a mistake on shared state deserves the same independent verification as any other unverified claim — trust-but-verify applies to a subagent's self-repair, not only to its forward-facing results.
