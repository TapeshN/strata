---
title: None and empty string produce the same HMAC message — gate on domain validity before the cryptographic check
date: 2026-06-20
category: guardrails
tags: [gating, determinism, contracts, interfaces]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a serialization format maps a language-level `None` to the same byte sequence as an empty string (as JSON does: `null` and `""` both serialize to the same suffix in a string concatenation), a cryptographic gate that signs the value before validating its domain can be bypassed by substituting one for the other. Both the null row and the empty-string row carry the same HMAC, so the signature check passes for either form — even though the application code branches on `is not None` and therefore takes different paths for each.

The fix has two parts. First, validate the field's domain explicitly before the cryptographic check: a field whose legitimate values are a known set of non-empty strings should reject the empty string and null immediately on receipt, before any HMAC comparison. Second, branch on truthiness rather than `is not None` in the dispatch logic, so the empty string falls to the default path regardless. Both guards are belt-and-suspenders: the gate-before-HMAC closes the collision class; the truthiness branch closes the dispatch gap.

The general rule: whenever `None` and `""` are both possible values for a field that feeds a cryptographic operation, treat the deserialization boundary as a collision source. Validate domain membership (the field is a non-empty member of the allowed set) before signing or verifying. This is a special case of the wider principle that type coercion at a serialization boundary should be treated with the same suspicion as user input.
