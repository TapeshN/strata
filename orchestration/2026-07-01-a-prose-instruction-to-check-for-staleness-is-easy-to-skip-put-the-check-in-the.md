---
title: A prose instruction to check for staleness is easy to skip; put the check in the output contract instead
date: 2026-07-01
category: orchestration
tags: [fan-out, subagents, verify-dont-trust, contracts]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Two parallel inspection agents given the same briefing — including an explicit instruction to check for repository drift before reading — returned opposite facts about the same underlying system. One had followed the instruction (checked how far its checkout was from the canonical remote branch before reading, and read from the remote when it found drift) and reported correctly. The other read directly from a local working copy that was several commits behind, without checking, and built findings on an absence that was no longer true — the thing it reported missing had already landed.

The root cause: a "check divergence first" instruction living only in prose briefing is something an agent can skip under time or token pressure, and nothing mechanical forces it. A working copy sitting a small number of commits behind the canonical branch, while still nominally on the right branch, is also easy for any automated drift-warning to miss if that warning only fires on being on the wrong branch entirely, not on being behind while on the right one.

Two fixes generalize. First, when fanning out multiple inspectors over shared, possibly-stale checkouts, put the divergence check inside the required structured-output contract itself — a mandatory field like "verified against: <ref>@<commit>" — so an inspector that cannot honestly fill that field cannot return findings at all, rather than hoping the prose instruction was followed. Second, when two independent inspectors disagree on a factual claim, treat it as a provenance question first (which source did each one actually read?) before treating it as an analysis disagreement — this is also the argument for deliberately keeping some redundant coverage across parallel inspectors on any load-bearing claim, since the redundancy is what made the contradiction visible at all.
