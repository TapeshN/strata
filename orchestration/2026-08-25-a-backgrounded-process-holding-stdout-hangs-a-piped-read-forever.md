---
title: A backgrounded process holding stdout hangs a piped read forever
date: 2026-08-25
category: orchestration
tags: [workflow, subprocess, hang, witness, autonomy]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An agent started a long-running helper process in the background, then piped a later command's output through a line-limiting filter such as `tail`. The call never returned. The root cause: a filter like `tail` reading from a pipe waits for end-of-file on its input, and end-of-file only arrives once every process holding that pipe's write end has closed it — including a background child that inherited the same stdout file descriptor from the parent shell. The foreground command finishing does not close the pipe if a detached sibling is still holding it open, so the read blocks indefinitely with no error, and a session watching only for "did the command return" reads this as an unexplained hang rather than a specific, diagnosable cause.

The general rule for any orchestration system that runs shell commands: never pipe a command's output through a filter like `tail`/`head`/`grep` when a background process might be sharing its stdout — redirect to a file explicitly instead, and read the file afterward. Any background process should itself be started with output explicitly redirected to its own file, detached from the parent's descriptors, rather than left to inherit the caller's stdout by default. Separately, a liveness check for a long-running agent turn should distinguish "still working" from "silently blocked" by inspecting whether a child process is actually consuming resources or making progress, not just by elapsed time or turn count — a live child holding a pipe open for many minutes with no output is a specific, recognizable failure signature, distinct from ordinary slowness.
