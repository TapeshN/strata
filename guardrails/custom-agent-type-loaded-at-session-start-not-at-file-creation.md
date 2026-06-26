---
title: A custom agent type defined mid-session is not invokable until the next session start
date: 2026-06-16
category: guardrails
tags: [agents, lifecycle, session-scope, registry, wired-not-working, skills]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Custom agent type definitions stored in a designated agents directory are loaded into the invokable registry at session start, not at file-creation time. A definition file written or modified during an active session will parse successfully and appear to be a valid agent, but it will not be present in the registry that dispatches and workflows use to resolve agent type names. Any workflow or dispatch that references the newly-defined type will fail with a "type not found" error, even though the definition file exists on disk and its schema is valid.

This is the file-exists-but-not-wired variant of the wired-not-working class. The file is correct; the runtime registration is absent. Verifying the agent's definition is not the same as verifying it fires.

The workaround: instead of referencing the agent by its registered type, load its definition by reading the definition file as the prompt and adopting it as operating instructions within a general-purpose agent invocation. This decouples the capability from the registry and makes it functional without requiring a session reload.

The correct verification sequence: after creating a new agent definition, do not assume it is invokable. Reload the session, then confirm the type appears in the registry. Only after a successful test invocation in the new session should the agent type be used in a production workflow. Any workflow that depends on a custom agent type must be tested against a reloaded session before being relied upon, not against the session in which the definition was written.
