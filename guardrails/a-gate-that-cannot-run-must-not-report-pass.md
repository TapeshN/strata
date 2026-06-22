---
title: A gate that cannot run must not report pass — distinguish cannot-run from ran-and-passed
date: 2026-06-14
category: guardrails
tags: [gating, evals, judge, determinism, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A quality gate had a dependency on an external judge that was not available in the running environment. Instead of reporting that it could not run, the gate returned an in-sync status, reporting the backlog as fully processed. The backlog was not processed. Every item in it was still undeposited. The false green propagated through the session as an established fact.

The failure mode: a gate whose execution depends on an external resource (a model API, a credential, a network service) silently returns a passing verdict when the resource is absent, rather than surfacing the missing dependency. A downstream system treats the passing verdict as evidence that everything is fine.

The correct behavior for any gate that cannot execute: return a clearly distinguished status — something like "could not run" or "skipped: dependency unavailable" — not "passed." The three states a gate must be able to distinguish are: ran and passed, ran and failed, and could not run. Conflating the third with the first is a silent failure that creates false confidence in the entire system.

This applies equally to automated quality judges, CI steps with missing secrets, health checks with unreachable backends, and any other gate whose execution path has a prerequisite. The prerequisite check must come first; its absence must be surfaced, not swallowed.
