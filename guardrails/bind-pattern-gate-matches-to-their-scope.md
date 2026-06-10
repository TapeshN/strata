---
title: Bind a pattern gate's matches to their scope — compound words and cross-repo IDs are the recurring false-positive classes
date: 2026-06-10
category: guardrails
tags: [gating, false-positives, narrow-dont-bypass]
confidence: learned
source: private-work
---

Keyword and identifier gates over-fire in two recurring ways. First, a keyword matches *inside* a compound technical term: a gate watching for the state word "open" fired on the phrase "fail-open", reading a merged item as still open and blocking a legitimate push. Second, a bare numeric identifier collides across namespaces: a gate that pairs "#N" references against its *own* repository's merge log flagged a document line describing a *different* repository's #N, because the local #N happened to be merged.

Both are the same defect: the pattern is matched without binding it to the scope it claims to describe. The fix is always to narrow the pattern — exclude compound terms that contain the keyword (fail-open, open-source), and require identifiers to be qualified by their namespace (repo-name#N) or scoped to the namespace named in surrounding context — and never to bypass the gate. A gate that erodes trust through false positives gets disabled by humans eventually; scoping it preserves both the gate and the trust.
