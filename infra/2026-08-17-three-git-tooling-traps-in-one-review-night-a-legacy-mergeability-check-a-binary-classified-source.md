---
title: Three git-tooling traps in one review night: a legacy mergeability check, a binary-classified source file, and identical-wrong auto-merges
date: 2026-08-17
category: infra
tags: [git, merge-safety, verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A reviewer checked whether two sibling branches would merge cleanly using a three-positional-
argument invocation of git's merge-tree command, and got "0 conflicts." Re-running with the
modern two-argument form (which derives the merge base automatically) surfaced six real conflicts,
two of them structural. The three-argument form is a legacy, trivial-merge-only invocation that
silently misreports when used bare; sibling-branch mergeability should always use the modern
form. The reviewer caught this only by doubting an answer that seemed too clean and re-running it
a different way — that instinct is the transferable lesson as much as the specific flag.

Separately, a source file that used literal NUL-byte characters as an internal separator caused
git to classify the ENTIRE file as binary, so a substantial set of changes to it showed up in every
pull-request diff as an opaque "binary file changed" notice — invisible to any reviewer who trusts
the diff view. Any source file should avoid non-text bytes (use an escaped representation that is
runtime-identical) specifically so it continues to diff as text; a review blind spot is
indistinguishable from a clean file until someone opens the raw bytes.

Finally, two independently-built parallel branches both appended new entries to the same registry-
shaped file and both updated a hand-maintained total-count assertion in its test — to the SAME
wrong number. A naive accept-both merge would have interleaved the two branches' list insertions
into syntactically broken code, but because both branches' count-line edits were textually
identical, git's automatic merge accepted them without ever flagging a conflict, silently locking
in the wrong number. Any file where parallel batches append same-shaped blocks and separately
maintain a derived total is a structural-conflict surface: reconcile by reconstructing each
batch's addition as a whole unit, and always RE-DERIVE the total from the merged data rather than
trusting either side's — or the reconciler's own — arithmetic.
