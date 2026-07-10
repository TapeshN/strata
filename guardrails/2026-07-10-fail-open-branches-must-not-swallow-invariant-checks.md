---
title: Fail-open branches must not swallow invariant/identity checks
date: 2026-07-10
category: guardrails
tags: [fail-open, invariant-checking, security, error-handling, code-review]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A fail-open branch designed for tolerance — a shadow mode, a dark-launch path, a "never refuse the user" best-effort fallback — will swallow an integrity or identity-verification failure exactly as readily as it swallows the transient failure it was built to tolerate. If the only thing standing between a forged or malformed object and a privileged operation is a downstream error that a lenient catch-all treats as "eh, proceed anyway," then a forgery that trips that exact error sails through completely unblocked.

What happened: a system had two operating modes — a strict "enforced" mode and a lenient "shadow" mode meant to let traffic flow even when some internal bookkeeping error occurred, so real users wouldn't get blocked by transient glitches. An object that failed to carry the expected internal marker (created via a low-level object-construction path that bypassed the normal constructor) threw a TypeError when the code tried to read a private field that only genuine objects have. In enforced mode, that TypeError got caught and correctly rethrown as a hard refusal. In shadow mode, the same TypeError landed in a "proceed on any internal error" catch block and was silently swallowed — so the forged object sailed through completely unchecked. The protection in enforced mode was accidental: it depended on an error happening to propagate the right way, not on an explicit check.

How to apply: whenever you add or review a fail-open / best-effort / shadow path, audit it specifically for whether it can also swallow an invariant check — an identity, authentication, or capability verification — not just the ordinary errors it was designed to tolerate. The fix is to move the identity/capability check to the very top of every gated code path, before the mode branch, and have it throw a typed, explicit refusal on failure — never rely on an incidental downstream error type to do that job. A fail-open mode should fail open only for the failures it was designed for; verification must run unconditionally, ahead of any tolerance logic.
