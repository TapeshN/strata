---
title: Two gates refused legitimate work because each read the wrong dimension of the request
date: 2026-09-02
category: guardrails
tags: [gating, ci, worktree, scope-not-bypass]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two separate automated gates blocked work that was legitimate, and in both cases the gate was reading the wrong signal, not applying the wrong policy. A deploy-budget gate that exists to cap how many production deploys land per day inspected the branch name and labels of the pull request being merged, not the branch it was merging into — so a merge into a shared integration branch, which itself deploys nothing on its own, was flagged as an unwanted solo deploy. Separately, a permission-grant tool and the gate that checks for its grant resolved their record of "who is authorized" from two different filesystem roots — one from the main checkout, one from the calling session's own isolated workspace — so a grant written by one was invisible to the other, and the exact same request was refused twice even after being explicitly authorized.

General rule: when a gate refuses work you believe is legitimate, the first diagnostic question is what the gate actually reads — the source branch or the destination branch, the caller's working directory or a fixed canonical one — before reaching for a bypass. A gate that inspects the wrong dimension of a request will refuse correct requests and, more dangerously, may pass incorrect ones that happen to look right on the dimension it does check. The fix is always to scope the gate to read the right thing and to have it name what it read in its own refusal message, never to disable it or route around it. Both gates here were fixed exactly that way and re-verified against the same requests that had originally been refused.
