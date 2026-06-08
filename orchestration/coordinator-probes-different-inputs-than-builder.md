---
title: The coordinator's independent verification must probe inputs the builder's fixtures don't cover
date: 2026-06-07
category: orchestration
tags: [verify-dont-trust, roles, evals, fan-out]
confidence: learned
source: private-work
---

An adversarial reviewer who reuses the same witnesses as the builder inherits the builder's blind spots. If the builder's test suite only exercises one category of input (for example, structured numeric values), the reviewer may accept a claim that the system handles other input categories (free-form strings, edge cases) without actually probing them.

The coordinator's independent verification should probe the edges and input categories that the builder's fixture set does not cover. In a concrete case, the builder's tests used one input format; the coordinator probed a different format and found it was rejected despite the specification requiring it to work. The reviewer had accepted without probing the second format.

General lesson: the value of independent verification comes from independence — using the same inputs as the builder validates the builder's assumptions, not the system's correctness.
