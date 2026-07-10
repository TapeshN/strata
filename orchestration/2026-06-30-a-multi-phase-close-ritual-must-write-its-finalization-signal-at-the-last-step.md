---
title: A multi-phase close ritual must write its finalization signal at the last step, never at an earlier preparation step
date: 2026-06-30
category: orchestration
tags: [lifecycle, gating, determinism]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A session-close ritual that runs a learning-extraction step early in its sequence, then continues through several more phases before actually finishing, will produce an "extraction happened" signal that is stale by the time anything downstream checks it — even though the extraction itself was genuine and correctly executed at the time it ran. Any activity in the phases that follow (including a token-usage threshold crossing during the operator's own subsequent turns) can trigger a fresh staleness signal that post-dates the extraction event, so a mechanical gate checking "has extraction happened more recently than the last staleness trigger" will correctly, but unhelpfully, report the extraction as stale.

The gate is not broken — it is behaving exactly as designed, catching genuinely intervening activity since the last recorded event. The ritual's phase ordering is what made the earlier event stale by construction: recording "done" at an early phase, when later phases can still generate new staleness, guarantees eventual mismatch.

The fix is to move the write: the ritual's very last action, not an earlier "prepare" phase, should be the one that re-stamps the finalization signal, since by definition nothing legitimate happens after the ritual's terminal step. The general rule for any multi-phase ritual shaped like "prepare X, do more work, then finalize": the finalization-gate signal belongs at the finalize step, never at the prepare step, because everything between prepare and finalize is exactly the kind of intervening activity a staleness check exists to catch.
