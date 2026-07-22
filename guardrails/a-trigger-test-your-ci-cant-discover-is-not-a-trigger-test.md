---
title: A trigger-test that your CI can never discover is not a trigger-test
date: 2026-07-22
category: guardrails
tags: [gates, ci-discovery, test-placement]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A meta-gate whose job is auditing whether every safety hook has a real, committed trigger-test looks for those tests at a specific, conventional location. A new hook's test existed and passed locally, but lived in a different directory than the one the discovery mechanism actually scans — so the meta-gate correctly failed it as effectively untested, because a test CI can't find contributes nothing to CI's actual coverage, regardless of whether it exists and passes on someone's machine.

**The rule:** when adding a new gate/hook and its trigger-test, put the test at exactly the path your discovery/CI-collection mechanism looks for it, not wherever is convenient for the rest of the surrounding work — a test's existence only counts if the thing meant to run it can actually find it.
