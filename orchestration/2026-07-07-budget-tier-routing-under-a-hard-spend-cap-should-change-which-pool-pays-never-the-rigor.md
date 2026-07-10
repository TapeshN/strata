---
title: Budget-tier routing under a hard spend cap should change which pool pays, never the rigor applied to risk
date: 2026-07-07
category: orchestration
tags: [cost, model-tier-routing]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Operating near the edge of a fixed weekly compute allowance, with a small additional metered credit available as backup, the routing decision that held up was to spend down the free, periodically-resetting allowance first, treat the metered credit purely as overflow once the free pool hit zero, and route separately-priced parallel or heavy work through yet a third, dedicated pool rather than pulling any of it onto the primary allowance. A tier explicitly reserved for high-level strategic realignment was deliberately kept out of active shipping work even under budget pressure, since using the wrong tool for the job wastes the scarcer resource faster than it saves the cheaper one.

The one legitimate way this pressure was allowed to change behavior was matching the depth of review to the actual risk of the code being changed — skipping a repeated re-review of code that is demonstrably dormant or inert is a reasonable adjustment to make under any budget, not a corner cut. Every change touching money handling, authentication, access control, or client data kept its full independent adversarial review regardless of how tight the budget was.

The generalizable rule for operating any multi-tier resource (subscription allowance, metered credit, a separate dispatch pool) under a hard cap: which pool absorbs the cost is a legitimate, explicit routing decision to make under pressure; how carefully any given piece of work is verified should track the risk of that specific work, and only that — never the remaining budget.
