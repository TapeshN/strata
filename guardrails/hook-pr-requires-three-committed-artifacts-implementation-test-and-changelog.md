---
title: A hook or gate PR requires three committed artifacts — implementation, trigger-test file, and CHANGELOG entry — inline verification is not the committed witness
date: 2026-06-29
category: guardrails
tags: [gating, preflight, ci, release, versioning]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When a new hook or enforcement gate is added to a repository's control plane, CI requires three distinct committed artifacts before a merge can succeed: the implementation file, a test file that exercises the gate's trigger paths, and a CHANGELOG entry. The CI gates check for the committed test file — not for evidence that the author ran a trigger matrix in the conversation. Inline verification, however thorough, does not satisfy a CI gate that checks for a committed artifact.

This creates a two-failure mode: the implementation may be entirely correct and the trigger matrix may have been manually verified, but the PR goes red twice in CI because neither the test file nor the CHANGELOG entry was committed before push. Each failure costs a full CI round.

The fix is to treat the hook as three files from the start. The implementation, the test, and the CHANGELOG entry are committed together in a single pass — not sequentially after seeing CI fail. A local preflight check that validates the meta-gate and changelog-gate expectations before any push converts the two-failure mode into a single green run.

The broader pattern: for any enforcement artifact whose authority depends on its presence on disk rather than its correctness in memory, the proof-of-correctness is the committed artifact running in CI, never the author's in-session witness.
