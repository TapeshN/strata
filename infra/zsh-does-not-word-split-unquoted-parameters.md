---
title: zsh does not word-split unquoted parameters — bash-semantics argument splitting silently corrupts batch loops
date: 2026-06-10
category: infra
tags: [shell, zsh, portability, batch-operations]
confidence: learned
source: private-work
---

In bash, `set -- $pair` splits an unquoted variable on whitespace into positional arguments. In zsh, the same line passes the entire string as a single argument — no splitting occurs. A batch of ten board mutations built on the bash idiom failed in zsh with errors of the form "could not resolve node id '<id> <number>'": each command received the two intended arguments fused into one.

When a script must run under zsh, either use a `while read a b` loop (the `read` builtin splits identically in both shells), or request splitting explicitly with zsh's `${=var}` expansion. This is the same trap family as inline `#` comments inside pasted command blocks, which interactive zsh also handles differently than bash scripts: zsh is not a drop-in superset of bash, and batch one-liners written from bash muscle memory are where the difference lands.
