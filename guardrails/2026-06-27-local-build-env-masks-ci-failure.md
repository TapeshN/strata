---
title: A populated local environment file masks CI-fatal missing secrets during a local build
date: 2026-06-27
category: guardrails
tags: [ci, gating, reproducibility, worktree]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A build run inside a populated local worktree passes when CI fails because the two
environments are not equivalent. A local worktree inherits whatever environment file
exists in the checkout; a CI run has only the secrets explicitly provisioned in the
pipeline. A check that requires a runtime secret at build time will succeed locally
(where the secret is present) and fail in CI (where it is absent), and the local result
tells nothing about the CI result.

The failure mode is compounded when an agent self-reports a local build pass and the
coordinator relays that claim as CI-green. The coordinator then discovers the failure
only when independently checking the CI conclusion — after having represented the work
as done.

Two distinct checks must be distinguished: a build-time check (which must be satisfiable
without runtime secrets, because the build runs where secrets are absent) and a
deploy-time or runtime check (which requires secrets but only runs after deployment).
If a check at build time requires a runtime secret, it belongs at a later stage.

The reliable witness for a pull request is the CI conclusion read directly from the
version control provider — not a local build result, not an agent's self-report. A
local build that passes because the developer environment holds secrets the CI runner
does not is a broken witness.
