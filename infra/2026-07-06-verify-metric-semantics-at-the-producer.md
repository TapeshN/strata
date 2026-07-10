---
title: Verify a metric's semantics at the producer before changing its behavior
date: 2026-07-06
category: infra
tags: [observability, metrics, dashboards, root-cause, semantics]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When someone asks you to change how a displayed metric behaves — reset it daily, aggregate it differently, alert on it — resist the urge to patch the display layer first. Go read the code or docstring that actually produces the number. A label on a dashboard is not a contract; it is only as accurate as whoever wrote it last remembered to make it.

What happened: an operator asked for a panel's token counter to reset every day, expecting it to represent cumulative daily spend. Reading the producer code that emitted the value showed it was something else entirely: a live snapshot of the current context window's occupancy (the last turn's input plus cached tokens). That number naturally grows within a working session and drops back to near-zero whenever the session compacts or resets — it has nothing to do with daily spend, so "make it reset daily" was a request that could not be honestly satisfied against that source field. Meanwhile the one place that actually recorded real spend over time was a ledger file that had gone dormant for weeks, receiving no live writes. The visible metric and the real cost data were two unrelated things wearing similar labels.

The fix was to build the thing that was actually missing — a proper day-stamped spend recorder wired to the real event stream, careful to exclude cache-read tokens so repeated snapshots of the same context window don't get double-counted — and to relabel the original occupancy readout so it stops implying it's spend.

How to apply: before implementing any change to a metric's semantics (reset cadence, aggregation window, alert threshold), find and read the producer — the function, script, or docstring that assigns the value — not just the UI or query that renders it. If the producer's actual meaning doesn't match what the requester assumes, say so and fix the mislabeling or build the correct source, rather than bending a display to simulate behavior its underlying data can't honestly support.
