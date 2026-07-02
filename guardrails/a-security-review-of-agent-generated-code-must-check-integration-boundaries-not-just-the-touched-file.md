---
title: A security review of agent-generated code must check integration boundaries, not just the file the agent touched — a cost-tier model reliably ships real money/auth bugs that pass CI
date: 2026-07-02
category: guardrails
tags: [model-tier-routing, security-review, ci-not-trust, double-verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A recurring pattern across several dispatches to a cheaper, cost-tier coding model: the returned code passed every automated check — compilation, unit tests, linting, and standard security scanners — while still containing real, exploitable money- or auth-path bugs. The bugs were not in the code the agent wrote in isolation; they were in how that code integrated with the rest of the system — a boundary the agent's own tests never exercised because the agent only tested the surface it built, not the seam where it met existing logic.

CI-green from a generation-optimized model proves the new code compiles and its own narrow tests pass. It does not prove the new code is safe where it connects to everything else — access control that assumes a check happened upstream, a data path that silently trusts a caller, a boundary condition only visible when combined with adjacent code the agent never read.

The fix: any code from a coding agent that touches money or auth needs an independent adversarial security review focused specifically on integration boundaries — not a re-read of the diff for what the agent said it did, but a hunt for what the agent's own narrow test suite would never have caught because it only tests the seam from one side. Do not treat "all automated checks green" as sufficient signal on a money/auth surface regardless of which model produced the code.
