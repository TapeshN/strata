---
title: An equivalence witness that checks status codes and markers, but never diffs the actual bytes, is asserting the plumbing instead of the property
date: 2026-08-17
category: guardrails
tags: [verification, gate-design, false-green]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A rewritten "these two code paths must produce equivalent output" acceptance test asserted that
both paths returned a success status code, an expected marker string, and deterministic output —
but never actually compared the two paths' output bytes against each other. When a reviewer
deliberately introduced a real divergence between the two paths as a mutation test, the suite
stayed green, because nothing in it actually pinned the one property that mattered: byte-for-byte
equivalence. The underlying property happened to be true at the time, but nothing in the test
enforced it.

The generalizable rule: whenever an acceptance criterion is phrased as "X equals Y," the test
suite must contain a literal, direct comparison of X against Y — status codes, presence of a
marker string, or a deterministic-looking shape are all plumbing, not the property itself. Any
witness written to satisfy an equivalence-shaped acceptance criterion should be mutation-tested
(deliberately break the equivalence and confirm the test goes red) before being trusted as closed.
