---
title: A dry-run gate built from a spec table must enumerate every row — partial enumeration passes its own tests while silently missing whole check categories
date: 2026-06-11
category: evals
tags: [evals, gating, determinism]
confidence: learned
source: private-work
---

When a dry-run or preflight gate is built by implementing rows from a specification table, it is tempting to implement and test only the rows that seem load-bearing. The failure mode is that partial coverage passes its own test suite (every implemented row passes) while leaving entire check categories absent. In production, the gate then silently ignores whole classes of inputs that the spec intended it to catch.

**The fix is structural:** create an explicit mapping of `spec_row → implementation_function` and assert in tests that every row in the specification has a corresponding entry in the map. An integration test that runs the gate over a fixture corpus and asserts the expected set of categories were actually checked is stronger than unit tests over individual rows alone.

**Table-driven testing discipline:** enumerate every `(context-key-absent → SKIP)` case first, before adding pass/warn/block rows. SKIP boundaries are the cheapest signal to verify — if a required context key is absent, the gate should surface a clear SKIP with a stated reason, never a silent no-op or a spurious block. Verifying the SKIP boundary explicitly documents what the gate requires and prevents future callers from passing a "just works" fixture that silently satisfied all keys.

**The handback requirement:** when a subagent returns a verification result, the handback must include a spec-row-to-function map as structured evidence — not a free-form "all checks passed" assertion. A free-form assertion cannot be reviewed for coverage.
