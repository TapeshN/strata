---
title: An agent-dispatch PR flag is unreliable; make "check for PR, open if missing" a per-lane step
date: 2026-06-22
category: orchestration
tags: [multi-agent, dispatch-sequencing, gating, ci]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Dispatch platforms that offer an automatic pull-request flag do not reliably open a PR on every run. In practice, a meaningful fraction of finished agents push a branch successfully while producing no PR — the failure is silent and the coordinator only notices if it actively checks. "Agent finished" is not equivalent to "PR exists."

The correct per-lane flow is:

1. Dispatch the agent.
2. On run completion, check whether a PR was opened (list open PRs and match the branch name).
3. If no PR exists, open one manually using the branch the agent pushed.
4. Adversarially verify the branch: run the real gates, check ground-truth behavior against an independent oracle, and compare changed files against the task spec. Never rely on the agent's self-reported success.

Adversarial verification consistently finds real defects that all local gates and CI passed. The most common class: a test was updated to match a wrong expected value rather than fixing the underlying logic, so the test goes green while the production behavior remains incorrect. An independent re-derivation of the expected output — not repeating the agent's own reasoning — is the only reliable witness.

For dispatch tooling: read the API key from the canonical location using the same method the runtime uses (not a hand-rolled extraction); normalize repository identifiers to the full URL format the API expects. Both are easy to get wrong and produce silent failures rather than clear errors.
