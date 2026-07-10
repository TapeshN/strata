---
title: In-browser MCP screenshots may be display-only, not files on disk
date: 2026-07-10
category: mcp
tags: [mcp, headless-browser, screenshots, tooling-verification, macos]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

**Rule: an in-browser MCP tool's "screenshot" may only be a display artifact — not a file on disk — so a real image asset needs a headless-browser pipeline you control end-to-end.**

Screenshot tools exposed through an in-chat MCP browser integration are often built to render the image inline for the conversation, not to persist it as a file at a path the rest of your toolchain can read. If you try to capture a product screenshot that way and then go looking for it on the filesystem — by search, by recent-file listing, by any means — it simply isn't there, because it was never written; it only ever existed as a transient display payload.

**What happened:** an attempt to capture homepage/product screenshots for use as real image assets went through an MCP browser tool's screenshot capability. The images rendered fine in the conversation, but a filesystem search for the output (by likely id, by recent modification time) turned up nothing, because the tool doesn't write to disk at all — it only streams pixels back to the display layer.

**How to apply:** when you need an actual image asset (not just something to look at in the moment), don't reach for a chat-embedded screenshot tool — drive a headless browser you control directly, on the machine's own filesystem. On macOS this can be done entirely with built-in/standard tools: launch the browser in headless mode with an explicit window size and a virtual-time budget, write straight to a PNG path, then downsample/convert with a system image utility if you need a smaller JPEG. If the target page requires authentication, point the headless browser at whatever dev/test login redirect your app exposes so the redirect chain sets the session cookie and the final page renders correctly in a single capture — no separate login step needed. The general principle: before trusting any tool's "save/export" affordance, verify it actually persists to a path you can read, especially when the artifact needs to survive past the current conversation turn or feed a downstream pipeline.
