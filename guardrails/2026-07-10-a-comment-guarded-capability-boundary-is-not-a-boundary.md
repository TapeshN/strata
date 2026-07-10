---
title: A comment-guarded capability boundary is not a boundary
date: 2026-07-10
category: guardrails
tags: [capability-boundary, type-safety, security-review, privilege-escalation, api-design]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A capability boundary "protected" only by a comment — a JSDoc `@internal` tag, a "call only from here" note, an import-path convention — is not protected at all. Prose is not enforced by the compiler, and any editor (human or AI) is free to construct the privileged value directly and route around every runtime check downstream, no matter how airtight those checks look.

**What happened:** A security review found a plain `static` factory method on a shared class, publicly exported from a shared package, whose only guard against misuse was a doc-comment saying it was for internal use only. That factory could mint a capability object representing an unbounded spending ceiling. Because the method was a normal public value in the type system, nothing stopped code elsewhere from calling it directly and forging a privileged object that bypassed a kill-switch flag entirely. The team reproduced this live: several large debits went through stamped as "enforced," even though the kill switch was supposedly on — because the forged capability never passed through the code path that checked it.

**How to apply:** When you design a privilege or capability boundary, ask whether the escape hatch is enforced by the type system/compiler or merely documented. If a privileged value can be constructed by any code that imports the module — regardless of a comment telling it not to — the boundary doesn't exist. Push the enforcement to the language level: make the constructor genuinely private and expose only a narrow, already-checked factory path, so there is no public API surface capable of forging the privileged value in the first place. This matters even more in codebases where AI agents or many contributors edit broadly — a comment-guarded shortcut will eventually get used, not out of malice but because it's sitting right there in the public API looking like a normal function.
