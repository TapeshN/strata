---
title: An external chat-based coding assistant can substitute for a primary agentic loop end-to-end, when the handoff contract travels with the brief rather than living in the primary system
date: 2026-07-14
category: orchestration
tags: [subagents, autonomy, lifecycle, fallback, external-agent]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When usage of a primary agentic tool ran low, a full batch of worker deliverables was instead built through an entirely separate chat-based coding assistant, briefed by hand, with the primary tool doing only the final verification and merge pass. The substitution worked end-to-end because the handoff contract itself was written directly into each brief rather than depending on the external assistant being able to read the primary system's own files or state — a fully self-contained brief is portable to any capable worker, human or AI, regardless of which tooling produced it.

Three structural choices made this safe rather than reckless. First, every pull request the external assistant produced still had to pass through the same server-side branch protection rules as any other contributor's work — rules enforced at the hosting platform level reach every pusher equally, regardless of which client or tool pushed the commit, so an external worker gets no special trust. Second, a lightweight pickup mechanism watched for the external assistant's output artifacts and surfaced them to the primary tool automatically, rather than requiring a human to manually ferry results between the two. Third, the primary tool's one remaining job was a single batched review-and-merge pass across all the deliverables, under the same per-change approval discipline as any other merge, and lightly steering the external assistant mid-conversation with two or three corrections caught the same classes of defect an internal review would have.

The generalizable pattern: an agentic workflow is more resilient than it looks if the handoff contract is designed to be self-describing and portable, and if the platform-level gates (branch protection, review requirements) apply uniformly regardless of which tool or agent is the source of a given change. That combination lets a usage-constrained primary tool degrade gracefully to "brief + gate + batch-review" instead of stalling entirely.
