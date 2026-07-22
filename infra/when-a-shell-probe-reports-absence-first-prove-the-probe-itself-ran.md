---
title: When a shell probe reports absence, first prove the probe itself ran
date: 2026-07-22
category: infra
tags: [shell, tooling, macos, false-negative]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A command commonly assumed to exist on every Unix-like system (a coreutils-style timeout wrapper) isn't actually present on every platform by default — and piping such a missing command into a filter can fail SILENTLY, producing "no output matched" rather than an obvious "command not found" error, which reads exactly like a real feature genuinely being broken. Debugging effort went into "fixing" code that was never broken, purely because the probe used to check it never actually ran. A related trap in some shells: certain variable-expansion syntaxes accept history-style modifier suffixes that silently rewrite the variable's value rather than erroring, mangling a value used later in the same command without any visible failure.

**The rule:** when a probe reports an absence or a negative result, first confirm the probe itself executed as intended (check its own exit status, or a trivial known-true case) before concluding the thing it's probing is actually missing or broken — and quote/brace shell variables defensively so an unexpected expansion modifier can't silently alter their value.
