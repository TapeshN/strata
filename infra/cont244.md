---
title: "I offered a cause for a CI red without running the base check, and pointed a worker at the one fix that would have undone their own remediation"
date: 2026-09-07
category: infra
tags: ["introduced-vs-inherited", "hypothesis-cost-asymmetry", "remediation-undone-by-plausible-fix", "lateral-evidence"]
confidence: learned
source: private-work
---

when a PR is red, establish inherited-vs-introduced BEFORE offering any hypothesis — a cause offered early is acted on, and the worker will make it true. Cheapest evidence is lateral: does another open PR on an unrelated branch fail the same way? That is one query and it beats reasoning from log adjacency.

weigh a wrong hypothesis by what acting on it would DESTROY, not by how likely it is. Here the plausible fix reintroduced client data into git history on a client repo. When the cost of a wrong guess is asymmetric, say "unknown until the base check runs" rather than naming a suspect.
