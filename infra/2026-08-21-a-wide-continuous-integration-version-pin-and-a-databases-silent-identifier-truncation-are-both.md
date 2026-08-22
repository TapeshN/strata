---
title: A wide continuous-integration version pin and a database's silent identifier truncation are both environment-skew facades that stay green for weeks
date: 2026-08-21
category: infra
tags: [ci, env-skew, migrations]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A module raised a real runtime error on the interpreter version actually installed on an
operator's own machine, because it used a newer type-annotation syntax that only works at RUNTIME
on a sufficiently new interpreter — while the CI pipeline's version pin was deliberately wide
("any 3.x"), so CI itself stayed green for weeks on a newer interpreter than the one actually in
use locally. A basic syntax-compile check cannot catch this class of bug, because the offending
construct is syntactically valid Python in every affected version — it only misbehaves as a
runtime type error on the older interpreter. The fix pairs a CI leg pinned to the EXACT interpreter
version actually in use with a dedicated structural (abstract-syntax-tree) scan for the specific
unsupported construct, since neither a wide CI pin nor a plain compile check catches it alone.

Separately, a database migration created an index whose full generated name exceeded that
database's identifier length limit; the database's own automatic truncation of the over-long name
did not match the ORM's own (different) truncation convention for names it expects to be able to
reference later — so a migration that applies cleanly, and a full test suite that passes, both
coexisted with a real, permanent drift between what the ORM believes the index is named and what
actually exists in the database. The generalizable pattern in both cases: a specific combination of
environment or tooling versions can produce a genuine defect that stays invisible for a long time
precisely because the automated gate's own environment happens not to trigger it — a green result
proves correctness only within the ONE environment the gate happened to run in, and a repo whose CI
is not pinned to the exact runtime configuration production or the tooling actually uses should
treat that gap itself as a standing risk.
