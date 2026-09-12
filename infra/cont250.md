---
title: "A safety registry was missing the one consumer that mattered, and metered timers ran for days before anyone noticed"
date: 2026-09-09
category: infra
tags: ["registry-is-the-control", "absent-consumer-equals-no-rule", "sri-repin", "metered-timers-unattributed", "found-by-watching-a-bill"]
confidence: learned
source: private-work
---

when a rule names "every consumer", the enumeration IS the control — audit it against reality (who actually pins this?) rather than trusting the list. When a job spends metered budget on a timer, its cost must appear somewhere a human reads without going looking.

both are the same defect at different scales — a control that describes the world instead of being derived from it. Ask of any registry: *what happens to something real that is not in this list?* If the answer is "it breaks silently", the list needs a check that discovers members, not a convention that they get added.
