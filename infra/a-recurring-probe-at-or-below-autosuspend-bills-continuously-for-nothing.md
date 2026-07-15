---
title: A recurring probe at or below a backend's autosuspend window bills continuously for zero benefit
date: 2026-07-12
category: infra
tags: [cost, latency, cache]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A lightweight periodic health check polled a downstream managed database on the same interval as that database's own auto-suspend idle timeout. The intent was a cheap, low-frequency probe; the actual effect was that the probe woke the database from suspension just before it would have gone idle, on every cycle, so the backend never actually suspended and billed for continuous compute the whole time — confirmed against real recorded usage on a pay-as-you-go plan. The cost was never the query itself; it was the wake the poll forced on an otherwise idle, auto-suspending resource, and polling at exactly the threshold interval is the worst possible case: maximum forced-wake cost for zero added freshness benefit over a longer interval.

The generalizable rule: before wiring any recurring probe against a metered or auto-suspending backend, compare the probe's interval to that backend's suspend/idle window first. If the interval is anywhere near or below the suspend window, the probe itself is the cost driver, not whatever it's checking. A durable fix separates a cheap, purely local wake signal from an actual network or database touch that only fires on a longer, deliberately configured interval, and a failed poll should back off exactly like a successful one — a hot-failure retry loop against the same interval burns the identical cost.
