---
title: Only a private class field brand truly unforges a JS object
date: 2026-07-10
category: guardrails
tags: [javascript, typescript, security, capability-object, private-fields, es2022]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

If you need to make an in-memory object unforgeable — impossible to construct via a backdoor bypassing your intended factory — reach for a private class field brand (`#field in obj`, ES2022+) and nothing weaker. Every other JavaScript "sealing" technique is defeatable, and the failure modes are subtle enough that they tend to survive one review and get caught only on the second or third.

What happened: a project needed to guarantee that instances of a security-sensitive class (a spend/budget object gating a kill-switch) could only be created through one sealed constructor — never forged with an arbitrary high-privilege value. Four successive review passes each found a live bypass of the prior fix. First attempt: a JSDoc `@internal` annotation on a "do not call this" static method — pure documentation, zero runtime enforcement. Second: a TypeScript `private` modifier on that method — erased entirely at runtime, reachable via a simple cast. Third: a module-scoped `Symbol` checked inside the constructor — defeated by `Object.create(Klass.prototype)`, which builds an instance without ever running the constructor, so the check is structurally unreachable. Fourth: a `WeakSet` membership brand — defeated by monkeypatching `WeakSet.prototype.has` to always return true, which silently breaks every WeakSet-based brand in the program at once (a realistic supply-chain/prototype-pollution vector). The rung that finally held: an ES2022 private instance field, checked via `#field in obj`. That check is a spec-internal brand operation with no user-overridable method anywhere in its path, and the field can only be installed by code that runs inside the sealed constructor.

How to apply: when you need an unforgeable object brand, ask two questions about your mechanism — (1) is it installed only by the one constructor you trust, and (2) is it checked by an operation nobody can override or route around via prototype tricks? Documentation, TS-only modifiers, symbols checked in a constructor, and WeakSets all fail question (2). Private field presence checks are currently the only JS-native mechanism that passes both.
