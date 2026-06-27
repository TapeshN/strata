---
title: When browser-MCP interaction appears broken, confirm from source and tests before calling it a bug; prefer DOM-truth tools over repeated screenshots
date: 2026-06-22
category: mcp
tags: [determinism, reproducibility, evals]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A browser-automation MCP tool can fail intermittently — an element click produces no visible response, a network request appears absent, a navigation seems stuck — in ways that look identical to a genuine application bug. Acting on the apparent failure by "fixing" code that is actually correct introduces a regression.

Before concluding that a browser-observed behavior is a bug:

1. Read the source implementation of the feature being observed. Does the code do what the observation suggests it should not?
2. Check whether existing automated tests cover this path. If a test suite already covers the behavior and passes, the implementation is likely correct and the observation is a tool artifact.
3. Use DOM-truth tools (read the element's text content or data attribute programmatically) rather than relying on a screenshot or a zoom. A screenshot is ambiguous; the DOM's own text content is not.

When a browser-MCP session encounters an extension-context error or navigation lockup mid-traverse, the recovery sequence is: navigate to a fresh URL, then prefer DOM-inspection tools over repeated click-and-screenshot cycles. Repeated screenshots on a hung session produce the same ambiguous output indefinitely; a programmatic DOM read either succeeds with ground truth or fails clearly.

The broader principle: a browser-MCP failure and an application bug are visually indistinguishable. Resolve the ambiguity from source code and test results before writing a fix.
