---
title: "An always-dirty file ends everyone's ability to read git status — and a red that belongs to no one is a red nobody fixes"
date: 2026-08-12
category: guardrails
tags: [repo-hygiene, verification, gates, ci, triage]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

# An always-dirty file ends everyone's ability to read git status

A machine-written runtime artifact was tracked in git. It changed on every run,
so `git status` was never clean — and once a repository is *never* clean,
nobody reads the output any more. That is not one messy file. It is the end of
everyone's ability to notice any *other* messy file, which is the whole point of
the signal.

**Prevention.** A machine-written runtime artifact does not belong in version
control. When a repository has a path that is dirty on every single
`git status`, treat it as a P1 in its own right, not as background noise you
learn to scroll past.

## Triage the mess before believing it is one

The same repository looked alarming: seventy dirty paths, including a set
described as "unreviewed deletions". The instinct was to defer it as a big
cleanup. The cheap classification took minutes and dissolved most of it — the
deletions were an artifact of comparing against a stale reference, and the
majority of the remaining paths were the always-dirty artifact and its
neighbours. Very little real judgement was required.

**Prevention.** Before deferring a repo-state mess, run the cheap
classification: for each path, does the local content still contain everything
the remote has? A *count* of dirty paths says nothing about how much judgement
is actually needed — and the scary-sounding subset is precisely the part most
likely to be an artifact of a stale ref.

## The newer file can be the one that looks like it lost content

Two versions of a working document differed, and the shorter one looked like it
had lost content — so the longer one looked newer. It was the reverse: the
document is kept under a compaction discipline, where shipped items are evicted
on purpose. Shrinking *was* the update.

**Prevention.** For a document under a compaction discipline, line count is not
recency. Read what the two versions **say** before ruling on which is ahead — a
working set is supposed to shrink.

## A red that belongs to no one is a red nobody fixes

A pull request failed on a check that had nothing to do with its diff. The
check had been failing on the main branch for months. Every author who tripped
over it had reasonably concluded "not mine" and moved on, so it stayed red
indefinitely — a real defect with no owner.

**Prevention.** When CI fails on something outside your diff, check whether the
main branch is already red before treating it as your problem *or* as someone
else's. An inherited red is a genuine defect that nobody owns, and the pull
request that trips over it is holding the cheapest opportunity anyone will ever
have to close it. Fix it rather than adding an exemption.

## Answer a blocked overwrite with a move, not a delete

A checkout refused to proceed because untracked local content would be
overwritten. That refusal is version control protecting content it cannot
recover for you. Renaming the file aside made the operation succeed *and* left
a diff that could be shown; deleting it would have made the same symptom go
away with nothing left to compare.

**Prevention.** A blocked operation of this kind is a warning about data you
have not looked at. Answer it with a reversible move plus a comparison you can
show, never with an irreversible delete and a shrug.
