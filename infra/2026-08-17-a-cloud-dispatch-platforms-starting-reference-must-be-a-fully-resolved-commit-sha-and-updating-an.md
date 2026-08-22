---
title: A cloud dispatch platform's starting reference must be a fully-resolved commit SHA, and updating an existing PR looks identical to "nothing happened"
date: 2026-08-17
category: infra
tags: [dispatch, verification]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Three separate integration gaps surfaced while dispatching work to a cloud-hosted coding-agent
platform through an automated pipeline. First, passing a branch NAME as the dispatch's starting
reference logged a warning that it was "not SHA-resolved, dispatching against the raw ref
(fail-open)" and then failed outright — resolving the branch to its full commit SHA first and
passing that succeeded immediately. Second, even a resolved-but-abbreviated (short) SHA was
rejected, because the platform's API validates the field as either a branch name or a FULL-length
SHA — the platform's two distinct error messages (an invalid-reference error versus a
repository-access error) reliably distinguish which of those two problems is actually occurring,
so reading the error text carefully before re-diagnosing saves a retry cycle.

Third, and separately: a dispatch instructed to push a remediation directly onto an EXISTING pull
request's branch delivered its changes perfectly — commits landed on the right branch within
minutes — while the automated pipeline nonetheless reported the dispatch as a silent no-op with "no
artifacts," because its own completion check only recognizes a brand-new pull-request URL as
evidence of success. A remediation-style dispatch that intentionally updates an existing branch
should be judged by that branch's own tip commit and the pull request's commit list, never by the
pipeline's own "parked" status — that status describes the pipeline's own expectations about what
success looks like, not whether the underlying work actually happened.
