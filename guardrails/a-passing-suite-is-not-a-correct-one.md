---
title: A passing test suite is not a correct one
date: 2026-05-30
category: guardrails
tags: [verify-dont-trust, evals, determinism, subagents]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

While hardening a safety gate, an adversarial verify stage caught a false-positive regression the builder's own large test suite had missed: a widened destructive-command guard matched flag-like substrings *inside quoted strings*, so a commit whose message merely mentioned a flag would have been wrongly blocked. The builder's tests had only positive cases — they proved the gate fired when it should, never that it stayed quiet when it shouldn't.

Two durable fixes: (1) flag/verb detection must be token-aware — split the command with a shell lexer and inspect tokens, never raw-regex over the whole line, so a quoted message or a URL path that mentions a flag isn't read as *using* it; (2) lock behavior with live *negative* probes, not just positive ones.

General lesson: a green suite means "the cases I wrote pass," not "the code is correct." Independent adversarial verification — especially the negative cases the author never thought to write — is where real defects surface before they ship.
