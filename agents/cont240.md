---
title: "Four blocking findings went back to workers tonight and two returned FIXED BETTER THAN SPECIFIED — both by narrowing, not by excepting"
date: 2026-09-07
category: agents
tags: ["handback-quality", "narrow-dont-except", "source-of-truth", "spec-the-property-not-the-patch"]
confidence: learned
source: private-work
---

for a matcher that over-fires, prefer **narrowing it to what it is actually for** over adding exceptions. An allowlist of real repo labels cannot corrupt prose by construction — there is no residual case to except, so the bug class is closed rather than sampled. Same move I made on an internal helper (heredoc bodies are data unless addressed to an interpreter) rather than blocklisting phrases.

when handing back a finding, state the DEFECT and the property that must hold, not the patch. Both better fixes came from workers who understood the seam rather than applying my literal instruction — and a spec that dictates the patch would have suppressed both.
