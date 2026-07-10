---
title: A verification witness must run through the actual production call path
date: 2026-07-10
category: evals
tags: [testing, verification, production-path, test-theater, witness-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A test that "witnesses" a fix is worthless unless it exercises the actual production call path — a passing test whose entry point differs from the code path real requests take proves nothing about production behavior.

**What happened.** A safety check (a spend/rate-limiting guard) was correctly embedded inside one helper function, and that helper had a passing test covering it. But an audit of the real call sites found that helper had zero production callers. Every real caller had independently hand-copied the same "check, then call, then record" sequence inline, without ever routing through the tested, guarded helper. So the guard existed and was tested — just not on any path a real request actually took. The one thing that looked verified was, in production, a no-op; the paths that mattered were silently unguarded and had never been exercised by the test suite at all. This shipped clean through a full green build, type-check, unit tests, and lint, because none of those gates asked whether the tested code was reachable from a real entry point.

**How to apply.** When you write or review a "we verified this" claim, don't stop at "a test passes and covers this logic" — trace whether the test's entry point is the same function real traffic invokes, or a look-alike wrapper nobody calls. Two concrete habits: (1) route every real call site through the single gated helper so the guard can't be silently reimplemented-then-dropped per call site, and (2) add a test anchored at each real production entry point that goes red if the guard is removed, not just a test of the helper in isolation. Treat this as a specific case of a broader rule: a proof only counts if it shares the code's actual path, not merely its logic — verify reachability, not just correctness in isolation.
