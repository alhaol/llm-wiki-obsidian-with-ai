#!/usr/bin/env python3
"""One-screen health summary of the vault, with the next step for each finding.

Author: Ibrahim AbuAlhaol

Usage:
    python3 vault_status.py [vault-root]

Runs the skill's checks and condenses each to one line:

  inbox     +/ items waiting                        (inbox.py list)
  backlog   raw files not yet compiled              (check_evidence.py)
  evidence  fidelity suspects and evidence errors   (check_evidence.py)
  names     naming-convention violations            (check_names.py)
  guide     tag, facet, and folder violations       (check_guide.py)
  git       uncommitted changes                     (git status)

Each check's full output is one command away; the summary says which. Exits 1
when anything needs attention, 0 when the vault is clean.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def run(args: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8")
    return result.returncode, result.stdout + result.stderr


def script(name: str, *args: str) -> list[str]:
    return [sys.executable, str(SCRIPTS / name), *args]


def number(pattern: str, text: str) -> int:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else 0


def status(vault: Path) -> list[tuple[str, int, str, str]]:
    """Rows of (check, count needing attention, detail, next step)."""
    rows = []

    _, out = run(script("inbox.py", "list", str(vault)), vault)
    items = number(r"(\d+) item\(s\)", out)
    rows.append(("inbox", items, f"{items} item(s) in +/", "/organize"))

    if (vault / "wiki").is_dir():
        _, out = run(script("check_evidence.py", str(vault)), vault)
        suspects = number(r"(\d+) fidelity suspect", out)
        errors = number(r"(\d+) evidence error", out)
        backlog = number(r"(\d+) unreferenced raw", out)
        rows.append(("backlog", backlog, f"{backlog} raw file(s) not compiled", "/ingest"))
        rows.append(("evidence", suspects + errors,
                     f"{suspects} fidelity suspect(s), {errors} evidence error(s)",
                     "lint the wiki  (details: check_evidence.py)"))
    else:
        rows.append(("wiki", 0, "no wiki/ yet", "/ingest a first source"))

    _, out = run(script("check_names.py", str(vault)), vault)
    names = number(r"(\d+) naming violation", out)
    rows.append(("names", names, f"{names} naming violation(s)", "lint the wiki  (details: check_names.py)"))

    _, out = run(script("check_guide.py", str(vault)), vault)
    guide = number(r"(\d+) guide violation", out)
    detail = "no vault guide" if "no vault guide" in out else f"{guide} tag/folder violation(s)"
    rows.append(("guide", guide, detail, "lint the wiki  (details: check_guide.py)"))

    code, out = run(["git", "status", "--porcelain"], vault)
    if code == 0:
        changed = len([line for line in out.splitlines() if line.strip()])
        rows.append(("git", changed, f"{changed} uncommitted change(s)", "commit before /organize"))
    else:
        rows.append(("git", 0, "not a git repo", "git init (Hermes needs it)"))
    return rows


def main(argv: list[str]) -> int:
    vault = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    rows = status(vault)
    width = max(len(r[2]) for r in rows)
    print(f"Vault status: {vault}\n")
    for check, count, detail, step in rows:
        mark = "!!" if count else "ok"
        hint = f"  -> {step}" if count else ""
        print(f"  {mark}  {check:<9} {detail.ljust(width)}{hint}".rstrip())
    pending = sum(1 for r in rows if r[1])
    print(f"\n{'All clear.' if not pending else f'{pending} area(s) need attention.'}")
    return 1 if pending else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
