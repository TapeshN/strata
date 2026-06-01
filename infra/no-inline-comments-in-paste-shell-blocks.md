---
title: Never put inline comments in a shell block meant for a human to paste
date: 2026-05-30
category: infra
tags: [release, ci, command-formatting]
confidence: learned
source: private-work
---

Interactive `zsh` does not treat `#` as a comment by default (`interactivecomments` is off). A multi-command release block handed to a user with inline `# ...` annotations was parsed with those comments as *arguments*: parenthetical notes hit glob-qualifier errors, word-notes became stray arguments to the publish command, and a `stash` that never ran left the tree dirty so a later pull aborted — ending with a version tag pushed onto the wrong commit.

The fix is a formatting rule: commands only inside a block meant for paste; put every explanation in prose *above* the block. Assume the default interactive shell is `zsh`.

General lesson: a code block you hand to a human is executed verbatim in their shell, not yours, and not in a comment-tolerant context. The safe default is zero inline comments in any paste-ready shell block; a lint that rejects `#` inside fenced shell blocks can enforce it.
