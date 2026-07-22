---
title: A CSP that permits inline scripts must carry the sandbox directive on the RESPONSE, not rely on the consuming iframe's sandbox attribute
date: 2026-07-19
category: guardrails
tags: [security, csp, owasp-a05, embedding]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Content served under a Content-Security-Policy that permits inline scripts executes with its own first-party origin's full privileges the moment it's loaded directly — opened in a new tab, or shared as a link — because an iframe's `sandbox` attribute is enforced by the PARENT page embedding it, and only applies when the content is actually loaded inside that specific iframe. Two independent security reviews converged on the same finding from different angles.

**The rule:** if content permitting inline scripts might ever be loaded outside of a deliberately-sandboxing container, the server response itself must carry a `sandbox` directive (via the CSP header) so the browser treats it as an opaque, restricted origin regardless of how it's loaded — never rely solely on the embedding page's iframe attribute. Separately: a strict `connect-src` blocks fetch/XHR/WebSocket/beacon network calls, but NOT navigation-class egress (a location assignment, `window.open`, a meta-refresh) — don't claim a CSP has achieved "zero network" without accounting for navigation-based paths out.
