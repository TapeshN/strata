---
title: A Spec-Table Gate Must Enumerate Every Row, or Coverage Gaps Hide Behind Green Tests
date: 2026-06-11
category: guardrails
tags: [spec-coverage, dry-run-gates, test-design, verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When you build an automated verification gate (a dry-run check, a compliance scanner, a pre-merge validator) from a specification table, the gate must enumerate every row of that table as its own explicit check — not just the rows that were top of mind when you wrote the first tests. A gate that only covers a subset of the spec will pass its own test suite cleanly while silently missing entire categories of failure, because nothing in the test suite proves coverage of the rows that were never encoded. Green output from a partial gate looks identical to green output from a complete one — the gap is invisible unless someone deliberately audits row-by-row.

What happened: a dry-run gate was built against a multi-row specification, but only a subset of the spec's rows were actually wired into checks. The gate's own tests passed, creating false confidence, because the tests exercised the implemented rows, not the spec as a whole. The gap was categorical, not incremental — whole classes of check were simply absent, not merely weakly tested.

How to apply: when building any spec-driven gate, first produce an explicit mapping table of spec-row to implementing-function (or check-name), and keep that mapping in the handback/PR description so a reviewer can tick off each row against the code. Treat any spec row without a corresponding function as an open gap, not a "later" item. For the tests themselves, enumerate boundary cases systematically — for table-driven logic, cover every combination of "input signal absent" first (these should reliably produce a skip/no-op outcome), since a missing-input path is the cheapest, highest-signal way to catch a gate that silently no-ops instead of failing loud.
