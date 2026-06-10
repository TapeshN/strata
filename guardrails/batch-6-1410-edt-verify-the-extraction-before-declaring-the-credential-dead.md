---
title: Suspect extraction before declaring a credential dead
date: 2026-06-10
category: guardrails
tags: [preflight, determinism, evals, judge]
confidence: learned
source: private-work
---

When an API call returns a 401, the instinct is to declare the credential invalid. That instinct is often wrong. The more likely culprit — especially in a session involving hand-rolled environment-variable extraction — is that the extraction itself is mangling the value. Quote characters, carriage returns, or trailing whitespace that look invisible in a terminal are invisible to casual inspection but fatal to an HTTP auth header. A pipeline that strips only double quotes will silently leave single quotes attached; a pipeline that reads a raw line without invoking the shell's own source semantics can pick up characters that dotenv-aware loaders discard automatically.

The diagnostic that reliably cracks this is printing the length and character-class profile of the extracted value — quoting presence, whitespace presence, byte count — without ever printing the value itself. A clean credential and a quote-mangled credential look identical in most log lines but differ by exactly the count of extra characters introduced.

The downstream consequence is more serious than a single failed request. When an evaluation harness or judge component draws its credentials from the same extraction path, every verdict it produces during the mangled-key window is instrument error, not content signal. Failures scored as zero are not evidence of a gap in the system under test; they are evidence of a broken thermometer. Accepting those verdicts at face value queues unnecessary remediation work and, worse, gives false confidence that real failures were caught and addressed.

The generalizable rule: before escalating a 401 to "credential is dead," re-test using a verified-clean extraction — shell source, a dotenv-aware loader, or an explicit character-audit of the raw bytes. Treat the extraction as the first suspect, not the last resort. This is the same discipline as checking instrument calibration before trusting a surprising measurement.
