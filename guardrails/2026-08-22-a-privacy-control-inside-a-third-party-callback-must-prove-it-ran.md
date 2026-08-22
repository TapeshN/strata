---
title: A privacy/masking control implemented as a third-party library's callback must prove the hook actually ran
date: 2026-08-22
category: guardrails
tags: [security, privacy, widget]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A screen-capture feature masked sensitive elements using a callback hook exposed by a widely-used rasterization library. When a host page already defined a global with the same name as that library — an older bundled copy, or a compatibility shim — the library's own internal wiring silently skipped invoking the masking hook. No error was thrown, and an unmasked capture would have been captured and stored. The feature's "fail-closed on error" design was real, but it only covered the path where the library actually threw; it said nothing about the path where the hook was simply never invoked.

Fix: set an internal flag from inside the hook itself, and discard (never persist) any capture where that flag was never set — the presence of output is treated as untrustworthy until the hook's own execution is separately confirmed. Load a pinned, private-scoped copy of the library so a host page's own global can't intercept it, and add integrity checking on the loaded bytes.

General rule: any privacy or security control that depends on a third-party library correctly invoking your callback must independently verify that invocation happened — never assume "no error" means "the hook ran." Test the specific "hook never invoked" failure mode against the real library in a realistic host environment, not just a harness that always calls your callback correctly.
