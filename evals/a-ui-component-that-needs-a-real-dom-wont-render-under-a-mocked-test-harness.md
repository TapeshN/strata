---
title: A UI component that needs a real DOM won't render correctly under a mocked-backend unit-test harness — flag the harness gap, don't fake the test
date: 2026-07-21
category: evals
tags: [testing, evals, dom, harness-design]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A component relying on a browser-shaped rendering environment (a markdown-to-DOM renderer, for instance) fails to render inside a test runner configured for a plain server-side environment with mocked backend calls — not because the component is broken, but because the test harness never actually provides a working render surface for it. Trying to force a component-level render test through that harness produces confusing, unrelated-looking errors that have nothing to do with the component's actual correctness.

**The rule:** for a UI fix whose test harness genuinely can't render it, the honest witness is two-part: a source-wiring regression guard (assert the fix is present and wired to the right place in source) PLUS a standalone behavioral render test run in an environment actually configured to render that component correctly — not a component-render test squeezed into a harness that was never built for it. Explicitly flag the harness gap as its own finding rather than writing a test that looks like it proves rendering but doesn't.
