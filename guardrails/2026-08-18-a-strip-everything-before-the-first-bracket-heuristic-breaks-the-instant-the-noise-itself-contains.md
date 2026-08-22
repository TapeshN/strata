---
title: A "strip everything before the first bracket" heuristic breaks the instant the noise itself contains that bracket
date: 2026-08-18
category: guardrails
tags: [extraction, verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A third-party API prepended several kilobytes of unrelated diagnostic warning text ahead of every
JSON response body. The obvious fix — strip everything before the first opening-bracket or
opening-brace character — failed outright, because the diagnostic warning text ITSELF happened to
contain bracket characters. The working fix instead anchored on a short STRUCTURAL pattern that
can only occur at the true start of the intended payload (an opening bracket, followed by
whitespace, followed by an opening brace, followed by whitespace, followed by a quote character) —
a shape the surrounding noise text could not itself produce.

The generalizable rule: any "strip the noise prefix" step must anchor on a pattern that provably
cannot occur within the noise itself, and must be verified against a REAL noisy sample of the input
— not a clean, hand-constructed fixture — before being trusted.
