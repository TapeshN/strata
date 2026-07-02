---
title: An agent writing a plausible-looking but unsourced value into a system of record has fabricated data, and only a provenance check catches it
date: 2026-07-02
category: guardrails
tags: [verify-dont-trust, contracts, autonomy]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An automated data-entry task produced a contact address that was never present in any of its source material — it was algorithmically derived from a known domain name using a plausible naming convention, for a record whose actual source material only specified a website and an alternate, non-email contact channel. The value looked entirely legitimate and passed the task's own adversarial review, because that review checked security properties (scoping, safety, whether an outbound message would actually be sent) rather than where each individual value had come from. It was only caught by a human deliberately searching for that literal string across every known source document and finding no match.

The generalizable rule: in any system of record fed by automated agents, an honest placeholder is strictly better than a plausible guess, because downstream automation that later acts on that field (a follow-up message, an outreach campaign) will treat a fabricated value exactly the same as a real one and act on it without knowing the difference. The review procedure for any agent-written "real-looking" data should include a provenance pass — grep or otherwise trace each individual value back to an actual source document, since anything with no traceable origin is fabricated by definition, regardless of how plausible it looks. Verifier prompts for any data-entry task should include a provenance axis explicitly, not just security axes — a verifier only ever catches what its checklist actually names.
