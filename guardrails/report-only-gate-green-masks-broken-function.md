---
title: A report-only gate (exit-code 0) reads green while its core function is broken; verify the behavioral output count, not the step color
date: 2026-06-17
category: guardrails
tags: [gating, ci, determinism, evals]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A gate step configured to exit successfully regardless of findings — using a non-blocking flag, a continue-on-error directive, or a logical-or with true — verifies only that the tool ran. It tells nothing about whether the tool did its job. A security scanner set to report-only will show green even when it finds dozens of violations and every suppression rule is broken.

The definition of done for a report-only gate is the behavioral count, not the step color:

- A suppression that works: the scan runs and reports zero findings after the rule is applied.
- A suppression that does not work: the scan finds N violations regardless; the step color remains green.

These two states are indistinguishable from the CI status indicator alone.

The witness requires reading the actual output: the findings count, the suppression count, which rules fired. An agent that reviews the gate output and returns a structured PASS verdict based on the green step color has not witnessed the gate's function — it has witnessed the step's completion.

A complementary check is the negative control: verify that the scanner still catches a deliberately introduced violation that the suppression should not suppress. If the negative control passes (the scanner catches the planted violation), the detection logic is intact. If it fails, the scanner itself is broken.

A config file consumed by a secret scanner must contain no literal secret-pattern strings, even in comments. The scanner reads the config and may flag its own configuration.
