---
title: An edit-interception hook cannot be an adversarial security boundary — gate on the one property an attacker cannot forge
date: 2026-07-13
category: guardrails
tags: [security, hooks-semantics, path-auth, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A safety mechanism was built as a pre-write interception hook: before any file-editing tool ran, it checked whether the target path belonged to a protected area and, if so, blocked the edit unless an on-disk marker proved the caller held an exclusive claim on that area. Across four successive adversarial reviews, each fix closed one forgery route and opened, or left open, another: a forged marker file; a forged back-pointer that the tool used to resolve which protected area a path belonged to, which a legitimate-looking list command echoed back without verifying it against anything signed; a case-sensitivity gap on a case-insensitive filesystem that let a differently-cased path alias the protected one; and a substring match on a protected-looking folder name that could be satisfied by creating a same-named subfolder anywhere in the tree. The reviews eventually converged on a deeper realization: the entire class of bypass was possible because the interception point itself only covers one category of write action — a caller using a lower-level, more general execution primitive can always reach the filesystem directly, going around the hook entirely, no forgery required.

The structural fix was to key the gate on the canonical, filesystem-resolved form of the actual target path — the one input a caller cannot forge, because it is the operation being gated — rather than on any adjacent marker, back-pointer, or naming convention that has to be trusted. The broader lesson: a hook that only intercepts one class of action is collision-prevention for cooperating callers, not an adversarial security boundary, and no amount of patching the marker logic changes that. Know the enforcement point's actual reach before claiming a security property for it, and give any safety gate that gets rewritten a fresh, independent adversarial review rather than reusing the same attacker mental model that was already defeated once.
