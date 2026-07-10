---
title: Verify inherited claims before acting; an eval must be CI-reachable, not just present
date: 2026-07-08
category: evals
tags: [evals, ci-gating, verification, stale-documentation, audit-hygiene]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Before acting on any inherited "known fact" in a hand-down document — a status report, a scorecard, a seeded set of findings — verify it fresh against the primary source (the actual code, config, or CI run), because these claims are snapshots that decay and are wrong more often than teams expect.

What happened: an audit inherited a set of "known" quality claims from prior documentation and set out to act on them. A fresh, independent read-only pass instead of trusting the hand-down turned up that several of the seeded claims were stale or simply incorrect: a repo flagged as having "zero test-gating CI" actually had a real blocking test suite with discrimination-witness tests, making it one of the stronger examples rather than the weakest; another repo flagged as having "zero evals" did have an eval suite, but it could only run against a local model and was unreachable from the CI pipeline that was supposed to gate merges on it — so the real defect was invisibility to the gate, not absence of evals altogether; and a few previously-flagged legal/code defects had already been fixed in the interim but were still listed as open. Acting on the stale claims as given would have either wasted effort re-fixing what was already fixed or misdirected work against a wrong premise entirely.

How to apply: treat any inherited claim in a hand-off, ticket, or prior report as a hypothesis, not a fact, and re-verify it against the live source before spending effort on it — a cheap way to do this at scale is a bounded, read-only pass that returns concrete evidence (file and line, or a command's actual output) rather than restating prose. Separately, when checking whether "an eval exists" for some pipeline, the correct test isn't whether the eval exists on disk — it's whether the eval is reachable from the CI or gate that's supposed to act on its result; an eval that only runs locally is functionally invisible to automated enforcement.
