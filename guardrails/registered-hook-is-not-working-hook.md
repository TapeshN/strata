---
title: A safety hook that is registered but has a defect provides zero protection
date: 2026-06-06
category: guardrails
tags: [gating, ci, verify-dont-trust, lifecycle]
confidence: learned
source: private-work
---

A safety hook that is registered in a settings file but whose implementation has a defect will silently degrade: it may return a stale default on its first call, crash on import in a different runtime environment, or fail to load entirely. In all these cases the gate reads as registered while enforcing nothing.

Concrete defects found: a hook that cached a stale default on the first call and never read the halt file it was supposed to check; hooks that crashed on import because a standard library module behaved differently in an older runtime.

Prevention: every safety gate must ship with a failure-trigger test that proves the gate actually fires (returns a blocking result) when given an input that should trigger it. "Registered" is not the same as "working." This is a sibling of "gates that are never run are fiction" — the distinction is that a registered-but-defective hook may be harder to notice, because it appears to run.
