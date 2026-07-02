---
title: A CI path-ignore rule meant to skip expensive tests on docs-only changes can also skip the one check meant to validate those docs
date: 2026-07-02
category: infra
tags: [ci, docs, gating]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A documentation-only pull request landed cleanly because the CI configuration excluded markdown-only changes from the full test suite — a reasonable cost optimization. But the same exclusion also skipped a lightweight check whose entire job was to validate the structure of documentation files (required frontmatter, type classification, etc.). The doc landed without that validation, was subtly malformed, and the failure only surfaced later on an unrelated, purely-code pull request that ran full CI against the now-accumulated bad state — a red check on an innocent change caused by a merge from hours earlier.

The root cause: a path-ignore rule is usually written to skip expensive checks whose subject matter doesn't touch the ignored paths. It's easy to also, unintentionally, catch the rarer class of check whose entire subject IS the ignored paths — a doc-content validator has no reason to run on a code-only change, but every reason to run on a docs-only one, and a blanket ignore rule doesn't distinguish between the two.

The fix: any path-ignore carve-out in CI should be audited specifically for checks whose subject matter is the ignored path set, and those checks should be pulled into a lightweight job that runs precisely when the expensive suite is skipped, not lumped in with everything else. Separately: when a check fails on your change for state you didn't introduce, land the fix forward immediately rather than treating it as someone else's problem — an accumulated red blocks everyone's next unrelated change.
