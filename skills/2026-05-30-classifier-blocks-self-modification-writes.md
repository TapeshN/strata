---
title: Auto-mode classifier blocks self-modification writes independently of conversational approval
date: 2026-05-30
category: skills
tags: [guardrails, autonomy, skills, self-modification, permissions]
confidence: learned
source: private-work
---

In Claude Code auto-mode, writes to the commands directory and the agent library paths are classified as self-modification and blocked at the tool level — independently of whether the user has approved the action in conversation, in a plan, or via explicit instruction. The classifier enforces this category regardless of context.

This is the correct behavior from a security standpoint: an agent that could bypass self-modification gates by obtaining conversational consent would be much easier to manipulate into harmful configuration changes. The gate needs to be independent of the conversation.

The practical implication: any session that plans to create a new slash command or skill must first add an allow rule to the project settings file before attempting the write. The allow rule is the human's explicit, durable authorization — persisted in settings, not just spoken in conversation.

The pattern that works:
1. Open settings and add the specific allow rule (e.g., allow writes to commands directory)
2. Only then attempt the write — it goes through cleanly
3. The session chat provides the file content; the human pastes the terminal command if the automated path is still blocked

The lesson generalizes beyond skills: for any action the classifier treats as self-modification, the permission must live in a settings file, not just in the conversation. Plan for this at the start of any session that touches agent configuration.
