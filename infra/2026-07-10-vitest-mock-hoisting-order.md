---
title: A vi.mock factory runs before your top-level consts exist
date: 2026-07-10
category: infra
tags: [vitest, testing, mocking, javascript, typescript]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When a `vi.mock("module", factory)` call references a top-level `const` or `class` declared later in the same file, the factory throws `Cannot access 'X' before initialization` — and the whole test file reports "0 tests" rather than a normal failure. That's the tell: it's a collection-time load error, not a test assertion failing.

**What happened.** Vitest hoists every `vi.mock()` call to the very top of the file, above all imports and top-level variable declarations, so the mock factory can intercept the module before anything else runs. But a plain `const mockThing = {...}` or a `class SomeError extends Error {...}` defined later in the file is not hoisted the same way — it only exists after its own declaration executes. If the factory closes over that binding, it's referencing a variable that hasn't been initialized yet, and the engine throws immediately during module evaluation, before any test even registers. This surfaced repeatedly in a single session — once for a custom error class used by a mocked helper, and again for a mock data object used by a mocked data-access layer.

**How to apply.** Anything a `vi.mock` factory needs to reference — mock objects, fake classes, sentinel values — must be created inside a `vi.hoisted()` callback. That callback is itself hoisted above the mock factories, so the bindings it returns by destructuring are already initialized by the time a factory closes over them. Declare the fake class and the mock function inside the callback, return them as an object, destructure that object into top-level consts, and pass those consts to the factory. The rule of thumb is that the factory may only reference names that came out of `vi.hoisted()`, an import, or the module scope of the mocked module itself.

The general debugging rule: when a Vitest (or Jest) file reports zero tests collected instead of some number of pass/fail results, suspect a hoisting-order problem in a mock factory before assuming a config or environment issue.
