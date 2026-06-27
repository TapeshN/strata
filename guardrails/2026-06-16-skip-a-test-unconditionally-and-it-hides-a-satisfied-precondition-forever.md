---
title: An unconditional skip that documents a missing precondition hides a satisfied one forever once the precondition ships
date: 2026-06-16
category: guardrails
tags: [testing, hollow-test, gating, lifecycle, verify-live-state]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A test with an unconditional skip says "this precondition is absent." When the precondition is eventually installed, the skip stays — now documenting a falsehood. The test reads green and reveals nothing. The capability it was meant to guard is live and unguarded.

This failure is a deferred version of the hollow-test pattern. When a skip was written, it was honest. It becomes dishonest only later, when something external changes and the test is not revisited. Because the skip looks like correct test discipline (skip what you cannot run), no one is alerted.

The practical consequence: a suite can show 100% passing while silently omitting assertions for every capability that was installed after its test was written. The suite proves the state of the world at the time the tests were authored, not the current state.

Two practices prevent this. First, when a capability ships, the person shipping it should search the test suite for unconditional skips that reference that capability by name and flip each one to a real assertion with a conditional skip (skip only when the artifact is genuinely absent). Second, a skip that says "X is not installed" should check live whether X is installed, not assume. A skip with a live check degrades correctly if X disappears again; an unconditional skip is always wrong once X arrives.

The reflex: landing a capability means owning a grep of the test suite for its name.
