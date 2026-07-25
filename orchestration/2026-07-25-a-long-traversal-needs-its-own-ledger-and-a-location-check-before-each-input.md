---
title: A long traversal survives context exhaustion only if it writes its own ledger as it goes, and needs a location check before every input
date: 2026-07-25
category: orchestration
tags: [context-window, lifecycle, determinism, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A verification pass that walks many independent items one at a time — flows through an application, records in a migration, endpoints in an API surface — can run long enough for a working session to run low on context before every item is covered. If progress only lives in the session's own reasoning, hitting that limit mid-pass loses everything not yet folded into a final summary, including items that were already fully verified.

The durable pattern is to append one row to an on-disk record the moment each item's verdict is reached, not at the end of the pass. When the session's context runs out partway through, that record already holds every completed verdict; a resuming session can pick up from the next unrecorded item instead of re-deriving what was already walked, and nothing already verified is lost even if a closing summary never gets written.

A related discipline from the same kind of pass: before typing into what looks like the right input on a page, confirm which page you are actually on. An earlier step in the same flow can silently redirect to a different route, and the first available text field at the new location may belong to an entirely unrelated feature that happens to occupy the same screen position as the one intended. Typing without checking can submit a value through the wrong feature's input rather than the one meant to be exercised. Reading the current route immediately before typing into a composer-style field is a cheap, general check against this class of misdirected input, and it matters most in exactly the long, multi-step traversals where a durable on-disk ledger is also earning its keep.
