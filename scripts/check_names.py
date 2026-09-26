#!/usr/bin/env python3
"""Check vault file names against the naming convention.

Author: Ibrahim AbuAlhaol

Usage:
    python3 check_names.py [vault-root] [path ...]

Every file outside raw/ and +/ is named

    {word}_{word}[_{word}[_{word}[_{word}]]]_{identifier}.{extension}

with two to five lowercase words (a-z, 0-9) describing the content, then an
identifier naming the file's type. The identifier is the extension itself
(`_md.md`, `_png.png`, `_pdf.pdf`), except for Excalidraw drawings, which use
`excali` (`login_flow_sketch_excali.excalidraw.md`).

Exempt: raw/ and +/ (sources keep their fetched names; the inbox is transient),
dot-paths (Obsidian and the agents' own directories), and the vault's fixed
files: HOME.md, ME.md, GUIDE.html, Systems/vault-guide.md, wiki/index.md and
wiki/log.md.

With paths (vault-relative), only those files are checked. Prints one line per
violation and exits 1 if there are any. The vault root defaults to the current
working directory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EXEMPT_DIRS = {"raw", "+"}
FIXED_FILES = {
    "HOME.md",
    "ME.md",
    "GUIDE.html",
    "Systems/vault-guide.md",
    "wiki/index.md",
    "wiki/log.md",
}

# Compound extensions whose identifier is not simply the last suffix. Longest
# first, so ".excalidraw.md" wins over ".md".
SPECIAL = ((".excalidraw.md", "excali"), (".excalidraw", "excali"))

WORD_RE = re.compile(r"^[a-z0-9]+$")
MIN_WORDS, MAX_WORDS = 2, 5


def split_name(name: str) -> tuple[str, str, str] | None:
    """Return (stem, extension, expected identifier), or None without an extension."""
    lower = name.lower()
    for ext, ident in SPECIAL:
        if lower.endswith(ext) and len(name) > len(ext):
            return name[: -len(ext)], name[-len(ext) :], ident
    if "." not in name.strip("."):
        return None
    stem, ext = name.rsplit(".", 1)
    return stem, "." + ext, ext.lower()


def problem(name: str) -> str | None:
    """Why `name` breaks the convention, or None when it follows it."""
    parts = split_name(name)
    if parts is None:
        return "no extension"
    stem, ext, ident = parts
    if ext != ext.lower():
        return f"extension {ext} is not lowercase"
    segments = stem.split("_")
    if len(segments) < 2:
        return f"missing _{ident} identifier"
    *words, found = segments
    if found != ident:
        return f"identifier is {found!r}, expected {ident!r}"
    bad = [w for w in words if not WORD_RE.match(w)]
    if bad:
        return f"words must be lowercase a-z/0-9: {', '.join(repr(w) for w in bad)}"
    if not MIN_WORDS <= len(words) <= MAX_WORDS:
        return f"{len(words)} word(s), expected {MIN_WORDS} to {MAX_WORDS}"
    return None


def exempt(rel: Path) -> bool:
    if any(part.startswith(".") for part in rel.parts):
        return True
    if rel.parts[0] in EXEMPT_DIRS:
        return True
    return rel.as_posix() in FIXED_FILES


def vault_files(vault: Path) -> list[Path]:
    return sorted(
        p.relative_to(vault)
        for p in vault.rglob("*")
        if p.is_file() and not exempt(p.relative_to(vault))
    )


def main(argv: list[str]) -> int:
    vault = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    if len(argv) > 2:
        files = [Path(a) for a in argv[2:] if not exempt(Path(a))]
    else:
        files = vault_files(vault)

    violations = [(f, why) for f in files if (why := problem(f.name))]
    for rel, why in violations:
        print(f"{rel.as_posix()}: {why}")
    print(f"\n{len(files)} file(s) checked, {len(violations)} naming violation(s)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
