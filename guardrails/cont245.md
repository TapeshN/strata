---
title: "I ran my own gate, it FAILED, and I pushed anyway — because I ran it as a separate line instead of gating the commit on it"
date: 2026-09-08
category: guardrails
tags: ["gate-not-in-the-chain", "exit-code-unconsumed", "directory-vs-repo", "wrote-the-gate-then-ignored-it"]
confidence: learned
source: private-work
---

a verification command must be IN the chain it guards — `check && commit && push`, never `check` on one line and `commit && push` on the next. A gate whose exit code nothing consumes is a print statement.

this is the same shape as the gates banked in an earlier entry, one level up. Those were mechanisms that reported success while doing nothing; this is a mechanism that reported FAILURE correctly and was ignored by its own caller. **Reading a gate's output is not the same as obeying it** — and I am the one who wrote both the gate and the caller, in the same session, having spent the night telling workers that a green check is not a witness.
