---
title: A test pinned to a prose pattern or regex can be satisfied by an unrelated mechanism, and a floor added later must get its own case
date: 2026-08-22
category: journal
tags: [tests, security]
confidence: learned
source: private-work
---

Two related incidents in the same review pass. First: a set of route-level refusal assertions were moved onto a newly-added, higher-priority refusal floor; the route-level cases they used to cover went silently unpinned, and deleting them left the suite green. The original assertion had also been weak in a second way — it matched on a loose text pattern that a completely different, sibling refusal message also happened to satisfy, so the test had never uniquely exercised what it claimed to. Second, on a different check entirely: a flagship regression test asserted on a loose textual pattern; with the entire mechanism it was meant to test removed, the test stayed green because a separate, unrelated staleness check produced output matching the same loose pattern.

General rule: when a test's assertion is a prose match or regex rather than an exact, stable identifier (a reason code, an error constant), a different code path can satisfy it for the wrong reason, and the test silently stops proving what it claims to. Assert exact codes/constants, not patterns. And when a new, higher-priority check is added on top of existing behavior, give the new floor its own dedicated test case rather than moving an existing assertion onto it — the old case may still need to be true, just for a different, now-untested reason.
