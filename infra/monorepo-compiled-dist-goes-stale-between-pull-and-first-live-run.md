---
title: A monorepo's compiled dist goes stale between pull and run — rebuild shared packages before the first live invocation
date: 2026-06-16
category: infra
tags: [ci, determinism, lifecycle, release, wired-not-working]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

In a monorepo with a shared compiled package, pulling the latest code from the remote does not rebuild that package's compiled output. The consumer loads the compiled dist file — which is gitignored and not updated by a pull — not the TypeScript source. If the source was updated after the last local build, the consumer will run stale code silently: no error on startup, no warning, just behavior that doesn't match the current source.

A concrete failure: a shared module's compiled dist was built before a new function was added to the source. After pulling the branch that added the function, the runtime executor loaded the stale dist and raised an error on first call — `is not a function`. All unit tests passed because they import TypeScript source directly through a TS-aware test runner. Only the compiled-dist consumer (the production executor) was affected. The bug stayed latent until the first real dispatch.

This is a structural gap between what tests verify and what the live path executes: tests run against source, production runs against the compiled output. The two can diverge silently in a monorepo where builds are not automatically triggered on pull.

The fix is structural: a preflight step that rebuilds the shared workspace before starting the consumer. This should be part of any execute, serve, or deploy command that depends on a compiled package. "Pull and run" is not enough — it must be "pull, rebuild shared, then run."

The adjacent verification principle: before claiming an integration is working, perform at least one real end-to-end live run. A pipeline that is fully coded, merged, tested, and key-valid can still fail on first use if the build step has not been run since the last relevant source change. Confirm success via the receiving service's own API (an active agent, a queued job, a confirmed receipt), not via the local process's output.
