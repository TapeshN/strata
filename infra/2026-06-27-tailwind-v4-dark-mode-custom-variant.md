---
title: Tailwind v4 dark: variant silently ignores custom theme attributes
date: 2026-06-27
category: infra
tags: [tailwind, css, dark-mode, frontend]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

In Tailwind CSS v4, the `dark:` variant defaults to `@media (prefers-color-scheme: dark)` unless you tell it otherwise. If your app implements a user-controlled theme toggle by setting an attribute like `data-theme="dark"` on the root element (a very common pattern, since it lets a toggle button override the OS setting), every `dark:` utility class in the codebase silently stops working — Tailwind is still watching the OS media query, not your attribute. The visible symptom can look like a narrow, unrelated bug (in one real case, a set of status pills rendered with inverted colors after a light/dark toggle), which makes it easy to chase the wrong root cause and patch individual components instead of noticing the whole dark-mode system is disconnected.

What happened: a team built a manual theme toggle that stamps `data-theme` on `<html>`, assumed Tailwind's `dark:` classes would respond to it (as they did under Tailwind v3's default class-strategy behavior in many setups), and only caught the mismatch when a specific component looked visually wrong after toggling.

How to apply: whenever a Tailwind v4 project drives dark mode from anything other than the OS preference — a manual toggle, a stored user setting, a server-rendered attribute — explicitly rewire the variant with a `@custom-variant` declaration that matches your actual selector, e.g. targeting elements where `data-theme="dark"` is set on themselves or an ancestor. Do this once, in the global CSS entry point, before writing any `dark:` classes, rather than discovering it component-by-component after a toggle "looks broken." If several unrelated components all look subtly wrong after adding a theme toggle, suspect the variant wiring before suspecting each component.
