---
title: Open redirects: prefix-only guards die to control-character stripping in URL parsers
date: 2026-07-03
category: guardrails
tags: [security, open-redirect, owasp-a01, cwe-601, url-parsing, input-validation]
confidence: learned
source: private-work
---

A same-origin redirect guard that only checks for a literal `//` prefix (plus maybe a leading backslash) on a `next`/`redirect` query parameter is bypassable, and the bypass comes from a layer most developers never think about: the URL parser itself.

What happened: a login flow validated its post-auth redirect target by rejecting strings starting with `//` or `\`, intending to block protocol-relative URLs that point off-site. An attacker-controlled value like `/<TAB>/evil.com` (a path segment with an embedded tab, carriage return, or line feed before the double slash) sailed past that check — the leading character was `/`, not `/` `/`. But when the browser or a downstream WHATWG-compliant URL parser (the standard used by browsers and modern JS URL implementations) processes that string, it first strips ASCII tab, CR, and LF from the *entire* string before doing any parsing. That collapses the value to `//evil.com`, which is now a protocol-relative URL pointing at a different origin, and the browser happily navigates there post-login.

How to apply: never trust a prefix or substring check for redirect-target validation — it's checking the string before the browser's own normalization runs, not after. Instead: (1) strip or reject any control character (Unicode code points U+0000–U+001F, plus U+007F/DEL) from the input up front, then (2) resolve the remaining string against a known placeholder origin using the platform's URL constructor, and (3) assert the resolved result's origin equals that placeholder origin exactly. This origin-equality backstop catches every encoding or normalization trick that could re-trigger authority parsing, because by the time you compare origins, all parser-level normalization has already happened on both sides.
