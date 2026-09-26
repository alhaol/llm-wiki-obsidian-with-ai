#!/usr/bin/env python3
"""Inventory and close out the vault's `+/` inbox for the Organize workflow.

Author: Ibrahim AbuAlhaol

Usage:
    python3 inbox.py list   [vault-root]
    python3 inbox.py finish [vault-root]

`list` prints one row per file in `+/` (dotfiles skipped) with a kind the agent
uses as a first guess, never a verdict:

  clip   markdown that already carries the raw-template header (> Source:)
  note   any other markdown
  asset  anything else (images, PDFs, audio, office files, ...)

and flags exact byte-for-byte duplicates of files already elsewhere in the
vault, so they can be dropped instead of filed twice.

`finish` runs after every item has been moved out. It removes empty
subdirectories of `+/`, keeps `+/.gitkeep` so the empty inbox stays in git, and
exits 1 listing whatever is still left. The vault root defaults to the current
working directory.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

INBOX = "+"
KEEP = ".gitkeep"
MARKDOWN = {".md", ".markdown"}

# Header lines of references/raw-template.md, as a clipper or a prior fetch
# would write them.
RAW_HEADER_RE = re.compile(r"^>\s*Source:\s*\S", re.MULTILINE)


def visible(path: Path, base: Path) -> bool:
    """True when no component below `base` is a dot-name (Obsidian hides those)."""
    return not any(part.startswith(".") for part in path.relative_to(base).parts)


def inbox_files(vault: Path) -> list[Path]:
    inbox = vault / INBOX
    if not inbox.is_dir():
        return []
    return sorted(p for p in inbox.rglob("*") if p.is_file() and visible(p, inbox))


def kind_of(path: Path) -> str:
    if path.suffix.lower() not in MARKDOWN:
        return "asset"
    head = path.read_text(encoding="utf-8", errors="replace")[:2000]
    return "clip" if RAW_HEADER_RE.search(head) else "note"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vault_digests(vault: Path, sizes: set[int]) -> dict[str, Path]:
    """Hash visible vault files outside +/ whose size matches an inbox file."""
    found: dict[str, Path] = {}
    inbox = vault / INBOX
    for path in vault.rglob("*"):
        if not path.is_file() or not visible(path, vault):
            continue
        if path.is_relative_to(inbox) or path.stat().st_size not in sizes:
            continue
        found.setdefault(digest(path), path)
    return found


def cmd_list(vault: Path) -> int:
    files = inbox_files(vault)
    if not files:
        print(f"{INBOX}/ is empty" if (vault / INBOX).is_dir() else f"no {INBOX}/ folder in {vault}")
        return 0

    known = vault_digests(vault, {f.stat().st_size for f in files})
    seen: dict[str, Path] = {}
    rows = []
    for path in files:
        h = digest(path)
        dup = known.get(h) or seen.get(h)
        seen.setdefault(h, path)
        rows.append(
            (
                path.relative_to(vault).as_posix(),
                kind_of(path),
                dup.relative_to(vault).as_posix() if dup else "",
            )
        )

    width = max(len(r[0]) for r in rows)
    for rel, kind, dup in rows:
        line = f"{rel.ljust(width)}  {kind:<5}"
        print(f"{line}  duplicate of {dup}" if dup else line)
    counts = {k: sum(1 for r in rows if r[1] == k) for k in ("note", "clip", "asset")}
    dups = sum(1 for r in rows if r[2])
    print(
        f"\n{len(rows)} item(s): {counts['note']} note, {counts['clip']} clip, "
        f"{counts['asset']} asset; {dups} duplicate(s)"
    )
    return 0


def cmd_finish(vault: Path) -> int:
    inbox = vault / INBOX
    inbox.mkdir(exist_ok=True)

    # Deepest first, so a parent empties once its children are gone.
    for path in sorted(inbox.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    (inbox / KEEP).touch()

    left = inbox_files(vault)
    if left:
        print(f"{INBOX}/ is not empty; still to file:")
        for path in left:
            print(f"  {path.relative_to(vault).as_posix()}")
        return 1
    print(f"{INBOX}/ is empty")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"list", "finish"}:
        print("usage: inbox.py {list,finish} [vault-root]", file=sys.stderr)
        return 2
    vault = Path(argv[2]).resolve() if len(argv) > 2 else Path.cwd()
    return cmd_list(vault) if argv[1] == "list" else cmd_finish(vault)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
