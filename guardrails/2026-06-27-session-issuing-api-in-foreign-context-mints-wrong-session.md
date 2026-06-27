---
title: A session-issuing API called in a foreign request context mints a session for the wrong principal
date: 2026-06-27
category: guardrails
tags: [security, hitl, autonomy, roles, lifecycle]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Authentication frameworks that issue a session on sign-up typically do so by setting a
session cookie in the current HTTP response context. When an authenticated operator
(an admin, a privileged user) calls the sign-up function inside a server action or
request handler — for example, to create a new account on behalf of someone else —
the session cookie issued belongs to the newly created account, not to the caller.
The calling operator's session is silently replaced.

This is not a bug in the authentication library. It is the correct behavior for a
session-issuing primitive: the caller of the session-issuing function becomes the
session holder. The bug is in the application layer that passes a session-bearing
request context to a function that issues a new session.

The fix is to use a non-session-issuing path for privileged account creation: write
the account directly to the credential store without going through the authentication
library's sign-up endpoint, or use an administrative API that explicitly skips session
issuance.

The generalizable rule: any sign-up or account-creation primitive that issues a session
must be called only where the caller intends to become the new session holder. In an
admin context where one principal creates credentials for another, the session-issuing
path is always wrong. The distinction between "create an account" (no session) and
"sign up" (creates account AND mints a session) is a load-bearing one that many
authentication libraries conflate in their primary API.
