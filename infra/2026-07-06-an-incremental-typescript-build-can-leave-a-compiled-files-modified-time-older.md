---
title: An incremental TypeScript build can leave a compiled file's modified time older than its edited source, tripping a local freshness guard on code that is actually current
date: 2026-07-06
category: infra
tags: [tsc-incremental, tsbuildinfo, dist-freshness, mtime, local-false-failure]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A freshness guard that compares a compiled output file's modification time against its source file's modification time is a reasonable way to catch a stale build being shipped by accident. But an incremental TypeScript build cache can decide that a given output would be byte-identical to what is already on disk and skip rewriting it — leaving the compiled file's modification time untouched even though the source file was just edited and rebuilt. Locally, that produces a guard failure that reads as "source is newer than the compiled output," even though the compiled output actually reflects the new source correctly; the mismatch is purely a timestamp artifact of the incremental cache deciding not to touch a file it judged unchanged. A clean continuous-integration run is unaffected, because a fresh checkout has no incremental cache and always performs a full compile with fresh timestamps.

The fix is to delete the incremental build-info cache (or the whole output directory) and rebuild from scratch whenever this specific failure shows up locally. More generally, this is a useful triage question for any test that fails locally but would plausibly pass on a clean checkout: if the answer is yes, treat it as a stale local artifact rather than a real regression, and clear the artifact before spending more time debugging the "regression" itself.
