---
title: A credential rotation is not done until the environment is clean on every live shell and application
date: 2026-06-10
category: guardrails
tags: [secrets, lifecycle, verify-dont-trust, boundaries]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A session-scoped environment variable export shadowed the credential store for an entire session. Five freshly issued credentials appeared to fail in sequence — each was valid; each was losing to the ghost value still present in the environment. Applications launched from that terminal inherited the exported value. Only when the terminal was identified and the export cleared did the sequence of apparent failures stop.

The rotation was operationally incomplete even though the new credential had been issued and stored correctly. Issuance and storage are two of the three steps; the third — clearing every path by which the old value can still be presented — was not part of the checklist.

A complete rotation protocol:

1. Issue and store the new credential in the credential store.
2. Search the live environment for any conflicting export: scan every active shell session, every `.env` file, and every environment file the running applications read. An environment variable takes precedence over the credential store for tools that check env first.
3. Restart long-lived applications that inherited the old value — launch them fresh rather than from a terminal that may still hold the export.
4. Verify liveness with a fresh extraction and a test call before declaring the rotation complete.
5. Revoke the old credential only after the new one has been confirmed live at every call site.

The class extends: any time a tool misbehaves in a way that looks like an expired credential but the credential appears valid, the first diagnostic step is to check whether an environment variable is presenting a different value than the credential store. Print the length and first-and-last characters; do not print the value itself.
