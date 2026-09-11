---
title: A lazily-computed remote field is not a healthy value, and a directory is not a repository
date: 2026-09-05
category: infra
tags: [determinism, boundaries, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Filtering a remote code-review API for pull requests sitting in a "blocked" merge state, by matching only the known-bad value, undercounted the real number by a wide margin. The field is computed lazily by the remote system: at the moment of the query, several pull requests were still in an "unknown, not yet evaluated" state rather than explicitly healthy or explicitly blocked, and a filter that looks only for the bad value cannot distinguish "confirmed fine" from "not evaluated yet." The miscount is one-directional and silent — it only ever hides problems, never invents them. Rule: when a remote system computes a field on demand, never infer health from the absence of the known-bad value; assert the presence of the known-good value, or poll until the field resolves out of its pending state. An unresolved/unknown state is not a synonym for OK.

Separately, in the same investigation: two local directories were checked out against the very same remote repository, at different commits and with different tooling wired up (one with no CI configured, one with a full pipeline) — a survey that enumerated directories reported the project as uninstrumented, because it happened to scan the empty one. A directory is not a repository; the same remote can exist checked out more than once, under different local names or in different places. Rule: any tooling that discovers projects by walking the filesystem must dedupe by the remote's canonical URL before drawing a conclusion about what does or doesn't exist for a given project — never by local directory path or name.
