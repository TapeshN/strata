---
title: A class rename that deletes the old CSS family leaves an orphaned-markup regression — recover the deleted rules from git, don't reinvent them
date: 2026-07-04
category: guardrails
tags: [regression, css, git-recover, layering]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A site redesign migrated one section's markup to a new CSS class and deleted the old class family in the same commit. A different, unrelated section on the same page still used the old class name — nothing renamed it there — so once the shared stylesheet rules disappeared, that section fell back to unstyled browser defaults. The visual result looked like a spacing or content bug (labels and values collapsing into each other); the actual cause was a stylesheet that had simply stopped existing for that markup.

The fix is not to guess a fresh layout for the orphaned section — the original author already had a working design for it, and it is retrievable. Recover the exact deleted rules from the commit that removed them (read the stylesheet at the parent revision of the deleting commit), confirm every CSS variable they reference still exists in the current stylesheet, and restore them verbatim rather than reinventing the layout from scratch. Verify with computed styles and a live render, not just a diff review.

The generalizable habit: whenever a redesign renames or migrates a CSS class, grep every usage of the old class name across the codebase before deleting its rules — a class can be shared by markup the redesign never touched. And a mechanical guard is cheap here: flag any class referenced in markup with no matching rule in any stylesheet, which catches this exact regression class before it ships.
