---
title: A token-level theme change only recolors what was tokenized — grep the source AND the deployed asset
date: 2026-07-21
category: guardrails
tags: [css, verify-dont-trust, deploy-witness, design-systems]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Rewriting every design-token value in a stylesheet and confirming the result live in a browser feels complete, but component-level rules deep in a large stylesheet can still hold hardcoded literal color values that were never routed through a token in the first place — invisible to both the token-rewrite pass and to a casual visual look, because they sit far down the file and a quick scan doesn't surface them. Only an explicit search for raw literal values outside the token declarations themselves reliably finds them.

**The rule:** after any theme or design-token change, grep the SOURCE for raw color literals outside the token block and treat every hit as a decision (route it through a token, or explicitly justify leaving it hardcoded) — a browser look only confirms what you happened to scroll past. Separately, grep the actual DEPLOYED asset too, not just the source: the deployed build is what a user actually receives, and a source-only review can pass clean while a stale or partially-propagated deployed asset still serves the old values.
