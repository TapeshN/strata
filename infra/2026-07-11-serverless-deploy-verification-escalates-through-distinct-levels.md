---
title: Serverless deploy verification escalates through distinct levels — "done" is the deepest one that actually applies
date: 2026-07-11
category: infra
tags: [ci, release, boundaries]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

For an app that ships to a serverless/edge platform with a client-bundling step, there isn't one "it's tested" bar — there are at least three, and each can pass while the next fails silently in production.

Level one: type-checking and unit tests run in a plain Node process, and both can pass on code a browser bundler cannot actually package — a Node-only API imported into a module reachable from client-rendered code type-checks and unit-tests cleanly, then fails specifically in the client-bundling step, which neither check exercises. The fix at this level is to prefer platform-neutral primitives (a web-standard API instead of a Node-only one) for anything reachable from client-side code.

Level two: even a clean build does not prove the serverless runtime actually loads and executes the code — a transitive dependency that assumes a browser-like or CommonJS environment can build and unit-test fine locally, then crash at module-load time in the real serverless runtime (a require/import-shape mismatch), producing a runtime error in production while every local and build-time gate stayed green. The fix at this level is auditing the dependency tree for runtime-incompatible transitive packages and preferring ones built for the serverless runtime.

A companion failure in the same family: an environment-detection check written with one deploy target in mind didn't account for a different deploy target the platform maps onto the same underlying signal, silently failing closed on infrastructure the check's author never actually tested against.

The generalizable rule: for any platform with more than one execution context between "compiles" and "a real user hits it" (Node vs. browser-bundle vs. serverless-runtime), verification has to walk through each context in turn — the only complete witness is exercising the actually-deployed route, not a local build or test run standing in for it.
