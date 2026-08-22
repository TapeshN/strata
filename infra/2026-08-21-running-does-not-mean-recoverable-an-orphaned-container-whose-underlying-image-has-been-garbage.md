---
title: "Running" does not mean "recoverable": an orphaned container whose underlying image has been garbage-collected cannot be committed — it must be exported
date: 2026-08-21
category: infra
tags: [provenance, release, infra-truth]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A running container turned out to be the ONLY remaining instance of a particular build — its
underlying container image had already been garbage-collected by the runtime, so the standard
"commit this running container into a new image" recovery path failed outright, because it
requires a content digest that no longer existed. The only viable snapshot path was exporting the
running container's full filesystem directly (a large archive of its root filesystem), rather than
committing it as an image. Separately, a different live artifact's build stamp turned out to be a
raw content hash rather than a commit reference, so it could never be resolved to any git object
in the first place, by design.

The generalizable rule: "running" is not the same claim as "recoverable" — a container whose
backing image has been garbage-collected can only be preserved by exporting its filesystem
directly, not by committing it. Every release artifact should carry a label recording the actual
commit it was built from (one that is reachable from a remote, not merely a content hash), and any
release or health-check tooling should treat a "live" label as meaningful only once that source
commit is confirmed to resolve.
