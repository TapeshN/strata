---
title: A denylist on an attacker-controlled field is unwinnable — allowlist it
date: 2026-06-20
category: guardrails
tags: [gating, autonomy, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A gate that matches a declared action field against a set of known-bad values is structurally unwinnable. The attacker controls the field; they can always supply a value that is not yet on the denylist — an invented verb, a unicode invisible character, a whitespace variant that survives ASCII strip but not unicode strip, or a homoglyph. Each round of patching enlarges the denylist without closing the input space. Two independent red-teams confirmed this empirically: after patching a whitespace bypass, a round-two pass found twelve additional Unicode format characters (zero-width, soft-hyphen, BOM, fullwidth space) that `str.strip()` does not remove, plus any novel string not in the set.

The correct structure is an allowlist: accept only values that belong to a fixed, explicitly enumerated set of legitimate inputs (preferably lowercase ASCII). Any value outside the set is rejected at the gate, before the cryptographic check. An exact-membership test against a closed set admits no transform — unicode, case, substring, homoglyph — because the transform produces a string that is simply not in the set. A single round-two adversarial pass on the allowlist-based gate found zero survivors across two-hundred-plus crafted variants.

The broader principle: any field that an attacker controls and that a gate inspects for "bad" patterns should be allowlisted, not denylisted. Denylist gates belong only on outputs or on fields whose input space is already bounded by a prior allowlist elsewhere.
