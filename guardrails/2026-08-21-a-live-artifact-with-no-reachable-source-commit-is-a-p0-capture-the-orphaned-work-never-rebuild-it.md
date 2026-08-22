---
title: A live artifact with no reachable source commit is a P0 — capture the orphaned work, never rebuild it from the trunk
date: 2026-08-21
category: guardrails
tags: [provenance, release, client-safety]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A live deployed artifact carried a build identifier that resolved to no commit in any checkout and
no matching commit on the remote — the actual source turned out to be a combination of a merged
pull request's head, several additional local-only commits, and hundreds of uncommitted files
sitting in an isolated working copy. Simply rebuilding "from the trunk" — the seemingly obvious
recovery path — would have silently discarded all of that unrecoverable local work, exactly the
outcome that had been explicitly ruled out.

The generalizable rule: when a live artifact's declared source cannot be resolved to a commit that
exists anywhere on the remote, treat it as a P0 data-loss risk, not a routine rebuild. The correct
recovery is to commit the orphaned working copy verbatim onto a reviewable branch first, get it
merged, and only THEN re-point the release process at the now-real commit. Any release process
should refuse outright to stamp a build with a commit identifier that does not resolve on the
remote — provenance should be a hard release-time gate, not an assumption.
