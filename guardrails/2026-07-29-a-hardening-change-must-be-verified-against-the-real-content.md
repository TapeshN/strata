---
title: A security-hardening change must be verified against the real content it protects, not just the policy string
date: 2026-07-29
category: guardrails
tags: [gating, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
efficacy: decorative
---

Two independent breakages in one day traced to the same root cause. A hardening pass on a content-security policy was reviewed and tested at the level of the header string — does it parse, does it contain the expected directives — and shipped green both times. In practice, one policy misplaced a needed grant onto the wrong directive and let a resource class fall through to a default-deny, so an embedded application never mounted; a second policy granted a resource type to the wrong element category, so a bundle whose assets were inlined as data blobs silently fell back to a degraded default.

The lesson: a content-security or sandboxing policy is only correct relative to what the content actually needs, and testing the policy in isolation from the content it serves proves nothing about that. Any change to a hardening policy on a content-serving route should ship with a fixture that exercises the actual resource classes the served content uses, plus one live render check before merge comparing behavior under the old and new policy. Grants should be justified by an observed need in the real content, not by a plausible-sounding guess — and the standing rule that any loosening of a security boundary needs independent adversarial review still applies in full; this lesson is specifically about verifying a tightening against reality too.
