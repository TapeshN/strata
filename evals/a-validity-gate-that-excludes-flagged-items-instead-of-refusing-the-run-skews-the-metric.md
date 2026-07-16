---
title: A validity/contamination filter that silently excludes flagged items — instead of refusing the whole run — skews the metric it's supposed to protect
date: 2026-07-14
category: evals
tags: [evals, judge, measurement-integrity, gate-bias, golden-sets]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A scoring pipeline used a per-response validity check to reject contaminated or otherwise invalid responses before aggregating a preference metric across a panel. In practice, the rejection logic used phrase-based markers that happened to correlate with the language typically used to argue FOR one particular option — so the exclusion was not neutral. It preferentially discarded responses favoring one side, which deflated that side's measured preference rate and could fabricate the appearance of a one-sided or agreeing panel even when the underlying panel was not actually one-sided.

The general rule: when a validity or contamination check trips inside a measurement pipeline, the correct response is to REFUSE the whole run (or the specific item) and surface it as invalid — never to silently exclude the flagged item and continue aggregating the survivors, because exclusion changes the composition of what's being measured, and a self-serving exclusion pattern will systematically favor whichever side's language looks least like the exclusion criteria. If the check itself relies on phrase or keyword lists to decide what counts as contaminated, those lists must be scoped to result-stance-neutral vocabulary — words that flag "this response is invalid" independent of which option it favors — never vocabulary that happens to describe one option's own merits. Otherwise a "quality gate" becomes a hidden thumb on the scale for whichever side's supporting language resembles the exclusion pattern less.
