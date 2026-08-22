---
title: A webhook that grants an entitlement must bind to the specific entitlement the payment actually paid for
date: 2026-08-22
category: journal
tags: [money, webhooks]
confidence: learned
source: private-work
---

A payment-processor webhook handler extended "the customer's newest recurring pass" whenever an invoice-paid event arrived. In practice this meant: an invoice for an unrelated product line extended a completely different entitlement; a zero-dollar anchor invoice generated internally by the app's own billing-day logic still granted a full new term; and a period end-date taken verbatim from the processor's line-item data (rather than derived from the product's own known interval) produced an entitlement extending years further than intended.

General rule: a webhook that grants or extends an entitlement in response to a payment event must resolve which specific entitlement was paid for by an identifier stamped in the processor's own metadata at the time the entitlement was created — never by "whichever one is newest." It should also check that a real, non-zero amount was actually paid and inspect the event's own reason/type field before treating it as a renewal, and clamp any period length taken from the processor to a sane, bounded multiple of the product's actual billing interval rather than trusting it verbatim.
