---
title: A third-party API key and its paired secret (like a webhook signing secret) are account-and-mode scoped — verify pairing empirically, not by dashboard context
date: 2026-07-17
category: infra
tags: [boundaries, contracts, release, multi-repo]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A recurring class of integration failure: a provider issues credentials in matched pairs (an API key on one side, a webhook signing secret or similar counterpart on the other), and those pairs are scoped to a specific account AND a specific mode (live vs test) within that account. Two separate incidents in the same integration surfaced two different ways this pairing breaks silently.

First, when an organization has multiple near-identically-named accounts with the same provider (a live account and a separately-named "sandbox" account, in addition to that live account's own built-in test mode), it is easy to register a webhook endpoint or copy a signing secret while the provider's dashboard is silently showing a DIFFERENT account than the one the deployed application's API key actually belongs to. A key from one account, paired with a secret from another, will never successfully verify a signed request — every delivery fails identically ("invalid signature"), and the failure gives no hint about WHICH side is mismatched. The only reliable tell is comparing an account-scoped fragment embedded in object identifiers (many providers embed a short account fragment inside their object IDs) between the account the CLI/API key resolves to and the account the dashboard URL is currently showing.

Second, even within a single correctly-identified account, editing an existing integration's endpoint URL (for example, repointing a test-mode endpoint from a staging URL to a production URL, or vice versa) does not automatically rotate that endpoint's signing secret — so a URL edit alone can silently misroute test-mode traffic into a production code path (or the reverse) while the old secret remains valid and gives no error signal, just a spike in delivery failures that isn't obviously a routing problem.

**The fix is procedural, not a one-time correction:** before copying any secret or trusting a dashboard's context, verify empirically which account you are actually looking at — call an authenticated "who am I" style endpoint with the credential the application actually uses and compare its account identifier against what the dashboard shows, rather than trusting visual context or recent-click history. After any change to a webhook endpoint's URL or an account's credentials, the end-to-end witness is a real, targeted test delivery to that specific endpoint, confirmed by its own delivery log — not "the configuration looks right."
