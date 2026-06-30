---
title: Validate a content gate at both poles before trusting a green run
date: 2026-06-30
category: infra
tags: [ci, gating, preflight, reproducibility, infra-tooling]
confidence: learned
source: first-principles
implementation_target: infra-tooling
---

When standing up an environment for a repository whose only executable surface is a CI guard, a single passing run proves less than it appears. A guard that exits zero on the current tree could be passing because the tree is clean — or because the guard never actually inspects the thing it claims to protect. The green is ambiguous until both poles are witnessed.

The discipline that resolves the ambiguity: exercise the gate against a known-good input and against a deliberately malformed input, in the same session. The known-good run confirms the gate does not produce false positives on valid content. The malformed run — a file with the wrong frontmatter, a path the leak scan should reject — confirms the gate actually fires and is not a phantom check. Only after seeing it fail on something bad is its pass on something good meaningful.

Two structural details make this reliable for a tracked-file guard. First, a gate that enumerates inputs from the version-control index (rather than the working directory) will not see a new file until it is staged; the negative test must stage the bad file or it silently proves nothing. Second, gates that emit non-blocking warnings alongside hard errors need their exit code read directly, not inferred from the presence of warning text — a warning-heavy run that still exits zero is a pass, and treating the warnings as failure would erode trust in the gate the same way false positives do.

The corollary for environment setup generally: "the checks pass" is a weaker claim than "the checks pass on good input and fail on bad input." The second is the one worth depositing.
