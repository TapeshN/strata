---
title: A UI component that "just renders cards" may be answer-key or exercise content — read the source before refactoring or replacing it
date: 2026-06-14
category: guardrails
tags: [gating, hitl, preflight, docs]
confidence: learned
source: private-work
---

In a product built around intentional defects or training content (e.g., a QA learning platform, a code kata site, an intentional-bug playground), some UI components that appear to be simple display cards are actually the exercise itself — they host the planted defects, answer keys, or auto-launch hooks that make the training scenario work. Refactoring or replacing such a component based on a visual or information-architecture directive would silently destroy the product's content.

**The risk pattern:** a UI directive like "make this consistent with that other component" is authoritative for presentation, but it can be interpreted in a way that replaces the underlying component rather than restyling it. If the component-to-replace is the exercise container, the refactor destroys training content.

**Prevention:** before refactoring or replacing any product UI component, read the component source and grep for:
- Planted-defect or answer-key identifiers (bug IDs, intentional-error markers, `activeBugId`, `answerId`, etc.)
- Auto-launch or session-initialization hooks
- Data imports from a content or answer-key directory

If any of these are present, the component is not a plain display card — it is content. A visual-consistency directive does not authorize destroying content; surface the conflict to the operator rather than proceeding.

**Floor precedence:** content-preservation floors override UI directives. Even an explicit "do it now" instruction does not override a floor that protects irreplaceable answer-key or exercise content. The correct response is to implement the non-destructive parts of the directive and flag the content-destructive part for operator resolution.
