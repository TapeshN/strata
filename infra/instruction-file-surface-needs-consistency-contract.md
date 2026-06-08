---
title: Agent instruction files drift across tools without a consistency contract
date: 2026-06-06
category: infra
tags: [multi-repo, docs, roles]
confidence: learned
source: private-work
---

Instruction files for different tools (AI assistant context files, IDE rule files, agent configuration files) accumulate per-tool with no consistency contract, drifting in the same way that safety gates drift when added independently per-repo. A repository can have a rules file for one tool but not the equivalent file for another, leaving agents in that tool without governing context.

In a concrete case, one repository had rules for one class of tool but no context file for another — meaning a session in the second tool would run without any governing constraints.

Prevention: define a consistency contract for instruction files across tools, specifying which file must be present for each tool and what each must contain. Audit coverage periodically — the same way you audit gate coverage after a preflight contract is established.

General lesson: instruction-file drift and gate drift are the same problem at different layers. Apply the same contract-and-audit discipline to both.
