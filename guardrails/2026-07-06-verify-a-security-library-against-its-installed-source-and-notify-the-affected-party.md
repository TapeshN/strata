---
title: Verify a security-sensitive library's real behavior against its installed source, and treat notifying the affected party as part of the definition of done
date: 2026-07-06
category: guardrails
tags: [boundaries, contracts]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Before shipping a feature that lets a user change their own account's email address, the make-or-break security question — does changing that field actually move which credentials can sign in, or does the authentication library key sign-in on a separate, unrelated identifier — could not be answered by a generic mental model of "how auth libraries usually work." It was settled correctly only by reading the actual installed dependency's own source for its sign-in lookup logic, which confirmed the email field genuinely was the login key for that specific library and version.

Once that question was settled, an independent review of the same feature surfaced two further, easy-to-miss gaps that a purely functional test would not catch: a uniqueness-violation error message that doubled as an oracle revealing whether a given account already existed across tenants (a global uniqueness check needs a response that does not confirm existence), and a missing audit trail plus missing notification for a change that revokes the old session's continued access to that identity.

Two generalizable rules follow. First, any security-relevant claim about how a third-party library behaves should be settled by reading that library's own installed source for the specific behavior in question, not by assuming a common pattern applies. Second, for any feature that changes an account's identity in a way that revokes existing access, the definition of done includes an audit event for the change and a notification to the party who is losing access — not just a working access-control gate, since the person losing access is exactly the one who most needs to be told.
