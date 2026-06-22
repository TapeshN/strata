---
title: A monitoring signal must read from something the monitored activity actually changes
date: 2026-06-16
category: guardrails
tags: [determinism, evals, loop, gating]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A factory-state indicator reported that the system was idle while a full wave of work was actively running. The signal read from two sources: a process identifier check via the OS process interface, which returns "dead" inside a container because the host process namespace is not visible; and a file-freshness check on a path that does not exist inside the container. Both sources fell through to an idle default. The signal was structurally unable to report any state other than idle, regardless of what was actually happening.

The failure pattern generalizes: a liveness or activity signal that reads from a data source the monitored activity does not write to will always return the wrong answer. The monitor is disconnected from the thing it is supposed to observe.

The correct design: identify what the monitored activity actually changes — a ledger it appends to, a state file it updates, a counter it increments — and read that. If there is no such artifact, the activity is not observable by a signal, and the signal should report "unknown" rather than a fabricated state.

A signal that always reads one value regardless of actual system state is worse than no signal. It does not just fail to help; it actively misdirects decisions made against it.
