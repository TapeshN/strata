---
title: Fixing a bug class thoroughly means sweeping from the file your own fix cites as its pattern origin, and fixing the keying at the producer
date: 2026-07-11
category: guardrails
tags: [multi-tenant, boundaries, contracts, layering]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A join or lookup that keys on a value with insufficient precision (for example a coarse timestamp with no tenant/owner identifier) can silently cross-join unrelated records whenever two of them happen to land on the same value at that precision — with the failure surfacing only as anomalous counts, not an error. Fixing the specific places the bug was reported passes review, but a genuinely thorough fix requires an independent sweep for the same defect elsewhere in the codebase — and the highest-yield place to start that sweep is the exact file that the already-fixed code's own comments or docstrings cite as "the pattern we mirror." That file is disproportionately likely to carry the identical defect, because it's the origin the other call sites were copied from, and it is easy to overlook precisely because it wasn't in the original bug report.

Separately: once the defect class is understood, the most durable fix is not patching every consumer that joins on the bad key — it's fixing the key at its source, so every downstream consumer inherits the correct value for free instead of each needing its own patch.

The general rule: (a) when you fix one instance of a bug class, explicitly sweep the codebase for the same shape, starting with whatever file the fixed code's own documentation names as its origin or reference implementation; (b) when the defect is a missing or too-coarse identifier flowing through a pipeline, fix it at the point the identifier is produced, not at each point it's consumed.
