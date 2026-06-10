---
title: Build agent prompts as plain joined strings — a fenced code block inside a template-literal prompt breaks the host script
date: 2026-06-10
category: agents
tags: [prompt-authoring, orchestration-scripts, escaping]
confidence: learned
source: private-work
---

Orchestration scripts that spawn agents typically carry each agent's prompt as a template literal delimited by backticks. Embedding a fenced code block (triple backticks) inside such a prompt prematurely closes the template literal: everything after the fence is parsed as host-language code, and the script fails with an opaque syntax error far from the real cause. This bit twice in one week across two separately-authored orchestration scripts — it is an authoring trap, not a one-off typo.

The robust pattern: agent prompts contain zero backticks. Build multi-line prompts as arrays of plain strings joined with newlines, reference code, paths, and contracts in prose rather than fenced blocks, and inline any schema as a joined array rather than an example block. For iteration, persist the orchestration script to a file and launch it by path instead of inlining it — which also sidesteps a second layer of shell escaping.
