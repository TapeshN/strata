#!/usr/bin/env python3
"""Validate strata entries against schema.md contract.

Checks:
  - Required frontmatter fields present with valid values
  - category frontmatter matches the directory the file lives in
  - implementation_target (if present) is a valid value
  - No floating .md files in the repo root or outside a known category dir
  - Non-empty body

Exit 0 on success, 1 on any failure.
"""

import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

SKIP_ROOT_FILES = {"README.md", "CHANGELOG.md", "schema.md"}
SKIP_DIRS = {".git", ".github", ".claude"}

VALID_CATEGORIES = {
    "agents", "mcp", "rag", "guardrails", "orchestration",
    "evals", "infra", "skills", "journal",
}

VALID_CONFIDENCE = {"learned", "hypothesis", "speculation"}
VALID_SOURCE = {"private-work", "first-principles", "reading", "conversation"}
VALID_IMPLEMENTATION_TARGET = {
    "agent-guardrails", "coordinator-layer", "client-rules",
    "shared-prompts", "infra-tooling",
}

REQUIRED_FIELDS = {"title", "date", "category", "tags", "confidence", "source"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

GUARDRAIL_MISSING_TARGET_WARNING = True


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Returns ({}, content) on parse failure."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---\n", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4:]
    fm: dict = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm, body


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single entry file."""
    errors: list[str] = []
    warnings: list[str] = []
    rel = path.relative_to(REPO_ROOT)

    content = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    if not fm:
        errors.append(f"{rel}: missing or unparseable frontmatter (file must start with ---)")
        return errors, warnings

    for field in REQUIRED_FIELDS:
        if field not in fm or not fm[field]:
            errors.append(f"{rel}: missing required field '{field}'")

    date_val = fm.get("date", "")
    if date_val and not DATE_RE.match(date_val):
        errors.append(f"{rel}: invalid date format '{date_val}' (expected YYYY-MM-DD)")

    cat = fm.get("category", "")
    if cat:
        if cat not in VALID_CATEGORIES:
            errors.append(
                f"{rel}: invalid category '{cat}' — must be one of {sorted(VALID_CATEGORIES)}"
            )
        elif path.parent.name != cat:
            errors.append(
                f"{rel}: category '{cat}' doesn't match directory '{path.parent.name}'"
            )

    conf = fm.get("confidence", "")
    if conf and conf not in VALID_CONFIDENCE:
        errors.append(f"{rel}: invalid confidence '{conf}'")

    src = fm.get("source", "")
    if src and src not in VALID_SOURCE:
        errors.append(f"{rel}: invalid source '{src}'")

    impl = fm.get("implementation_target", "")
    if impl and impl not in VALID_IMPLEMENTATION_TARGET:
        errors.append(
            f"{rel}: invalid implementation_target '{impl}' — must be one of "
            f"{sorted(VALID_IMPLEMENTATION_TARGET)}"
        )
    elif not impl and cat == "guardrails" and GUARDRAIL_MISSING_TARGET_WARNING:
        warnings.append(
            f"{rel}: guardrails entry has no implementation_target — consider setting it "
            f"so the feedback loop stays deterministic"
        )

    if not body.strip():
        errors.append(f"{rel}: entry body is empty")

    return errors, warnings


def check_floating_docs() -> list[str]:
    """Find .md files in the repo root that aren't in the allowlist."""
    errors = []
    for md_file in REPO_ROOT.glob("*.md"):
        if md_file.name not in SKIP_ROOT_FILES:
            errors.append(
                f"{md_file.relative_to(REPO_ROOT)}: floating doc — "
                f".md files must live in a category directory"
            )
    return errors


def main() -> int:
    all_errors: list[str] = []
    all_warnings: list[str] = []
    entry_count = 0

    all_errors.extend(check_floating_docs())

    for category in sorted(VALID_CATEGORIES):
        cat_dir = REPO_ROOT / category
        if not cat_dir.exists():
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name in SKIP_ROOT_FILES:
                continue
            entry_count += 1
            errs, warns = validate_file(md_file)
            all_errors.extend(errs)
            all_warnings.extend(warns)

    if all_warnings:
        print(f"⚠  {len(all_warnings)} warning(s):\n")
        for w in all_warnings:
            print(f"  {w}")
        print()

    if all_errors:
        print(f"❌ Validation failed — {len(all_errors)} error(s):\n")
        for e in all_errors:
            print(f"  {e}")
        return 1

    cats_with_entries = sum(
        1 for c in VALID_CATEGORIES if any((REPO_ROOT / c).glob("*.md"))
    )
    print(
        f"✅ {entry_count} entries valid across "
        f"{cats_with_entries}/{len(VALID_CATEGORIES)} categories"
    )
    if all_warnings:
        print(f"   ({len(all_warnings)} warning(s) above — not blocking)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
