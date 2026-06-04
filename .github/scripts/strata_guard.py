#!/usr/bin/env python3
"""strata content guard — CI gate for the public learning journal.

Strata is a PUBLIC paraphrased-learning repo. Content is supposed to arrive only
via the /deposit pipeline, which paraphrases and IP-gates each entry. A
hand-authored PR (docs, config, a stray CLAUDE.md) bypasses that pipeline — this
gate is the backstop that runs on EVERY pull request and push to main.

Two checks:

  1. SCHEMA   — every non-exempt ``*.md`` must begin with the ``schema.md``
                frontmatter block (``---``).
  2. NO LEAK  — no tracked text file may contain an absolute machine path or a
                named private control-plane artifact (the exact class of leak
                that put private paths into this public repo).

Proprietary identifiers (client / product names) are deliberately NOT listed in
this file — it lives in a public repo. They belong in an optional repo secret
``STRATA_BLOCKLIST`` (newline-separated, ``#`` comments allowed), read at run
time. If the secret is unset the proprietary check is skipped with a warning;
the structural checks always run.

Exit 0 = clean. Exit 1 = one or more violations (printed as ``path:line``).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

# --- frontmatter (schema.md) ------------------------------------------------
# schema.md exempts these by name; .claude/ is Claude Code config and .github/
# is CI tooling — neither are journal entries.
EXEMPT_BASENAMES = {"README.md", "CHANGELOG.md", "schema.md"}
EXEMPT_PREFIXES = (".claude/", ".github/")

# --- leak patterns ----------------------------------------------------------
# Public-safe and SPECIFIC: anchored to real artifact names / absolute paths so
# they catch genuine leaks without tripping on paraphrased prose that merely
# discusses concepts ("control plane", "a handoff doc") in the abstract.
# Case-sensitive on purpose — "handoff doc" must pass, "HANDOFF.md" must not.
LEAK_PATTERNS: list[tuple[str, str]] = [
    (r"/Users/", "absolute macOS home path"),
    (r"/home/[A-Za-z0-9._-]+/", "absolute Linux home path"),
    (r"\bAutomation_Projects\b", "private workspace root name"),
    (r"WorkTrees_Automation_Projects", "private worktrees root name"),
    (r"strata-sync", "private deposit-ledger filename"),
    (r"\bagents-inbox\b", "private control-plane inbox dir"),
    (r"\bLEARNINGS\.md\b", "private learnings ledger"),
    (r"\bHANDOFF\.md\b", "private handoff doc"),
    (r"PARALLEL-PLAN", "private execution-plan doc"),
    (r"EXECUTION-PLAN", "private execution-plan doc"),
    (r"\$TAP_CORE_BLOCKLIST", "private blocklist env var"),
]

# This gate carries the pattern list itself — never scan it for leaks.
LEAK_SCAN_SKIP_PREFIXES = (".github/",)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout
    return [p for p in out.splitlines() if p]


def is_frontmatter_exempt(path: str) -> bool:
    if os.path.basename(path) in EXEMPT_BASENAMES:
        return True
    return path.startswith(EXEMPT_PREFIXES)


def secret_patterns() -> list[tuple[str, str]]:
    raw = os.environ.get("STRATA_BLOCKLIST", "")
    terms = [
        t.strip()
        for t in raw.splitlines()
        if t.strip() and not t.strip().startswith("#")
    ]
    return [(re.escape(t), "STRATA_BLOCKLIST term") for t in terms]


def _looks_binary(data: bytes) -> bool:
    return b"\x00" in data[:4096]


def main() -> int:
    files = tracked_files()
    violations: list[tuple[str, str, int, str]] = []  # kind, path, line, detail

    # 1) schema / frontmatter
    for path in files:
        if not path.endswith(".md") or is_frontmatter_exempt(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as fh:
                first = fh.readline()
        except (OSError, UnicodeDecodeError):
            continue
        if first.lstrip("﻿").rstrip("\n") != "---":
            violations.append(
                ("SCHEMA", path, 1, "missing frontmatter block (schema.md requires '---')")
            )

    # 2) leak scan (structural + optional secret-provided proprietary terms)
    have_secret = bool(os.environ.get("STRATA_BLOCKLIST", "").strip())
    compiled = [(re.compile(p), why) for p, why in LEAK_PATTERNS]
    compiled += [(re.compile(p), why) for p, why in secret_patterns()]

    for path in files:
        if path.startswith(LEAK_SCAN_SKIP_PREFIXES):
            continue
        try:
            with open(path, "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        if _looks_binary(raw):
            continue
        for lineno, line in enumerate(raw.decode("utf-8", "ignore").splitlines(), 1):
            for rx, why in compiled:
                if rx.search(line):
                    violations.append(("LEAK", path, lineno, why))

    # report
    if not have_secret:
        print(
            "::warning::STRATA_BLOCKLIST secret not set — proprietary-term check "
            "skipped (structural schema + leak checks still ran)."
        )

    if violations:
        print(f"\nstrata-guard FAILED — {len(violations)} violation(s):\n")
        for kind, path, lineno, detail in violations:
            print(f"  [{kind}] {path}:{lineno} — {detail}")
        print(
            "\nThis repo is public. Entries must carry schema.md frontmatter, and "
            "must never contain machine paths or private control-plane artifact "
            "names. Route learnings through /deposit (it paraphrases + IP-gates)."
        )
        return 1

    print("strata-guard PASSED — schema + leak checks clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
