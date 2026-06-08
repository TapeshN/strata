---
title: TypeScript legacy module resolution cannot find packages that use subpath exports
date: 2026-06-02
category: infra
tags: [ci, interfaces]
confidence: learned
source: private-work
---

TypeScript's legacy module resolution cannot find packages that export their types through subpath entries in `package.json`. This causes type errors on imports like `pkg/subpath` even when the package ships correct type definitions at those paths. The resolution mode looks for `pkg/subpath.d.ts` or `pkg/subpath/index.d.ts` directly — it does not read the `exports` map.

The fix: upgrade to a modern module resolution mode that reads the package's exports map. Any project using test frameworks or reporting libraries that ship types at subpath entrypoints should use modern resolution from the start; adding such libraries to a project using legacy resolution without upgrading it first will produce type errors.

General lesson: when a package ships types at subpath entrypoints and your TypeScript project uses legacy module resolution, the fix is always the same — upgrade the resolution mode, not the import style.
