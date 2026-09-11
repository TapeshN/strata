---
title: "Specced" is not "briefed" — and a handback template where every field encodes a past failure
date: 2026-08-25
category: agents
tags: [coverage, handback-contract, worker-cadence, review-throughput]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

**1. A roadmap entry is a reminder; a brief is executable, and claiming coverage on the former is a false-complete.** Asked whether a body of planned work was fully captured, a coordinator answered that it was "all specced". It was not. It existed as prose in a status document — a list of names with a sentence each — and nothing an agent could pick up and run. A push-back prompted a real audit against the completeness document, which found ten genuine gaps and grew the executable queue from thirty-four items to forty-seven.

The root cause was measuring coverage by whether the coordinator could *describe* the work rather than whether anyone else could *do* it. Those are different properties, and only the second matters when the entire point is that other agents execute. The test: could a worker start this tomorrow from what is written, without asking a question only I can answer? If not, it is not covered, however fluently it can be explained in conversation.

**2. A handback template where every field encodes a specific past failure.** Recorded because the fields are not arbitrary and re-deriving them means re-earning them. The head commit identifier, because a branch that moved after its review is a different branch than the one reviewed. Whether the witnesses ran on the FINAL commit, because a full suite from before the last two fixes is not a witness for the tree being merged. Whether the independent review ran on the final tree or was inherited — the same failure applied to review. The base and any stacking, because a stack rooted on a pre-remediation tip silently drops the fixes beneath it. A failing-on-revert demonstration per fix, the only proof a fix is bound by a test rather than merely accompanied by one. Residuals and everything NOT verified, including whatever a reviewer could not run — this field is worth more than the green ones, because a known gap can be acted on and an invisible one cannot. Any unrequested changes on the branch, since work serving neither a finding nor the brief is its own risk even when it looks harmless. And whether the change is user-visible, which decides whether human eyes are required regardless of verdict.

**3. Bounded continuous work: cap the QUEUE, not the worker.** A worker that halts after every handback wastes hours idling; one that never halts accumulates unmerged branches that drift as the trunk advances — which is precisely what forced a restack and conflict pass on three pull requests the same day. The binding constraint is not the worker's throughput, it is the reviewer's. So: continue automatically, hold at most three open pull requests at once, and prefer a next task that touches different files than the open ones. When the cap is reached, that is the reviewer's signal to prioritise merging above anything else.
