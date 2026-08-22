---
title: Deferred repricing that only applies after a billing boundary can never change the invoice generated at that boundary
date: 2026-08-22
category: journal
tags: [money, billing]
confidence: learned
source: private-work
---

A price-change pipeline applied pending rate increases only once their effective date had passed, then made a proration-free swap with the payment processor. By the time that swap ran, the processor had already generated the period's renewal invoice at the old rate — so the change consistently landed one billing period later than intended, and the notice shown to the affected customer described a change that hadn't actually taken effect yet.

General rule: when a downstream provider (a payment processor) generates its own invoice at a fixed boundary independent of your system, any price/plan change meant to take effect exactly at that boundary must be scheduled with the provider before the boundary occurs — via a pre-scheduled provider-side change, or an approval-time swap — while keeping your own system's record of the effective date accurate to when it should visibly apply. Applying the change only after the boundary has already passed guarantees it misses the very event it was meant to affect.
