---
title: A safety floor backed by discovered data must UNION with its baked-in baseline — and a gate only covers the scope you actually run it in
date: 2026-08-23
category: guardrails
tags: [gate-design, ci, boundaries, identity]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A merge floor decided whether a given repository belonged to the protected class that may not be merged without an explicit human grant. It started life with a hardcoded set of repository names and was later "improved" to read a runtime registry instead. Whenever that registry returned anything at all, it REPLACED the hardcoded set — so the floor's coverage silently shrank to whatever happened to be cloned on the machine running it. Compounding that, the two sources spelled the same repository differently, one carrying full directory names and the other short names, so membership tests missed even for repositories present in both. The floor kept reporting a healthy verdict while quietly declining to protect the things it existed to protect. The failure was also order-dependent under test — another suite left a fixture-bound module cached in the interpreter — which is why several passes went by without anyone seeing it.

Two rules come out of that. First, a safety predicate backed by DISCOVERED data must be monotone: discovery may ADD to the baked-in floor and must never subtract from it. Any code path where "we found a list" replaces "we know this minimum" is a fail-open waiting for an empty or partial discovery. Second, when one concept is spelled two ways, normalize at the COMPARISON rather than at one producer — the same twin-identity failure documented elsewhere in this corpus, in its quieter naming form.

The same week produced two more green signals that were green only because of what they never ran.

A work lane's own gate command ran the tests that lane owned, while the repository-wide contract test that must register every cross-service route lived in a different part of the tree. The change added two new routes, every local gate passed, and continuous integration failed on that single test. A gate you forgot exists is still a gate — and a change that introduces a new interface must run the contract test that OWNS that interface, in the same commit that registers it.

And the hosted continuous-integration runner used a newer language runtime than the machine that actually executes the tooling in practice. Three constructs valid on the newer runtime — a union type written in value position, and a timestamp parser that only accepts a trailing zone designator in later versions — failed at runtime on the production interpreter, one of them badly enough that an entire suite could not even be collected. A lint that checks only type annotations cannot see any of them. The interpreter that runs a tool in production is the interpreter its tests must run on before the change is called done.
