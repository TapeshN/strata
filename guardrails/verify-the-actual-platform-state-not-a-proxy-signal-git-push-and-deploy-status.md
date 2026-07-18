---
title: Verify a git push and a platform deploy by their actual state, not a proxy signal
date: 2026-07-16
category: guardrails
tags: [ci, release, gating, determinism]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Two related witnessing failures in the same delivery pipeline, both with the same root shape: trusting a signal that is usually correlated with success, instead of confirming the actual state directly.

**A `git push` can fail silently and still look done.** A push command can print only a trailing configuration hint (unrelated help text) instead of the actual success line that names the source and destination refs — and reading any output at all, without checking for the specific success marker, is easy to misread as "it worked." When that happens, the intended fix never reaches the remote, and anything built downstream of "the push succeeded" inherits a stale base. This recurred multiple times in the same stretch of work, through different proximate causes each time (once a piped/aliased command silently swallowed the real push output). The durable fix is not "read the output more carefully" — it's to stop trusting push stdout entirely and instead assert the invariant directly: after any push, compare the local branch's commit hash against its upstream tracking ref (they must be equal), which is immune to any wrapper, alias, or pipe eating the printed output.

**A deployment-status API can report a stale success for a state it hasn't caught up to yet.** After a merge, querying a hosting platform's own deployment-status API for the production environment can return the PREVIOUS successful deployment (from before the merge) because it hasn't yet indexed the new one — while the platform's own CLI, queried directly for the live deployment list, correctly shows the new deployment mid-build. Treating "the status API says success" as proof of a deploy is trusting a system that can be behind real-world state by design (eventual consistency in its own indexing). The fix: witness deploys through the platform's own live listing/inspection tooling (a CLI's "list current deployments" and "inspect this deployment's logs" commands), not through a status API whose freshness guarantee is unclear, especially in the minute or two immediately after a merge.

The general lesson underneath both: any "did the thing happen" question has one authoritative source (the ref comparison; the platform's live deployment list) and several plausible-looking proxies (push stdout; a status API). Prefer the authoritative source by default, especially for any check that gates further automated action.
