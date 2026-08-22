---
title: A capability field with no call sites enforces nothing — assert enforcement by its call sites, not its presence
date: 2026-08-22
category: journal
tags: [security, gates]
confidence: learned
source: private-work
---

A gateway's principal model carried a `capabilities` field, and the surrounding documentation asserted that an empty capability set granted nothing by default. In practice, the function that actually checks a capability against a request was called from exactly one of the nine routes that should have depended on it — the other eight enforced nothing, regardless of what the field or the documentation claimed.

General rule: whether an access-control mechanism is actually enforced is a fact about its call sites, not about the existence of the field, enum, registry, or documentation describing it. Before trusting that a capability model, flag, or permission field protects a given route, grep for where the checker function that reads it is actually invoked along that route's request path — a model that exists but isn't called from most of the surfaces it's meant to protect is decoration, not a control.
