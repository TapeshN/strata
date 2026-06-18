---
title: CI is the only trustworthy build witness — local pass is not CI green
date: 2026-06-16
category: guardrails
tags: [gating, ci, determinism, autonomy, subagents, roles]
confidence: learned
source: private-work
---

Across multiple parallel agent lanes in the same work session, a recurring failure mode emerged: an agent reports a successful local build, the orchestrating layer relays that result as confirmation, and the PR is treated as green — but the actual CI pipeline is red. This happened in at least four distinct cases within a single session. The root cause is that a local build executes in an environment that differs materially from CI: it has a populated secrets file, no end-to-end test suite, and no secret-scanning step. A build that passes locally under those conditions says nothing about whether it will pass in the environment that matters.

The lesson has two parts. First, the witness must be at least as strong as the gate it claims to satisfy. A local build exit-code is a weaker witness than CI; an end-to-end test result is a weaker witness than a full status-check rollup; a file-existence check is a weaker witness than confirming the thing the file describes actually fires. Substituting a weaker witness for a stronger one is a silent failure — the gate appears green while the underlying condition is unverified.

Second, an orchestrating agent that relays a subagent's self-reported result without independently verifying it against the authoritative source inherits that subagent's blind spots. The fix is procedural: before calling any PR ready to merge, the coordinator must query the CI system directly and require a clean merge-state status with zero failing checks. No agent's self-report substitutes for that query.

A related anti-pattern appeared with a build script that required runtime secrets to be present in order to complete. Because local environments had those secrets populated, builds passed locally and failed only in CI and preview deployments, which correctly lack them. Build-time gates may only assert conditions that are knowable at build time — typically structural concerns like bundle hygiene or type correctness. Requiring runtime values at build time conflates two distinct lifecycle stages and guarantees CI breakage while making local development look healthy.

The generalizable principle: define the authoritative witness for each gate before the gate is considered wired, verify that the witness is actually reachable by the agent performing verification, and never accept a self-reported local result as a substitute for the system-of-record check.
