---
title: Verify a secret the way the runtime reads it, not the way a manual grep extracts it
date: 2026-06-16
category: guardrails
tags: [secrets, verification, env-vars, dotenv, false-alarm, rule-15]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A manual verification of a credential that uses a different extraction method than the runtime will produce false positives. A common case: a shell pipeline that greps a `.env` file strips double-quotes but not single-quotes. The runtime's dotenv loader strips both. The manually-extracted value arrives with literal quote characters that the API rejects, producing an "invalid key" error that reflects the extraction tool's bug, not the credential's validity.

When a credential check fails, examine the extraction method first. Print the first few characters of the extracted value and confirm they match the expected key prefix and character set, without surrounding whitespace or quote characters. A key that loads correctly in production and fails only in your manual harness is almost certainly a harness problem.

Two related disciplines:

First, when a self-written tool reports a failure, treat it as a suspect rather than as ground truth (rule 15 applied to your own tooling). A freshly-written extraction pipeline is more likely to have a bug than the credential system it is testing.

Second, any false "broken" verdict that has been written to durable records must be explicitly corrected — reversed in every document where it was recorded — not merely stopped being mentioned. A stale "blocked/dead" entry in a log produces wrong decisions for any reader who encounters it later.
