---
title: An iframe embed is governed by TWO independent CSP policies — verify both, and witness the actual rendered frame
date: 2026-07-19
category: guardrails
tags: [security, csp, owasp-a05, embedding]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Making one origin embeddable inside another as an iframe requires satisfying two SEPARATE policies enforced by two different parties: the embedded content's own `frame-ancestors` (or legacy X-Frame-Options) header, which the CHILD controls, and the embedding page's own `frame-src` Content-Security-Policy directive, which the PARENT controls. A review had already verified the child side (the embedded content permits framing) but the parent's own CSP configuration only allowlisted a couple of existing origins in its `frame-src` — so a newly-added, otherwise-fully-permitted embed target was silently blocked by the wrong half of the contract. Both prior reviews and CI were green; the gap only showed up in a live render of an embed combination that had never actually existed before.

**The rule:** any "can origin X embed origin Y" check must enumerate BOTH policies, and the only real witness is the actual rendered frame in a browser — neither header alone proves the embed works. Where possible, derive the parent's allowlist from the same single source of truth that governs which origins are permitted to be embedded at all, so a newly-allowed target can't pass one gate and silently fail the other.
