---
title: A check, gate, or preflight step must never write a tracked file as a side effect of its own healing logic
date: 2026-07-13
category: infra
tags: [preflight, gating, ci, idempotency, determinism]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two separate automated steps inside a shared pre-merge check suite each did something reasonable in isolation but dangerous in context: one detected duplicate sections in a tracked changelog-style document and automatically collapsed them on every run; another computed a score for a piece of work and appended that score as a new row to a tracked, append-only ledger file on every run. Both were framed as "checks," so a plain, routine invocation of the check suite — the kind any contributor runs constantly, on any checkout — silently rewrote those tracked files underneath them, in one case reordering thousands of lines and dropping structural headers in the process. Grepping the check's own wrapper script for file-write operations didn't catch it, because the wrapper genuinely only read data; the mutation lived one layer down, inside a "self-healing" helper the wrapper called.

The underlying design mistake is embedding legitimately useful healing behavior — auto-merging duplicate sections that a rebase produced, or appending a real score once — inside something that is invoked, and trusted, as a read-only check. The fix is structural: any write that healing logic wants to make should sit behind an explicit, separately-invoked flag, never fire automatically inside a check/gate/preflight context, and a meta-check that hashes every tracked file before and after the full check suite runs would make an entire class of these silent-mutation bugs mechanically impossible to reintroduce. The general rule: a check, gate, or preflight step exists to observe and report — the moment it writes to a tracked file, it has become a mutation with a misleading name, and every tree that innocently runs it becomes a victim.
