---
title: A gate that runs after the irreversible action is not a gate — ordering is the property, not presence
date: 2026-06-07
category: guardrails
tags: [gating, verify-dont-trust, boundaries, agent-guardrails]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A safety gate is only effective if it precedes the side-effect it is meant to prevent. A gate that runs after the irreversible action provides the appearance of protection while offering none — the action has already executed by the time the gate fires.

A concrete instance: an operator-approval gate was wired between two steps of a dispatch handler. Step one made the external API call (the paid, irreversible action). Step two ran the approval check. The gate passed all code review; it was present, wired, and functional in isolation. But the call ordering meant that a denied approval could not undo a dispatch that had already occurred.

The failure mode is easy to miss during review because the gate's logic is correct — the gate itself works. The bug is in where the gate sits in the execution order, not in what the gate does.

Detection requires a call-order assertion, not a status-string assertion. A test that checks the gate's final outcome (approved/denied) cannot distinguish a gate that ran before the action from one that ran after it. A test that records the timestamp of the approval call and the timestamp of the first external API call, and asserts the former is earlier, can catch it.

Generalization: "present but mis-phased" reads safe in code review and is structurally unprotected. For any gate on an external side-effect (a dispatch, a payment, a send, a write), the verification question is not "does the gate exist?" but "does the gate run before the action?" The witness is a call-order assertion or a test that asserts the action is absent on deny, not a test of the gate's logic in isolation.
