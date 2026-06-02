---
title: A gate's status is a claim — produce it by running the real gate, not a proxy or its docstring
date: 2026-05-31
category: guardrails
tags: [gating, verify-dont-trust, ip-boundary]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Two incidents, one root cause. (1) An ad-hoc content scan piped a raw pattern file — including its blank lines — into a `grep -f` count. A blank line is an empty pattern that matches every line, so the scan reported a phantom match and held a clean commit. The production gate strips comments and blanks and was fine; only the *documented ad-hoc command* was buggy. (2) Separately, the behavior of a boundary gate was asserted from its *docstring* ("fails closed if unset") rather than its code — which actually fell back to a default file and ran normally. The "blocked, must relaunch" claim was wrong; a real commit went through clean.

General lesson: "the gate passed" and "the gate blocked" are both claims that require *running the real gate, clean* — not a hand-rolled proxy, not the docstring, not a cached summary. When you must scan ad-hoc, strip comments and blank lines before `grep -f`, and always report counts, never echo matched terms. The authoritative decision is the production gate's, produced live.
