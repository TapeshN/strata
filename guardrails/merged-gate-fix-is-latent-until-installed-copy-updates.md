---
title: A merged fix to a gate is latent until the runtime's installed copy updates
date: 2026-06-10
category: guardrails
tags: [gating, lifecycle, deploy, verify-dont-trust]
confidence: learned
source: private-work
---

Safety hooks and gates are loaded by the runtime from an installed path — often a long-lived primary checkout — not from the branch where their fix just merged. Merging a gate fix is therefore not deploying it: the old, buggy gate keeps enforcing until the installed copy is reconciled. This has a vicious special case: when the buggy gate guards the very push that carries its own fix, the old installed copy blocks the fix from landing.

Observed repeatedly (five instances in one workspace): a documentation-freshness gate over-fired on a false positive, the corrected gate sat merged on the main branch, and the stale installed copy kept blocking pushes. Environment-variable bypasses set in a shell command never reached the hook either, because hooks run in the host process's environment, not the command's.

Treat gate fixes as deploys, not merges: after merging, reconcile the installed path explicitly, then verify self-heal by running a genuine payload through the *installed* gate — not the repo copy — and watching it pass. Where the gate blocks its own fix, make the flagged target honestly compliant first (fix the document, not the gate's opinion), land the fix, then reconcile.
