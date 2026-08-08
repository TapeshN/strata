---
title: Two independently green test suites can validate the same wrong assumption; a persona-walk catches what no test can
date: 2026-08-08
category: evals
tags: [testing, contract-tests, fixtures, persona-walk, integration]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When two packages or services communicate across a wire boundary, and each side's test suite validates against its own hand-written fixture for the OTHER side's data shape, both suites can pass while both are wrong about the actual contract — the consumer's fixture is shaped how its author imagined the producer responds, and the producer's suite only checks its output against itself. Compilation, type-checking, and every unit test can be green because each side is internally consistent with its own incorrect assumption. The structural fix is a contract test: the consumer's test suite imports the producer's REAL payload-building code, or a recorded real payload, as its fixture, so the two sides literally cannot disagree without one suite failing at commit time. Any hand-written fixture standing in for data that crosses a package or service boundary should be treated as a standing risk.

Separately, a "persona-walk" — manually walking each user role through its single most important, defining action, end-to-end against the real system — catches an entire class of bug that no unit test, type-check, or code review will ever flag: absences. A UI control can render a state the system has no way to produce (an approve/decline action with no code path on either side of the wire that can ever set it), and a role can be missing an action a sibling role has on the identical screen. Nothing is technically wrong with the code that exists, so every static check passes; the defining gap is invisible until someone actually tries to do the thing a real user in that role would do. Any pipeline that ships a multi-role application benefits from a dedicated persona-flow evaluation stage — adversarial, per role, walking the real screens — positioned between "build is green" and "ready to ship."
