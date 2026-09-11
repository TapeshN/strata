---
title: Union is the safe merge for an append-only log, and the wrong one for a queue
date: 2026-09-05
category: guardrails
tags: [determinism, boundaries, idempotency]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When reconciling several copies of append-only-looking state files so a stale checkout could catch up, a straightforward union — combine every row present in any copy — was the correct merge for most of them, but wrong for one, because that one file was a queue: an item had already been judged and removed from it earlier the same day, and the file's current emptiness on that entry WAS the up-to-date state. Unioning brought the stale row back, silently reversing a completed judgement and reopening an alarm about work that was actually finished.

The files were identical in format, extension, and append-shaped history — nothing about their name or structure distinguished the two kinds. The only discriminator that matters: does a row's ABSENCE ever encode a real state change? In a pure log, absence just means "not yet written" — union is lossless. In a queue where processing an item means removing it, absence means "handled" — union is a resurrection of already-completed work.

The catch was accidental: a reviewer recognized a row they had personally deleted hours earlier and re-read the diff rather than trusting the merge output. Rule: before merging two on-disk versions of a state file, ask explicitly whether its normal writer ever performs a delete/dequeue as part of ordinary operation. If it does, the merge needs a deliberate pick-one-side (or a real reconciliation pass) — never a blind union. Same extension and shape are not evidence of the same merge semantics.
