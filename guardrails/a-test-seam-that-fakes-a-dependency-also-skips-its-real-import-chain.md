---
title: A test seam that fakes a dependency also skips loading that dependency's real import chain
date: 2026-08-30
category: guardrails
tags: [runtime-import, test-seam, dependency-injection, esm-cjs]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A production sign-in path failed on every attempt while the full automated test suite stayed green. The cause was an authentication library's real verification code path throwing a runtime-only module-resolution error — a CommonJS-required package pulling in an ESM-only nested dependency, an error class that only ever surfaces when the actual import chain executes. The test suite never hit it, because the test seam substitutes a fake verifier for exactly that code path, so no test in the suite ever loaded the library's real import chain. The fix was switching to a lighter verification approach already used elsewhere in the same codebase, and verifying the fix live in production rather than trusting the suite alone.

The generalizable rule: whenever a test seam substitutes a fake for a real dependency, that substitution also silently skips loading the dependency's actual import chain — so a whole class of runtime-only failures (module resolution, native bindings, environment-specific initialization) can ship completely unseen by an all-green test suite. Any dependency whose real import path is bypassed by a test seam needs at least one smoke test that imports and initializes the real chain, not only the substitute. Separately: when a system's error handling maps several distinct underlying failures to one generic user-facing message, keep a server-side reason trace behind that message from day one — an indistinguishable failure message costs multiple debugging round-trips before a trace even exists to read.
