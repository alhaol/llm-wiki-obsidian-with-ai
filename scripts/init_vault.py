#!/usr/bin/env python3
"""Bootstrap an Obsidian vault as an LLM-wiki workspace.

Author: Ibrahim AbuAlhaol

Run this straight after cloning the skill into your vault's agent directory:

    mkdir -p ~/brain && cd ~/brain
    git init
    git clone <repo> .claude/skills/my-llm-wiki
    python .claude/skills/my-llm-wiki/scripts/init_vault.py

It infers the vault root from its own location, so it normally needs no
arguments. What it does:

  * verifies the vault is a git repo (Hermes needs .git to find project skills)
  * renames the skill in SKILL.md frontmatter to match its directory
  * creates raw/ and wiki/
  * copies guides/guide.md into the vault as Systems/vault-guide.md and creates
    the folders it lists (edit the guide *before* running this)
  * exposes the skill to Hermes via .agents/skills/ (symlink, junction, or copy)
  * writes a .gitignore that keeps Obsidian's churn out of history
  * prints the remaining manual steps

Apart from the folders and the vault guide, everything it creates lives in
dot-directories, which Obsidian does not index.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Agent directories that can hold a project-local skill, and which agents read
# them. Sourced from each tool's docs; see README.md for links.
AGENT_DIRS = {
    ".agents/skills": ("OpenCode", "Hermes"),
    ".claude/skills": ("Claude Code", "OpenCode"),
    ".gemini/skills": ("Gemini CLI",),
    ".hermes/skills": ("Hermes",),
    ".opencode/skills": ("OpenCode",),
}

# Between them these three cover every supported agent, so the bootstrapper makes
# the skill reachable from all of them no matter which one you cloned into.
EXPOSE_DIRS = (".agents/skills", ".claude/skills", ".gemini/skills")

# Where the vault guide ships inside the skill, and where it lands in the vault.
# The vault copy is visible in Obsidian on purpose: the human reads it too.
GUIDE_SOURCE = Path("guides/guide.md")
GUIDE_TARGET = Path("Systems/vault-guide.md")

# A folder line in the guide's "Folder Hierarchy" block, e.g. "  /Areas/Day-Job".
FOLDER_LINE_RE = re.compile(r"^\s*/([^\s/][^\s]*?)/?\s*$")

# OpenCode enforces this on the frontmatter name, and requires it to match the
# skill's directory name.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

GITIGNORE = """\
# Obsidian: per-machine UI state, not knowledge. Keep the rest of .obsidian/
# (your plugins and settings) versioned.
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache

# OS noise
.DS_Store
Thumbs.db

# Python bytecode from the skill's scripts
__pycache__/
*.pyc
"""


class Abort(Exception):
    pass


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)


def find_skill_root(start: Path) -> Path:
    """Walk up from this file to the directory containing SKILL.md."""
    for candidate in [start, *start.parents]:
        if (candidate / "SKILL.md").is_file():
            return candidate
    raise Abort(f"No SKILL.md found at or above {start}")


def find_vault_root(skill_root: Path) -> tuple[Path, str]:
    """Infer the vault from a skill living in <vault>/<agent-dir>/<name>."""
    for agent_dir in AGENT_DIRS:
        depth = len(Path(agent_dir).parts)  # e.g. ".claude/skills" -> 2
        try:
            vault = skill_root.parents[depth]
        except IndexError:
            continue
        if skill_root.parent == vault / agent_dir:
            return vault, agent_dir
    raise Abort(
        f"{skill_root} is not inside a recognized agent directory.\n"
        f"Expected <vault>/<{'|'.join(AGENT_DIRS)}>/<skill-name>.\n"
        "Move the clone there, or pass --vault to override."
    )


def ensure_git(vault: Path, do_init: bool) -> str:
    if (vault / ".git").exists():
        return "already a git repo"
    if not do_init:
        raise Abort(
            f"{vault} is not a git repo.\n"
            "Hermes locates project skills by finding the nearest ancestor with "
            ".git, so without it Hermes will not see this skill.\n"
            "Run `git init` there yourself, or drop --no-git-init and this "
            "script will do it."
        )
    result = run(["git", "init"], vault)
    if result.returncode != 0:
        raise Abort(f"git init failed: {result.stderr.strip()}")
    return "initialized"


def rename_skill(skill_root: Path) -> str:
    """Make the frontmatter name match the directory name."""
    dir_name = skill_root.name
    if not NAME_RE.match(dir_name) or len(dir_name) > 64:
        raise Abort(
            f"Directory name {dir_name!r} is not a valid skill name.\n"
            "Use lowercase letters, digits and single hyphens (max 64 chars), "
            "e.g. ibrahim-llm-wiki."
        )

    skill_md = skill_root / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    match = re.search(r"^name:[ \t]*(.+?)[ \t]*$", text, re.MULTILINE)
    if not match:
        raise Abort(f"No `name:` field in {skill_md}")

    current = match.group(1).strip()
    if current == dir_name:
        return f"already {dir_name}"

    text = text[: match.start()] + f"name: {dir_name}" + text[match.end() :]

    # Keep the skill discoverable under its new name by adding it as a trigger.
    desc = re.search(r'^description:[ \t]*"(.*)"[ \t]*$', text, re.MULTILINE)
    if desc and dir_name not in desc.group(1):
        body = desc.group(1).rstrip()
        body = body[:-1] if body.endswith(".") else body
        text = (
            text[: desc.start()]
            + f'description: "{body}, or \'{dir_name}\'."'
            + text[desc.end() :]
        )

    skill_md.write_text(text, encoding="utf-8")
    return f"{current} -> {dir_name}"


def guide_folders(text: str) -> list[str]:
    """Folder paths listed in the first code block under "## Folder Hierarchy"."""
    section = re.search(
        r"^##\s+Folder Hierarchy\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S
    )
    if not section:
        return []
    block = re.search(r"^```[^\n]*\n(.*?)^```", section.group(1), re.M | re.S)
    if not block:
        return []
    folders = []
    for line in block.group(1).splitlines():
        match = FOLDER_LINE_RE.match(line)
        if match and ".." not in match.group(1).split("/"):
            folders.append(match.group(1))
    return folders


def install_guide(vault: Path, skill_root: Path, source: Path | None) -> list[tuple[str, str]]:
    """Copy the vault guide in (never overwriting) and create its folders.

    Folders come from the vault copy when it already exists, so re-running
    after editing the guide in Obsidian picks up new folders.
    """
    steps: list[tuple[str, str]] = []
    target = vault / GUIDE_TARGET
    label = str(GUIDE_TARGET).replace(os.sep, "/")

    if target.is_file():
        steps.append((label, "left alone (already exists; folders read from it)"))
    else:
        source = source or skill_root / GUIDE_SOURCE
        if not source.is_file():
            steps.append((label, f"skipped (no guide at {source})"))
            return steps
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        steps.append((label, "created"))

    created = []
    for folder in guide_folders(target.read_text(encoding="utf-8")):
        path = vault / folder
        if not path.is_dir():
            path.mkdir(parents=True)
            created.append(folder)
    steps.append(
        ("guide folders", ", ".join(f"{f}/" for f in created) if created else "all present")
    )
    return steps


def expose_in(vault: Path, skill_root: Path, agent_dir: str) -> str:
    """Make the skill reachable from <vault>/<agent_dir>/<name>.

    Prefers a symlink, falls back to a Windows junction, and copies only as a
    last resort. Returns a human-readable description of what it did.
    """
    target = vault / Path(agent_dir) / skill_root.name

    if target.resolve() == skill_root.resolve():
        return "the install itself"
    if target.exists() or target.is_symlink():
        return "already present"

    target.parent.mkdir(parents=True, exist_ok=True)
    relative = os.path.relpath(skill_root, target.parent)

    try:
        os.symlink(relative, target, target_is_directory=True)
        return f"symlink -> {relative}"
    except (OSError, NotImplementedError):
        pass

    if os.name == "nt":
        # Junctions need no admin rights or Developer Mode, unlike symlinks.
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(skill_root)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return f"junction -> {relative}"

    shutil.copytree(skill_root, target)
    return "copied (no link support; re-run this script after editing SKILL.md)"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap an Obsidian vault as an LLM-wiki workspace."
    )
    parser.add_argument(
        "--vault",
        type=Path,
        help="Vault root. Inferred from this script's location by default.",
    )
    parser.add_argument(
        "--no-git-init",
        dest="git_init",
        action="store_false",
        help="Fail instead of running `git init` when the vault is not a repo.",
    )
    parser.add_argument(
        "--no-link",
        dest="link",
        action="store_false",
        help=(
            "Install only where the skill was cloned, instead of exposing it "
            "from both .agents/skills/ and .claude/skills/."
        ),
    )
    parser.add_argument(
        "--guide",
        type=Path,
        help=f"Vault guide to install. Defaults to {GUIDE_SOURCE} in the skill.",
    )
    parser.add_argument(
        "--no-guide",
        dest="install_guide",
        action="store_false",
        help=f"Do not install {GUIDE_TARGET} or create the folders it lists.",
    )
    args = parser.parse_args()

    try:
        skill_root = find_skill_root(Path(__file__).resolve().parent)

        if args.vault:
            vault = args.vault.resolve()
            installed_in = (
                str(skill_root.parent.relative_to(vault)).replace(os.sep, "/")
                if skill_root.is_relative_to(vault)
                else "(outside vault)"
            )
        else:
            vault, installed_in = find_vault_root(skill_root)

        steps: list[tuple[str, str]] = []
        steps.append(("vault", str(vault)))
        steps.append(("skill", f"{installed_in}/{skill_root.name}"))
        steps.append(("git", ensure_git(vault, args.git_init)))
        steps.append(("skill name", rename_skill(skill_root)))

        for name in ("raw", "wiki"):
            path = vault / name
            existed = path.is_dir()
            path.mkdir(exist_ok=True)
            steps.append((f"{name}/", "already existed" if existed else "created"))

        if args.link:
            for agent_dir in EXPOSE_DIRS:
                agents = ", ".join(AGENT_DIRS[agent_dir])
                steps.append(
                    (
                        f"{agent_dir}/",
                        f"{expose_in(vault, skill_root, agent_dir)}  [{agents}]",
                    )
                )

        if args.install_guide:
            steps.extend(install_guide(vault, skill_root, args.guide))

        gitignore = vault / ".gitignore"
        if gitignore.exists():
            steps.append((".gitignore", "left alone (already exists)"))
        else:
            gitignore.write_text(GITIGNORE, encoding="utf-8")
            steps.append((".gitignore", "created"))

    except Abort as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    width = max(len(label) for label, _ in steps)
    print("\nVault bootstrapped\n")
    for label, detail in steps:
        print(f"  {label.ljust(width)}  {detail}")

    print(
        f"""
Next steps

  1. Obsidian: "Open folder as vault" and select
     {vault}

  2. Start your agent from the vault root -- the skill resolves raw/ and wiki/
     relative to the working directory, so always launch from there:

       cd {vault}
       claude            # or: gemini, opencode
       hermes skills trust    # Hermes only, once per vault

  3. Ask it to ingest something:

       "add https://example.com/post to the wiki"

  4. Read {GUIDE_TARGET.as_posix()} in Obsidian. It is the folder and tag
     charter both you and the agent follow -- edit it there as your vault grows.

Customization goes in {installed_in}/{skill_root.name}/SKILL.md so your rules
travel with the skill. See references/obsidian-conventions.md for the
Obsidian-specific conventions worth adding.
"""
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
