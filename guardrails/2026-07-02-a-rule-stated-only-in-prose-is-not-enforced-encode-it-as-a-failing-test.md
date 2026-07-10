---
title: A rule stated only in prose is not enforced — encode it as a failing test the moment it is discovered
date: 2026-07-02
category: guardrails
tags: [gating, ci, evals]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A first draft of a routing configuration mapped an internal-only data stream onto a channel meant only for client-facing output. A reviewer caught it before it shipped, and the rule that fix implied — "no internal route may ever target a client-facing channel" — was written down as a design principle. The team's next move is the load-bearing part: rather than leaving that principle as a sentence in a document that a future change could violate without anyone noticing, it was encoded as a failing automated test that asserts the constraint directly against the routing configuration.

A rule that lives only in prose depends on every future author reading and remembering that specific sentence; a rule encoded as a test fails loudly and specifically the moment a future change violates it, with no dependence on anyone's memory. This is a small, concrete instance of a much larger principle: mechanical gates catch what documentation alone cannot, because documentation only helps the reader who chooses to read it.

The generalizable practice: whenever a code review or an incident produces a rule worth stating ("X must never target Y," "A must always precede B"), the default response should be to write a test that encodes exactly that constraint, not merely to add a line to a document. This turns an ad hoc catch into a durable, self-enforcing guarantee, and is the standing pattern to apply to any future constraint discovered the same way.
