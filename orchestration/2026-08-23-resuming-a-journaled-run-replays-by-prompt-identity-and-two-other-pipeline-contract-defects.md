---
title: Resuming a journaled run replays by prompt identity — plus two other pipeline contract defects that halt or leak work
date: 2026-08-23
category: orchestration
tags: [durable-execution, contracts, lifecycle, workflows]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A subscription usage cap fired mid-afternoon and killed every in-flight stage of several multi-stage runs at once. Completed stages were already in the run journal; the killed ones were not. Resuming each run from its journal replayed the cached stages and re-ran only the ones that died — which worked, but only because nothing in the script had been edited in between.

That replay is keyed on the stage's prompt text. Changing a single cosmetic word in a COMPLETED stage's prompt — a label reading "slice 6 of 6" updated to "of 7" — would invalidate that stage's cache entry and re-run a finished, side-effecting build stage on top of its own commits. So: before resuming, diff the script against what actually ran; never edit a completed stage's prompt; and detach follow-on work into a separate script instead of extending a live run's stage list. Combined with a push at every slice, a usage cap becomes a pause rather than a loss.

Second defect, same afternoon: a stage returned a structured "blockers" list and the orchestrating script stopped the entire lane whenever that list was non-empty. The builders had used the field for a design question and a release note after a fully green build, and the lane halted on a healthy result. A field whose mere presence halts a pipeline is a kill switch, and a kill switch needs a TYPED value rather than free text — halt only on an explicitly prefixed marker, and tell producers in the same prompt where non-halting notes belong instead. Generally: any schema field an orchestrator branches on should be specified by the effect it triggers, not by what its name suggests to a writer.

Third: every coordinator turn had been ending by starting a background wait for a file that some later turn was supposed to create, and nothing ever created it. Dozens of sleeping loops accumulated on the machine before anyone noticed the pile. A background wait whose exit condition nothing will ever satisfy is a process leak dressed as patience. Either wait on a real observable condition — a journal result count, a pull-request state — with a bounded timeout, or simply end the turn; asynchronous notifications arrive on their own.
