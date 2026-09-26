#!/usr/bin/env python3
"""Rename or move one vault file and rewrite every link to it.

Author: Ibrahim AbuAlhaol

Usage:
    python3 rename.py <vault-root> <old-path> <new-path> [--dry-run]

Paths are vault-relative. The file is moved (parent folders are created), and
every markdown file in the vault (dot-directories skipped) is updated:

  * markdown links and images, `[t](path)` / `![t](path)`, whose relative path
    resolves to the old file get the new relative path; `#anchors`, titles,
    `<angle brackets>` and `%20` encoding are kept
  * wikilinks and embeds, `[[name]]`, `![[name|alias]]`, `[[path/name#h]]`,
    that name the old file get the new name (a path-style link gets the new
    path)
  * the moved file's own relative markdown links are recomputed from its new
    folder

Fenced code blocks are left alone. It never overwrites: an existing new-path
is an error. When another file shares the old file's name, bare-name
wikilinks are ambiguous in Obsidian; they are reported and left unchanged.
--dry-run prints what would change and writes nothing.
"""

from __future__ import annotations

import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote, unquote

MD_LINK_RE = re.compile(r'(!?\[[^\]\n]*\]\()(<[^>\n]+>|[^)\s]+)((?:\s+"[^"\n]*")?\))')
WIKILINK_RE = re.compile(r"(!?\[\[)([^\]|#\n]+)((?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\])")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


class RenameError(Exception):
    pass


def visible(rel: Path) -> bool:
    return not any(part.startswith(".") for part in rel.parts)


def markdown_files(vault: Path) -> list[str]:
    return sorted(
        p.relative_to(vault).as_posix()
        for p in vault.rglob("*.md")
        if p.is_file() and visible(p.relative_to(vault))
    )


def link_name(rel: str) -> str:
    """How a bare wikilink names a file: notes without .md, others in full."""
    name = posixpath.basename(rel)
    return name[:-3] if name.endswith(".md") else name


def link_path(rel: str) -> str:
    return rel[:-3] if rel.endswith(".md") else rel


def resolve(from_dir: str, target: str) -> str | None:
    """Vault-relative path a relative link points at, or None if it leaves."""
    joined = posixpath.normpath(posixpath.join(from_dir, target))
    return None if joined.startswith("../") or joined == ".." else joined


def encode(target: str, style: str) -> str:
    if style == "angle":
        return f"<{target}>"
    if style == "pct":
        return quote(target, safe="/#.-_~")
    return f"<{target}>" if " " in target else target


def rewrite_md_links(line: str, old_dir: str, new_dir: str, old: str, new: str, moved: bool) -> str:
    def swap(m: re.Match) -> str:
        raw = m.group(2)
        style = "angle" if raw.startswith("<") else ("pct" if "%" in raw else "plain")
        target = raw[1:-1] if style == "angle" else unquote(raw)
        if SCHEME_RE.match(target) or target.startswith(("#", "/")):
            return m.group(0)
        path, _, anchor = target.partition("#")
        if not path:
            return m.group(0)
        points_at = resolve(old_dir, path)
        if points_at == old:
            dest = new
        elif moved and points_at is not None:
            dest = points_at
        else:
            return m.group(0)
        rel = posixpath.relpath(dest, new_dir or ".")
        rel = rel + (f"#{anchor}" if anchor else "")
        return m.group(1) + encode(rel, style) + m.group(3)

    return MD_LINK_RE.sub(swap, line)


def rewrite_wikilinks(line: str, old: str, new: str, ambiguous: bool, notes: list[str]) -> str:
    old_names = {link_name(old), posixpath.basename(old)}
    old_paths = {link_path(old), old}

    def swap(m: re.Match) -> str:
        target = m.group(2).strip()
        if "/" in target:
            if target not in old_paths:
                return m.group(0)
            replacement = new if target == old else link_path(new)
        else:
            if target not in old_names:
                return m.group(0)
            if ambiguous:
                notes.append(m.group(0))
                return m.group(0)
            replacement = posixpath.basename(new) if target.endswith(".md") else link_name(new)
        return m.group(1) + replacement + m.group(3)

    return WIKILINK_RE.sub(swap, line)


def rewrite(text: str, old_dir: str, new_dir: str, old: str, new: str,
            moved: bool, ambiguous: bool, notes: list[str]) -> str:
    lines, fenced = text.split("\n"), False
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            line = rewrite_md_links(line, old_dir, new_dir, old, new, moved)
            lines[i] = rewrite_wikilinks(line, old, new, ambiguous, notes)
    return "\n".join(lines)


def rename(vault: Path, old: str, new: str, dry_run: bool = False) -> list[str]:
    """Move old to new and rewrite links. Returns a report, one line per change."""
    old = posixpath.normpath(old.replace("\\", "/"))
    new = posixpath.normpath(new.replace("\\", "/"))
    for label, rel in (("old", old), ("new", new)):
        if rel.startswith("..") or posixpath.isabs(rel):
            raise RenameError(f"{label} path must be inside the vault: {rel}")
    if not (vault / old).is_file():
        raise RenameError(f"no such file: {old}")
    if (vault / new).exists():
        raise RenameError(f"refusing to overwrite: {new}")

    all_files = [
        p.relative_to(vault).as_posix()
        for p in vault.rglob("*")
        if p.is_file() and visible(p.relative_to(vault))
    ]
    ambiguous = any(f != old and link_name(f) == link_name(old) for f in all_files)

    report, notes = [], []
    for rel in markdown_files(vault):
        moved = rel == old
        path = vault / rel
        text = path.read_text(encoding="utf-8")
        old_dir = posixpath.dirname(rel)
        new_dir = posixpath.dirname(new) if moved else old_dir
        updated = rewrite(text, old_dir, new_dir, old, new, moved, ambiguous, notes)
        if updated != text:
            report.append(f"links updated: {new if moved else rel}")
            if not dry_run:
                path.write_text(updated, encoding="utf-8")

    for link in dict.fromkeys(notes):
        report.append(f"left unchanged (another file has the same name): {link}")
    if not dry_run:
        (vault / new).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(vault / old), str(vault / new))
    report.insert(0, f"{'would move' if dry_run else 'moved'}: {old} -> {new}")
    return report


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if a != "--dry-run"]
    if len(args) != 3:
        print("usage: rename.py <vault-root> <old-path> <new-path> [--dry-run]", file=sys.stderr)
        return 2
    try:
        report = rename(Path(args[0]).resolve(), args[1], args[2], "--dry-run" in argv)
    except RenameError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
