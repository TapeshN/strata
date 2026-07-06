---
title: Restoring a file with a plain version-control checkout during a neuter-and-verify test silently deletes uncommitted work instead of restoring it
date: 2026-07-06
category: guardrails
tags: [break-test, git-checkout-data-loss, causal-binding, cp-backup]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A standard way to prove a safety check is causally load-bearing is to temporarily neuter it, confirm the trigger test now fails, and then restore the original behavior. The natural way to "restore" a single file is a version-control checkout of that path from the last committed revision. That works cleanly only if the file's current, correct implementation was already committed before the neuter step. If the implementation being tested is itself still uncommitted — a very common situation right after writing a new guard — a checkout does not undo the temporary neutering; it reverts the file all the way back to the last commit, which predates the guard entirely, silently discarding the whole uncommitted implementation from the working tree. The failure is easy to miss in the moment because the "restore" step appears to succeed, and the damage only becomes visible later when something downstream fails on a now-missing piece of code.

The safe pattern for any neuter-then-restore verification cycle: before neutering, copy the target file to a temporary backup location with a plain file copy, make the temporary edit, run the trigger test, and restore from that copy rather than from version control. A version-control checkout should only be used to restore a file whose correct state is already safely committed.
