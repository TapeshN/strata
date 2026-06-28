---
title: A zero-step CI death with no logs is a billing or quota wall, not a code problem
date: 2026-06-27
category: guardrails
tags: [ci, gating, reproducibility]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When a CI job fails in under fifteen seconds with no step logs, no annotations, and the
runner log ending before "Set up job" executes, the failure is at the runner-provisioning
layer — not in the code or the action versions. Bumping dependency or action versions is
a red herring that consumes a CI run without addressing the cause.

The distinguishing signature: the run dies before any step output appears, sibling jobs on
public repositories pass, and the CI provider's status page shows no incident. This pattern
points to a spending cap or quota wall on the private-repo account rather than any actionable
code defect.

The diagnostic path is to download the run-log archive and inspect the system-level log
file (not the step log, which is empty). That file shows the runner handshake ending without
the job initializing. Cross-checking whether public and private repositories behave
differently under the same workflow confirms the account-level cause.

The lesson: never change a dependency or action version in response to a runner-startup
death. The fix lives at the account or billing layer, and applying a code change amplifies
confusion by producing another red run while the real cause remains untouched.
