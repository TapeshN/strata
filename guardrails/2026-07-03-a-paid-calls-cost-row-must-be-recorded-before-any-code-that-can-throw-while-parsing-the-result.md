---
title: A paid call's cost row must be recorded before any code that can throw while parsing the result
date: 2026-07-03
category: guardrails
tags: [cost, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A cost-accounting feature's very first real, live test — a real, billed call to a language model — failed silently in an unusual way: the model's response was valid, well-formed content, but wrapped in a formatting artifact (in this case, markdown fencing) that the response-parsing code did not anticipate. The parser threw before the code ever reached the line that appends a usage row to the cost ledger. The call was genuinely billed; the ledger recorded nothing. Every synthetic test written for this path passed, because every synthetic test fed clean, pre-formatted content that never exercised the parser's failure mode.

The general shape of the bug: an accounting step placed *after* a parsing step that can throw on the real, imperfect shape of live output means any parse failure on a genuinely paid call silently drops that call's own cost record — the worse the parser, the more expensive the blind spot, since it fails exactly on real traffic and passes on every test that used clean fixtures.

The fix and the generalizable rule: record the measured usage or cost of any paid external call immediately after the response arrives — before any code that parses, validates, or otherwise processes the result and could throw — because the call has already been paid for regardless of what happens next. A synthetic test suite that only ever exercises clean, well-formed responses will never surface this class of failure; it requires either a live call or a fixture that reproduces the real formatting variance actually seen in production.
