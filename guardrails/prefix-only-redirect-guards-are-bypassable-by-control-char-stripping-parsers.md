---
title: A prefix-only same-origin redirect guard is bypassable because URL parsers strip control characters before parsing — validate by parsed origin, not by literal prefix
date: 2026-07-03
category: guardrails
tags: [security, boundaries, contracts]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A same-origin check on a client-supplied redirect target that only rejects a literal double-slash prefix and backslash characters can still be bypassed. The standard URL parser used by browsers and many server runtimes strips certain ASCII control characters (tab, carriage return, line feed) from an entire input string before it begins structural parsing. A redirect target containing one of these characters embedded before a double-slash sequence — for example a tab character followed by what looks like a path — is not caught by a literal-prefix check, because the literal string does not start with `//`. After the parser silently strips the control character, the resulting string does begin with `//`, which the parser then treats as protocol-relative, resolving to a different origin entirely. A prefix check operating on the raw, unstripped string never sees the danger the parser will later construct.

The generalizable, airtight pattern: first reject any input containing a control character in the C0 range or the DEL character outright, so no parser-level normalization can later manufacture a delimiter that wasn't visibly present. Then validate the redirect target by resolving it against a known-safe placeholder origin using the runtime's own URL parser and asserting that the resulting parsed origin equals the placeholder — letting the same parser that will eventually be trusted to interpret the URL be the one that validates it, rather than re-implementing a subset of its normalization rules by hand by inspecting the raw string. A prefix or substring check on the raw string is never sufficient for redirect-target validation, because it can only catch dangers that are already visible in the input, not ones a downstream parser's normalization step will create.
