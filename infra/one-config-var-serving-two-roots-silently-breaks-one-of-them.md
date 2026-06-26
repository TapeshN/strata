---
title: A single config variable serving two root paths silently breaks one of them
date: 2026-06-25
category: infra
tags: [config, env-vars, two-roots, silent-failure, monorepo, dispatch]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

When a single environment variable is used to locate two structurally different roots — for example, a secrets file and a handoff directory — any invocation context where those roots diverge will silently fail one of the two lookups. The variable is valid for one use; the second use resolves to the wrong location and either returns empty results or falls through to a fallback that hides the problem.

The signature is a working dispatch that produces no output from the path that depended on the mismatched root. The call succeeds, no error is raised, and the missing output is only noticed downstream — or not at all.

The fix is to give each distinct root its own variable. Roots that coincidentally share a location in the common case are not the same root; they require separate declarations so that any invocation context where they diverge is handled correctly.

Corollary for diagnostics: when a pipeline step silently skips expected output, examine every path that the step resolves from a shared environment variable. The variable's value in the invocation context may be correct for one purpose and wrong for another.
