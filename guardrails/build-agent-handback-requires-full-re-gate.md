---
title: A build agent's handback is a claim; the coordinator must fully re-gate it, including confirming every new test actually executed
date: 2026-06-22
category: guardrails
tags: [gating, determinism, evals, ci]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A build agent that stops mid-task leaves a plausibly-complete file tree that has never been compiled or tested. An agent that completes and returns a one-line summary has told you nothing about whether the code builds, whether the tests pass, or whether the new test actually ran.

"Files exist" is not evidence. A build agent's handback is a claim, not a witness.

The coordinator must independently re-gate every handback:

1. Run the real build and full test suite. Do not rely on the agent's reported output.
2. Confirm each new test actually executed by grepping the test-runner's output for the new test's name. Test frameworks that enumerate test files explicitly in a run script silently skip any new file not added to that enumeration — the suite passes while the new test is dead.
3. For additive schema changes (adding a value to an enumeration, a new variant to a union type), check every location where the type is duplicated or re-declared. Agents routinely add the value to one declaration and miss the others.
4. For blocklist or IP-gate verification, replicate the gate's exact term-loading logic (strip blank lines, strip comment lines, then substring-match) rather than running a raw file-based grep. A raw grep with blank lines in the pattern file matches everything and generates false alarms.
