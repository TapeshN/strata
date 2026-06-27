---
title: An external CLI wrapper must defend against interface drift with a shape fallback, a conservative classifier, and a live smoke witness
date: 2026-06-11
category: infra
tags: [ci, gating, determinism, contracts, versioning, tooling]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A tool that wraps an external CLI can pass all its mocked unit tests and then fail silently in production the moment the CLI's output schema changes. Mocked tests assert the tool's logic against a fixed schema; they cannot catch that the CLI itself no longer emits the field the tool reads.

The failure mode is treacherous because it looks like a correct execution. The wrapper returns a verdict, the gate reads it, and the gate acts — but the verdict is wrong because the absent field defaulted to something the code never intended. In one observed case, a field rename in a minor CLI version upgrade caused a merge-ceremony tool to immediately park every queued task; the tool's tests were entirely green.

Three defenses make this class recoverable without re-mocking the world:

First, fetch two field shapes: the current shape first, the prior shape as a fallback triggered only when an unknown-field error is detected. This lets the tool continue working through a CLI version boundary without a breaking release of its own.

Second, classify unknown values conservatively. When a signal field carries an unrecognized value, the safe verdict is PENDING (do not merge yet), never APPROVED (merge now). A conservative classifier preserves safety when information is absent.

Third, the definition of done for any CLI-wrapping tool must include a live smoke test run against the real CLI — not just a mocked suite. The mocked suite proves the logic; the live witness proves the interface assumption is still valid. This witness should be part of the merge checklist for any PR that modifies the wrapper.
