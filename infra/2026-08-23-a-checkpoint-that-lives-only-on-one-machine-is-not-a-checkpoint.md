---
title: A checkpoint that lives only on one machine is not a checkpoint — and any artifact producer on a timer needs a size quota
date: 2026-08-23
category: infra
tags: [durability, backups, worktree, durable-execution]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An operating-system-managed sync folder — the kind a cloud-account toggle can empty wholesale — held the default root for every scratch checkout that agents worked in. During a storage cleanup that account setting flipped, the folder came back empty, and several days of in-flight branches appeared to vanish at once.

They had not. A scratch checkout's commits live in the parent repository's object store, so every branch ref was intact and every commit still listed. The first rule is therefore a diagnostic one: check the ref before declaring work lost. The folder is not the repository.

The second rule is sharper. A commit that has not been pushed is not a checkpoint. The durable-execution doctrine — "checkpoint to disk so a fresh session can resume from artifacts rather than memory" — is only true if the disk itself survives, and a disk is exactly what did not survive here. The moment a slice commits, it should push its branch and print the remote ref line back as part of its result. On a cheap-on-pull-request continuous-integration matrix, a branch push with no pull request triggers nothing, so the durability is free.

Third: the per-session scratch directory is cleared on reboot. A long run's scripts, reports, screenshots, and witness artifacts existed only there and were gone after a restart. Only the run journal survived — and a journal holds each stage's RETURN VALUE, not the report file that stage wrote. So the load-bearing facts (the verdict, the finding list, the commit identifiers) belong in the structured result, not behind a path to a report, and any artifact meant to outlive the run belongs somewhere that is neither the scratch directory nor a sync-managed folder.

Fourth, from the same afternoon and the same root cause: the disk filled because an encrypted-snapshot job ran on a timer with age-based retention, no size quota, no remote destination, and a run-at-load trigger that also fired on every boot. Twenty local-only snapshots consumed more space than the machine had free. Any artifact producer on a schedule needs a size quota and a count-based retention rule before it ships, enforced as the first statement the producer runs rather than as a cleanup habit — and it is usually better to snapshot before a merge or a destructive action than on a clock at all.
