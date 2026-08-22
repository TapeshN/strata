---
title: A schema-forced scout's own logging layer can silently truncate everything past a fixed byte cap — recovery requires reading raw transcripts
date: 2026-08-21
category: orchestration
tags: [orchestration, workflow, tooling]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

In a large fan-out of scouting agents each expected to return a structured report, a meaningful
fraction failed the structured-output contract outright (their responses did not parse as the
required schema after several retries), and the surrounding journal/logging layer had itself been
keeping only the first couple of kilobytes of each failed attempt — nowhere near enough to
reconstruct what the scout had actually found. Some of the truncated attempts were recoverable
(one had been double-encoded and happened to survive intact); most were not, and had to be
manually reconstructed from the underlying session transcripts and their tool-call results, at
real time cost.

The generalizable rule: agents expected to return a large report should return prose (plain text or
markdown), not a rigid schema — reserve schema-forced structured output for genuinely small,
tabular, or enum-driven payloads where the shape really is the whole contract. Any logging or
journaling layer that stores an agent's output for later recovery should not impose a small fixed
byte cap on "big report" style outputs, since that cap silently converts a partial failure into a
total, unrecoverable one.
