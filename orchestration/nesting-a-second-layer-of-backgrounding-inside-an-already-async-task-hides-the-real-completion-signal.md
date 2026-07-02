---
title: Nesting a second layer of backgrounding inside an already-async task hides the real completion signal, and recognizing it once does not prevent repeating it
date: 2026-07-02
category: orchestration
tags: [subagents, autonomy, lifecycle]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Twice within the same working session, a long-running command was launched using a harness's own asynchronous/background execution parameter, but the command string itself ALSO ended in a shell-level background operator. Both times, the harness reported "completed" almost instantly — because the outer shell setup (redirection, environment prep) returned immediately, and that's what the harness was actually tracking — while the real work kept running detached and undetected for minutes afterward. Both times, the mistake was only caught by manually inspecting the live process list.

The mechanism: an async/background execution parameter already tells the calling harness to background the whole command and report on its real exit. Adding a second, independent layer of backgrounding inside the command string creates a process that the harness's completion tracking is structurally blind to.

What makes this worth recording twice is that recognizing the mistake once in a session did not prevent repeating it minutes later — the underlying impulse (wanting to "fire and forget" a slow command under time pressure) recurs, and the fix isn't yet automatic. The durable rule: never combine a harness's own async/background parameter with a second, manual background operator inside the command string — pick exactly one layer. If a live process genuinely needs to be watched from outside the tool that started it, the watch-loop itself should be the only thing backgrounded, and it should go through the harness's own async parameter rather than a nested one.
