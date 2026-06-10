---
title: Six operational guardrails that keep biting: env ghosts, exit-code lies, agent resurrection, kill scope, rate-limiter collisions, and seed-state blindness
date: 2026-06-10
category: guardrails
tags: [lifecycle, ci, idempotency, autonomy, worktree, parallel-sessions]
confidence: learned
source: private-work
---

Six distinct failure modes surfaced during a single day of production engineering work. Each is independently reproducible and worth treating as a named guardrail class.

**1. Credential-rotation env ghosts.** A credential rotation is not complete until every live shell and every long-lived process has been verified clean. A single session-local environment variable — one that was never written to any rc file and therefore invisible to the usual tooling — can shadow keyring authentication for hours. Because most CLIs prefer environment variables over keyring entries, every call succeeds from the poisoned shell while fresh credentials appear to expire immediately. Apps launched from that terminal inherit the ghost and report auth failures after each attempted fix. The correct rotation sequence is: issue new credential → sweep all live shells for residual env exports → restart long-lived applications from a clean launch context (not from the same terminal) → only then revoke the old credential. A recurring security sweep should include an explicit check that no credential lives in a shell environment when it should live in the keyring.

**2. Named conclusions, not exit codes.** Reading pipeline health from a process exit code is unreliable when the exit code belongs to the last command in a pipeline rather than to the CI tool itself. The correct signal is the named conclusion emitted by the CI system — a count of explicitly labeled failure rows, not a numeric code. A related trap: when a build has multiple independent failures, fixing one can produce a superficially passing status that hides the remaining failures. The full failure list must be read before acting, not just the first item.

**3. Agent resurrection and the single-writer rule.** An agent that stops reporting during an infrastructure disruption is not necessarily terminated. Re-dispatching its task to a second agent targeting the same working directory risks having both agents wake simultaneously and push conflicting work. Before re-dispatching a stalled agent, confirm termination or assign the replacement to a fresh, isolated working directory. This is the same invariant as the shared-worktree race: a working directory should have exactly one active writer at any moment.

**4. Process-kill scope must be exact.** Killing a process by a short, non-unique name pattern can match unintended processes that share a common substring — including production services running in the same environment. The correct kill target is a fully qualified path or a port identifier specific to the process being stopped, never a bare script name.

**5. Per-IP rate limiters are structurally incompatible with parallel end-to-end test suites.** When multiple browser workers share a single IP address, a shared request counter races across all workers and resets cannot keep pace. The architectural fix is an environment-gated bypass that allows the test suite to opt out of rate limiting in CI, paired with an explicit opt-in enforcement header so that at least one serial test path can still observe real rate-limit responses. A related production corollary: when users share a network address translator — as at a conference venue or on a campus — per-IP limits must be sized for the full population behind that address, not for a single user.

**6. Seed state is a deploy witness, not an assumption.** A production environment can have all code paths green while the underlying data is entirely absent. Observing zero seeded records in a live database while every health check reports success is a real failure mode, not a theoretical one. Seed state must be included in the deploy verification checklist alongside code deployment and service health. The same principle extends to user-facing content: stale version numbers in marketing copy and broken public links are observable failures that no code-level test will catch — they require a user-perspective audit as part of the release process.
