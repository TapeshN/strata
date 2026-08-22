---
title: A once-per-period completion stamp with no clearing path on cancel/reset becomes a lockout — every terminal state in a stateful pipeline needs an exit
date: 2026-08-22
category: guardrails
tags: [state-machines, money]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A pricing pipeline recorded a "already staged this period" stamp the moment a batch entered staging, to prevent double-staging. Cancelling a staged batch cleared the batch's own state but never touched that stamp; a batch where every item ended up skipped for unrelated reasons left the stamp set with nothing to show for it. The combined effect: an owner's entire annual round of pending changes could silently vanish with no in-app path to recover it — re-approving found nothing due, and re-staging was refused outright by the very stamp meant to prevent duplicates.

General rule: any "once per period" or "already processed" guard that's implemented as a bare stamp, rather than a check against a still-live record, needs an explicit clearing action wired into every path that can terminate the thing it was guarding (cancel, full-skip, error, timeout) — otherwise the guard silently survives its own subject's failure and becomes a permanent lock. Test the guard by cancelling or all-skipping mid-pipeline and confirming the next attempt is not blocked.
