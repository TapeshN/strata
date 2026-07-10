---
title: A pipeline's exit status belongs to its last stage, and a closing claim needs its evidence stated right beside it
date: 2026-07-10
category: guardrails
tags: [ci, gating, verify-then-merge]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

When a verification command's output is piped through a second command (for example, to shorten or filter what's displayed) and the overall success/failure of that combined line is then checked, the checked exit status belongs to the LAST command in that pipe — not to the actual verification step earlier in the chain. A real type-check or lint step can report several genuine errors, get piped through a display-limiting command that itself always exits successfully, and the combined line still reports an overall success. This produces a false-positive "all clear" on a genuinely broken gate, and it is especially dangerous because the failing output is often still visible on screen right next to the false "success" — easy to miss if the success message is what gets acted on. The durable fix is to capture a gate's exit status directly, before any piping, and never assert a gate's pass/fail verdict through a piped command chain.

A related discipline, from the same stretch of work: at the end of any long autonomous work session, a closing message that simply asserts "this was merged, verified, and is done" is not itself proof of anything — the actual evidence for those claims may be scattered across dozens of earlier tool outputs that the reader never sees. The evidence a human can actually evaluate is only what appears in the final message; if a completion claim doesn't carry its supporting evidence adjacent to it, the safest assumption is that the claim hasn't been shown, even if the work was genuinely done — so before closing out a long session, re-run the key verifying checks one more time and show their real output next to each completion claim.

A third, unrelated but similarly mechanical lesson: a version-control commit message written through an interactive shell can have certain special characters inside it (particularly backticks, and certain other shell metacharacters) silently interpreted and stripped by the shell itself before the message is ever recorded — the commit still succeeds, so there's no error to notice, but the permanent record of that commit is quietly corrupted, missing exactly the technical detail it was written to preserve. Any commit message containing such characters should be passed through a method that is immune to shell interpretation (piping a heredoc-style block with a quoted delimiter into the commit command, rather than passing the message as a directly shell-expanded string).

A fourth, final lesson: a "stale premise" — believing something is still true, or still needs doing, when it has already changed — can come from a person's own recollection just as easily as from an out-of-date document. Any inherited instruction that describes the current state of some work should be verified against the actual, current state of the relevant system before acting on it, regardless of whether that instruction came from a stale document or from someone's memory of a moment that has since passed — silently redoing already-completed work is a worse outcome than pausing to point out the discrepancy.
