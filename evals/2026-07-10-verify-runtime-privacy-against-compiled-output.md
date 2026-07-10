---
title: When testing runtime encapsulation guarantees, verify against the compiled artifact, not the source
date: 2026-07-10
category: evals
tags: [typescript, tsc, private-fields, weakmap, transpilation, security-testing, build-verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When you claim a runtime property holds — a private field truly can't be read from outside, an object is truly frozen, a brand check truly can't be spoofed — the only valid witness is the artifact that actually ships and runs, not the source file a fast test runner transpiles on the fly. These two can enforce genuinely different semantics, and a green test on one tells you nothing about the other.

What happened: a package used native `#privateField` syntax for an internal value meant to be inaccessible from outside the class. The test suite ran green under a modern test runner (in this case, one that uses esbuild), which compiles to a recent JS target and preserves true private fields as native engine-level privacy — unreadable and unforgeable from outside, full stop. But the project's actual build config (`tsc` targeting an older ECMAScript version, ES2020) downleveled that same private field into a `WeakMap`-backed emulation plus helper functions to get/set/check membership. That emulation is not truly private: an attacker who can monkeypatch a built-in method the helpers rely on (like `WeakMap.prototype.has`) can intercept and defeat the "privacy" entirely. So the exact attack that source-level tests correctly reported as blocked succeeded against the compiled output that real consumers actually import and run.

How to apply: whenever a test asserts something about runtime structure — private state, immutability, brand/type checks, anything relying on JS engine guarantees rather than plain logic — build the project with its real production build command first, then run the attack or assertion against the compiled output in the actual output directory, not against the source. Treat the compiler's target/lib setting as part of the security surface: downleveling can silently swap a hard guarantee for a soft, bypassable one. If you must support an older target, either accept the weaker guarantee explicitly and document it, or raise the target and verify the raise actually removes the emulation by diffing the compiled output before and after.
