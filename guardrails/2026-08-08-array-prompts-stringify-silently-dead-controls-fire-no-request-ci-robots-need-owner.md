---
title: Array prompts silently stringify to a placeholder; a control that fires no request is dead; a CI robot identity can need an explicit owner
date: 2026-08-08
category: guardrails
tags: [orchestration, workflow, testing, ci, tooling-gotcha]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An orchestration primitive whose "run a sub-agent with this prompt" call expects a plain string can, when accidentally passed an array of strings instead, silently coerce it into the literal text of an object placeholder rather than raising a type error. Every agent that receives it then runs "blind," with no actual instructions, and produces schema-conformant but meaningless output. The dangerous part is that this can look like a complete, successful run: structured-output validation and completion counts both stay green because nothing about the malformed prompt breaks the pipeline's own contracts. Defense in depth: always join a prompt array into one string at the call site; add a first-line tripwire in the shared agent instructions telling an agent to stop and report if its own prompt looks like a placeholder object; and assert on the SHAPE of returned fields — for example, that a returned reference actually points at newly-created work, not a reused unrelated one — so a blind run throws instead of flowing downstream as if it succeeded.

A UI control that produces no network request when clicked is dead — verify any state-changing interaction by confirming the expected request actually left the client, not merely by the absence of a visible error. This shows up in two related ways: a production button that swallows clicks with zero requests and zero console errors is an absence-shaped bug; and automated form-filling that sets a framework-controlled input's underlying value directly, without dispatching the framework's own change event, causes the framework to never observe the change, so a subsequent submit silently no-ops even though the value visually appears filled in. Prefer driving such inputs through the platform's native value-setting mechanism paired with a dispatched input event, or genuine keystrokes, and always confirm a state-changing action by its network effect.

A mobile app's CI build robot identity or token can fail to resolve which project it belongs to if the app's own manifest doesn't declare an explicit "owner" field, even when a project identifier is otherwise present in the configuration — the resulting error message (suggesting an interactive init or link command) is misleading for an unattended context where interactive login isn't possible. A single explicit ownership field in the manifest resolves it. Separately, a free-tier CI queue for mobile builds can sit for hours at peak usage with its status timestamp frozen at creation time — check the platform's own public status page before assuming a stuck build indicates a bug in your own pipeline.
