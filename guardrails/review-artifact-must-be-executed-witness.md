---
title: Review wiring assertions require an executed witness, not a code-inspection artifact
date: 2026-06-06
category: guardrails
tags: [gating, verify-dont-trust, roles, evals]
confidence: learned
source: private-work
---

An adversarial code review that accepts a capability claim based on reading the source code rather than executing the tested path can produce a false pass. A reviewer who marks a wiring assertion as verified by citing a code-inspection artifact ("I read the source; the logic is correct") validates intent, not behavior. The integrated execution path may have defects the unit tests never exercise.

In a concrete case, a wiring assertion was marked verified by code inspection. The coordinator's independent integrated run showed the gate was non-functional — a module import sequence that worked when imported directly failed when loaded dynamically, with a different initialization order.

Prevention: wiring and integration assertions require a runtime witness — an executed command with observable output — not a code citation. Any `grep`, `cat`, `read`, or code-inspection phrase as an artifact command should be treated as unverified for the purpose of a wiring check.
