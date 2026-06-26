---
title: Name the witness and check its scope before reporting a root cause
date: 2026-06-24
category: guardrails
tags: [verify-dont-trust, determinism, evals]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A diagnostic run against one environment is not a witness for a different environment. When a root cause names a specific environment — a production secret, a live database, a deployed service — the evidence must come from that environment, not from a local or staging equivalent.

A test that fails against the local configuration cannot prove the production configuration is wrong. The authoritative witness for a production issue is a check that actually runs against production. Running the same check locally and treating the result as proof of a production bug is a scope error.

The same principle applies to proxy metrics. A byte count does not witness that content renders correctly in a real client. An HTTP status code does not witness that a page's assets load. A stub result does not witness that the real integration works. Before reporting a root cause, identify the exact check and ask whether its environment matches the environment where the symptom occurs. If not, the check is not a witness — it is a hypothesis that still needs to be grounded in evidence from the actual failing environment.
