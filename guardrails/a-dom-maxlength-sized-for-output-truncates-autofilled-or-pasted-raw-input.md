---
title: A DOM maxLength sized for a field's formatted output truncates autofilled or pasted raw input before any normalizer runs
date: 2026-08-30
category: guardrails
tags: [forms, autofill, client-validation, mobile-web]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A phone-number input used a DOM-level maxLength attribute sized for the field's formatted display length, intended as a simple guard against overlong input. Mobile autofill inserted a longer raw string — an international number carrying a country code and separators — that the browser truncated at the DOM cap before the field's own input handler, which correctly strips the country code and formatting, ever ran. The result was a silently mangled, truncated value saved with no error surfaced anywhere. The DOM cap had been sized for the field's OUTPUT shape, not the range of raw strings that autofill or paste can insert into it. The fix was to drop the DOM-level maxLength entirely and let the field's own per-event formatter be the single length authority.

General rule: on any input field that can receive autofilled or pasted text in a different shape than its displayed format, a DOM-level length cap is a truncation bug waiting to happen, not a safety guard. Length and shape validation belongs in the input's own normalizer, which runs on every event, never in a static HTML attribute that runs before the normalizer ever sees the value.
