#!/usr/bin/env python3
"""Check vault notes against the vault guide's tags and folders.

Author: Ibrahim AbuAlhaol

Usage:
    python3 check_guide.py [vault-root] [path ...] [--strip] [--guide FILE]

Everything is read from the guide (Systems/vault-guide.md by default), so a
customized guide is checked as written:

  * Tags: the allowed values are the `#facet/value` entries under each
    "### Facet:" heading of "## Tag Charter", and each facet's count comes from
    its "Apply exactly 1" / "Apply 1-3" / "Apply as needed" sentence.
  * Folders: the paths in the "## Folder Hierarchy" code block.

Reported, per markdown note outside the exempt set:

  unknown tag     a tag (frontmatter or inline #tag) the guide does not list
  facet count     a mandatory facet missing, or more values than allowed
  raw tag         any tag in raw/ (sources are never tagged)
  folder          a file (any type) in a folder the guide does not list, or
                  loose at the vault root

raw/<topic>/ and wiki/<topic>/ topics are free, one level deep. Exempt: +/,
dot-paths, HOME.md, ME.md, GUIDE.html, Systems/vault-guide.md, wiki/index.md,
wiki/log.md; Excalidraw drawings (*.excalidraw.md) are checked for folders
only.

--strip clears non-compliant tags from the checked notes, and changes nothing
else: unknown frontmatter tags are removed (the tags: key goes when empty);
an unknown inline tag loses its `#`, or is removed outright on a line that
holds only tags; in raw/ the frontmatter tags go and every inline tag is
escaped to `\\#` (it renders the same, but is no longer a tag). It never adds
tags: choosing the guide's values is judgment, not mechanics.

Exits 1 when anything is reported (after --strip: anything left).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GUIDE = Path("Systems/vault-guide.md")
FIXED_FILES = {
    "HOME.md",
    "ME.md",
    "GUIDE.html",
    "Systems/vault-guide.md",
    "wiki/index.md",
    "wiki/log.md",
}
TOPIC_DIRS = {"raw", "wiki"}
INBOX = "+"

GUIDE_TAG_RE = re.compile(r"`#([a-z0-9-]+)/([a-z0-9-]+)`")
APPLY_RE = re.compile(r"Apply (?:exactly )?(\d+)(?:\s*[–-]\s*(\d+))?")
FOLDER_LINE_RE = re.compile(r"^\s*/([^\s/][^\s]*?)/?\s*$")

# Obsidian's tag syntax: letters, digits, _ - /, at least one non-digit, and
# not glued to a word, URL, link anchor, or HTML entity.
INLINE_TAG_RE = re.compile(r"(?<![^\s,;])(\\?)#([A-Za-z0-9_/-]*[A-Za-z_/-][A-Za-z0-9_/-]*)")
TAGS_ONLY_LINE_RE = re.compile(r"^\s*(?:tags?\s*:\s*)?(?:#[A-Za-z0-9_/-]+[\s,]*)+$", re.I)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN_RE = re.compile(r"(`+)(.*?)\1")
FM_TAGS_RE = re.compile(r"^(tags?)\s*:\s*(.*)$", re.I)
FM_ITEM_RE = re.compile(r"^\s*-\s*(.*)$")


@dataclass
class Charter:
    values: set[str] = field(default_factory=set)
    counts: dict[str, tuple[int, int | None]] = field(default_factory=dict)
    folders: set[str] = field(default_factory=set)


def section(text: str, heading: str) -> str:
    match = re.search(rf"^##\s+{heading}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def read_charter(text: str) -> Charter:
    charter = Charter()
    for block in re.split(r"^###\s+Facet:.*$", section(text, "Tag Charter"), flags=re.M)[1:]:
        tags = GUIDE_TAG_RE.findall(block)
        if not tags:
            continue
        facet = tags[0][0]
        charter.values.update(f"{f}/{v}" for f, v in tags)
        apply = APPLY_RE.search(block)
        if apply:
            low = int(apply.group(1))
            charter.counts[facet] = (low, int(apply.group(2) or low))
        else:
            charter.counts[facet] = (0, None)

    code = re.search(r"^```[^\n]*\n(.*?)^```", section(text, "Folder Hierarchy"), re.M | re.S)
    for line in (code.group(1) if code else "").splitlines():
        match = FOLDER_LINE_RE.match(line)
        if match:
            charter.folders.add(match.group(1))
    return charter


# --- note parsing -----------------------------------------------------------


def split_frontmatter(text: str) -> tuple[list[str], list[str]]:
    """(frontmatter lines without the --- fences, body lines)."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1 :]
    return [], lines


def clean(tag: str) -> str:
    return tag.strip().strip("'\"").lstrip("#").strip()


def frontmatter_tags(fm: list[str]) -> tuple[list[str], tuple[int, int] | None]:
    """Tags and the (start, end) line span of the tags key, if any."""
    for i, line in enumerate(fm):
        match = FM_TAGS_RE.match(line)
        if not match:
            continue
        value = match.group(2).strip()
        end = i + 1
        if value:
            items = value.strip("[]").split(",") if value.startswith("[") else re.split(r"[,\s]+", value)
        else:
            items = []
            while end < len(fm) and FM_ITEM_RE.match(fm[end]):
                items.append(FM_ITEM_RE.match(fm[end]).group(1))
                end += 1
        return [t for t in map(clean, items) if t], (i, end)
    return [], None


def code_mask(line: str) -> str:
    """The line with inline code spans blanked, positions preserved."""
    return CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), line)


def inline_tags(body: list[str]) -> list[tuple[int, re.Match]]:
    found, fenced = [], False
    for n, line in enumerate(body):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in INLINE_TAG_RE.finditer(code_mask(line)):
            if not match.group(1):  # already escaped
                found.append((n, match))
    return found


# --- checks -----------------------------------------------------------------


def exempt(rel: Path) -> bool:
    return (
        any(p.startswith(".") for p in rel.parts)
        or rel.parts[0] == INBOX
        or rel.as_posix() in FIXED_FILES
    )


def folder_problem(rel: Path, charter: Charter) -> str | None:
    parent = rel.parent
    if parent == Path("."):
        return "loose file at the vault root"
    top = parent.parts[0]
    if top in TOPIC_DIRS:
        return None if len(parent.parts) == 2 else f"{top}/ files go exactly one level down: {top}/<topic>/"
    if parent.as_posix() in charter.folders:
        return None
    return f"folder {parent.as_posix()}/ is not in the guide"


def is_note(rel: Path) -> bool:
    return rel.suffix == ".md" and not rel.name.endswith(".excalidraw.md")


def check_file(vault: Path, rel: Path, charter: Charter, strip: bool) -> list[str]:
    problems = []
    folder = folder_problem(rel, charter)
    if folder:
        problems.append(f"folder: {folder}")
    if not is_note(rel):
        return problems

    path = vault / rel
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    fm_tags, span = frontmatter_tags(fm)
    inline = inline_tags(body)
    in_raw = rel.parts[0] == "raw"

    if strip:
        fm, body = strip_tags(fm, body, fm_tags, span, inline, charter, in_raw)
        new = ("---\n" + "\n".join(fm) + "\n---\n" if fm else "") + "\n".join(body)
        if new != text:
            path.write_text(new, encoding="utf-8")
        fm_tags, _ = frontmatter_tags(fm)
        inline = inline_tags(body)

    tags = fm_tags + [m.group(2) for _, m in inline]
    if in_raw:
        problems += [f"raw tag: {t}" for t in dict.fromkeys(tags)]
        return problems

    problems += [f"unknown tag: {t}" for t in dict.fromkeys(tags) if t not in charter.values]
    known = {t for t in tags if t in charter.values}
    for facet, (low, high) in charter.counts.items():
        n = sum(1 for t in known if t.split("/")[0] == facet)
        if n < low or (high is not None and n > high):
            want = f"{low}" if low == high else f"{low}-{high}" if high else f"{low}+"
            problems.append(f"facet count: {facet} has {n}, needs {want}")
    return problems


def strip_tags(fm, body, fm_tags, span, inline, charter, in_raw):
    if span:
        keep = [] if in_raw else [t for t in fm_tags if t in charter.values]
        start, end = span
        fm = fm[:start] + ([f"tags: [{', '.join(keep)}]"] if keep else []) + fm[end:]

    by_line: dict[int, list[re.Match]] = {}
    for n, match in inline:
        if in_raw or match.group(2) not in charter.values:
            by_line.setdefault(n, []).append(match)
    drop = set()
    for n, matches in by_line.items():
        line = body[n]
        tags_only = TAGS_ONLY_LINE_RE.match(line) and not in_raw
        for match in reversed(matches):  # right to left keeps offsets valid
            s, e = match.span()
            if in_raw:
                line = line[:s] + "\\#" + match.group(2) + line[e:]
            elif tags_only:
                line = line[:s] + line[e:]
            else:
                line = line[:s] + match.group(2) + line[e:]
        if tags_only:
            line = re.sub(r"\s{2,}", " ", line).rstrip(" ,")
            if re.fullmatch(r"\s*(tags?\s*:)?\s*", line, re.I):
                drop.add(n)
        body[n] = line
    return fm, [line for n, line in enumerate(body) if n not in drop]


def vault_files(vault: Path) -> list[Path]:
    return sorted(
        p.relative_to(vault)
        for p in vault.rglob("*")
        if p.is_file() and not exempt(p.relative_to(vault))
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check notes against the vault guide.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("paths", nargs="*", type=Path, help="vault-relative files to check")
    parser.add_argument("--strip", action="store_true", help="clear non-compliant tags")
    parser.add_argument("--guide", type=Path, help=f"guide file (default: <root>/{GUIDE})")
    args = parser.parse_args(argv[1:])

    vault = args.root.resolve()
    guide = args.guide or vault / GUIDE
    if not guide.is_file():
        print(f"no vault guide at {guide}; nothing to check against")
        return 0
    charter = read_charter(guide.read_text(encoding="utf-8"))

    files = [p for p in args.paths if not exempt(p)] if args.paths else vault_files(vault)
    total = 0
    for rel in files:
        problems = check_file(vault, rel, charter, args.strip)
        for problem in problems:
            print(f"{rel.as_posix()}: {problem}")
        total += len(problems)
    print(f"\n{len(files)} file(s) checked, {total} guide violation(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
