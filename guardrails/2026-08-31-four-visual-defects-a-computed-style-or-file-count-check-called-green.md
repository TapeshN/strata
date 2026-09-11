---
title: Four visual defects that a computed-style or file-count check called green, because the check and the defect lived at different layers
date: 2026-08-31
category: guardrails
tags: [facade-green, rendering-verification, animation, verification-layer]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A single review session produced four distinct defects, each of which passed its own most obvious verification method. An unanchored exclude pattern in a file-sync step, matching on a bare directory name rather than an anchored path, silently deleted an unrelated feature directory that happened to share that name — the sync step itself reported a healthy file count and checksum, and the failure only surfaced two build steps later when a module could no longer resolve. An SVG "line draw" animation used a computed style (a dash-offset reaching zero) to decide it had finished drawing, but the browser's own path-length calibration undershot on long curved paths, so a meaningful fraction of the shapes visibly stopped short of complete while the style check reported every one of them done. A chained SMIL animation timing reference silently failed to fire because the browser's own timing-string parser read a hyphen inside a referenced element id as subtraction rather than as part of the identifier. And a screenshot meant to prove an animation reached its destination was captured at a viewport height that cropped the destination out of frame, so the "proof" showed nothing conclusive either way.

Each of these four is the same root shape wearing a different coat: the verification method and the actual defect live at different layers. A byte count or checksum answers "how much changed," not "which specific files changed." A computed style or attribute-presence check answers "was this property declared," not "what actually got painted." An attribute the code correctly wrote is not the same claim as "the runtime's own parser accepted it under its grammar." And the page's real content is not the same thing as whatever fell inside one particular capture window.

For any rendering-shaped defect, sample the actual rendered pixels or served bytes — never a computed style or a declared intent. For any file-moving or syncing step, diff the resulting file list — never trust a count or checksum alone. Treat a runtime's parser or grammar for any embedded identifier as its own thing to verify, not something guaranteed just because the specification allows it. And confirm a capture window is large enough to contain the actual target before treating a screenshot as proof of anything.
