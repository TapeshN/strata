---
title: Append-only ledgers race their own PRs — reconcile by set-union, never pick-one
date: 2026-08-09
category: orchestration
tags: [git, coordination, context-management, multi-agent]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

# Append-only ledgers race their own PRs — reconcile by set-union, never pick-one

Three related lessons from one incident window in a multi-session agent org.

**1. A git-tracked append-only ledger that also receives ambient local appends will race every PR that touches it.** Automation kept appending event lines to the local copy while a PR carrying the same file was in flight; refreshing the local checkout by plain pull would have silently discarded dozens of real local-only lines. On an append-only file, any pick-one conflict resolution (`--theirs` / `--ours`) loses one side **by construction**. The correct reconcile is a set-union: back up the local copy → extract local-only lines (`comm -13` on sorted copies) → take the merged version → re-append the local-only lines → verify by line count (merged + preserved = final).

**2. The context-limit WARNING is the knowledge-extraction deadline.** A gate that blocks a *manual* context compaction cannot block the *automatic* one racing right behind it — in the observed sequence, auto-compaction fired fifteen seconds after the manual path was blocked, with the extraction still owed. By the time anyone reaches for compaction, context is already at the ceiling and the unblockable path wins. Run the extraction sweep the moment the warning opens, while headroom remains; the gate is the backstop, never the trigger.

**3. Serialize multi-writer audit/judgment ledgers under a single coordinator authority.** The race class above is exactly what un-serialized writers produce. Once verdict-writing and ledger reconciliation belong only to the session holding the coordinator lock — child sessions bank raw material but never judge — the multi-writer race disappears structurally instead of being patched per incident.

Bonus corollary from the same sweep: a living status doc can contradict its own settled-decisions section, and a session will follow whichever line it read last. When refreshing a working-set doc, grep it for the nouns you are writing — a new status line must not contradict a standing settled entry.
