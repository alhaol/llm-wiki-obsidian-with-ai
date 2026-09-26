import importlib.util
import tempfile
import unittest

try:
    import tomllib  # Python 3.11+; the scripts themselves need only 3.9
except ImportError:
    tomllib = None
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("init_vault", ROOT / "scripts" / "init_vault.py")
init_vault = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(init_vault)

GUIDE = """# Guide

```
/NotAFolder
```

## Folder Hierarchy

```
/Daily
  └─ captures

/Areas
  /Areas/Work
  └─ projects

/../escape
/raw
```

## Tags

```
/Tags
```
"""


class GuideFoldersTest(unittest.TestCase):
    def test_reads_only_the_folder_hierarchy_block(self):
        self.assertEqual(
            init_vault.guide_folders(GUIDE), ["Daily", "Areas", "Areas/Work", "raw"]
        )

    def test_missing_section_yields_nothing(self):
        self.assertEqual(init_vault.guide_folders("# Guide\n\nNo folders here.\n"), [])

    def test_shipped_guide_lists_folders(self):
        text = (ROOT / init_vault.GUIDE_SOURCE).read_text(encoding="utf-8")
        folders = init_vault.guide_folders(text)
        self.assertIn("raw", folders)
        self.assertIn("wiki", folders)
        self.assertIn("Systems", folders)


class InstallGuideTest(unittest.TestCase):
    def test_copies_once_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            skill, vault = tmp / "skill", tmp / "vault"
            (skill / "guides").mkdir(parents=True)
            vault.mkdir()
            (skill / init_vault.GUIDE_SOURCE).write_text(GUIDE, encoding="utf-8")

            init_vault.install_guide(vault, skill, None)
            target = vault / init_vault.GUIDE_TARGET
            self.assertEqual(target.read_text(encoding="utf-8"), GUIDE)
            self.assertTrue((vault / "Areas" / "Work").is_dir())
            self.assertFalse((tmp / "escape").exists())

            # User edits the vault copy and adds a folder; a re-run keeps the
            # edit and creates the new folder.
            target.write_text(GUIDE.replace("/raw", "/raw\n/Inbox"), encoding="utf-8")
            init_vault.install_guide(vault, skill, None)
            self.assertIn("/Inbox", target.read_text(encoding="utf-8"))
            self.assertTrue((vault / "Inbox").is_dir())


class ShippedGuideTest(unittest.TestCase):
    def test_lists_the_inbox_and_assets(self):
        text = (ROOT / init_vault.GUIDE_SOURCE).read_text(encoding="utf-8")
        folders = init_vault.guide_folders(text)
        self.assertIn(init_vault.INBOX, folders)
        self.assertIn("assets", folders)


COMMAND = """---
description: Say "hi" to the wiki
---

Use the {{skill}} skill.

Source: $ARGUMENTS
"""


class RenderCommandTest(unittest.TestCase):
    def test_markdown_keeps_frontmatter_and_arguments(self):
        text = init_vault.render_command(COMMAND, "my-wiki", "md")
        self.assertTrue(text.startswith("---\ndescription:"))
        self.assertIn("Use the my-wiki skill.", text)
        self.assertIn("$ARGUMENTS", text)

    @unittest.skipIf(tomllib is None, "needs tomllib (Python 3.11+)")
    def test_toml_is_valid_and_uses_gemini_args(self):
        text = init_vault.render_command(COMMAND.replace("\n", "\r\n"), "my-wiki", "toml")
        data = tomllib.loads(text)
        self.assertEqual(data["description"], 'Say "hi" to the wiki')
        self.assertIn("Use the my-wiki skill.", data["prompt"])
        self.assertIn("Source: {{args}}", data["prompt"])
        self.assertNotIn("$ARGUMENTS", data["prompt"])

    @unittest.skipIf(tomllib is None, "needs tomllib (Python 3.11+)")
    def test_shipped_commands_render_for_every_agent(self):
        sources = sorted((ROOT / init_vault.COMMANDS_SOURCE).glob("*.md"))
        self.assertEqual([s.stem for s in sources], ["fetch", "ingest", "organize"])
        for source in sources:
            text = source.read_text(encoding="utf-8")
            self.assertIn("{{skill}}", text)
            self.assertIn("$ARGUMENTS", text)
            data = tomllib.loads(init_vault.render_command(text, "my-wiki", "toml"))
            self.assertTrue(data["description"])
            self.assertNotIn("{{skill}}", data["prompt"])


class InstallCommandsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.skill, self.vault = tmp / "my-wiki", tmp / "vault"
        (self.skill / "commands").mkdir(parents=True)
        self.vault.mkdir()
        self.source = self.skill / "commands" / "fetch.md"
        self.source.write_text(COMMAND, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def read(self, rel):
        return (self.vault / rel).read_text(encoding="utf-8")

    def test_every_agent_gets_every_command(self):
        steps = dict(init_vault.install_commands(self.vault, self.skill))
        self.assertEqual(set(steps), {f"{d}/" for d in init_vault.COMMAND_DIRS})
        for rel in [".claude/commands/fetch.md", ".opencode/commands/fetch.md",
                    ".pi/prompts/fetch.md", ".gemini/commands/fetch.toml"]:
            self.assertIn(init_vault.STAMP, self.read(rel))

        for rel in [".claude/commands/fetch.md", ".pi/prompts/fetch.md"]:
            text = self.read(rel)
            self.assertTrue(text.startswith("---\ndescription:"), rel)
            self.assertIn("Source: $ARGUMENTS", text)

        hermes = self.read(".hermes/skills/fetch/SKILL.md")
        self.assertTrue(hermes.startswith("---\nname: fetch\ndescription: "))
        self.assertIn("Use the my-wiki skill.", hermes)
        self.assertIn(f"Source: {init_vault.HERMES_ARGS}", hermes)
        self.assertNotIn("$ARGUMENTS", hermes)

    def test_rerun_refreshes_stamped_files_and_keeps_the_humans(self):
        init_vault.install_commands(self.vault, self.skill)
        mine = self.vault / ".claude" / "commands" / "fetch.md"
        mine.write_text("my own /fetch", encoding="utf-8")

        steps = dict(init_vault.install_commands(self.vault, self.skill))
        self.assertIn("up to date", steps[".opencode/commands/"])
        self.assertIn("left alone", steps[".claude/commands/"])

        self.source.write_text(COMMAND.replace("Use the", "Now use the"), encoding="utf-8")
        steps = dict(init_vault.install_commands(self.vault, self.skill))
        for agent_dir in [".opencode/commands/", ".gemini/commands/", ".pi/prompts/", ".hermes/skills/"]:
            self.assertIn("updated", steps[agent_dir])
        self.assertIn("Now use the my-wiki skill.", self.read(".hermes/skills/fetch/SKILL.md"))
        self.assertIn("Now use the my-wiki skill.", self.read(".pi/prompts/fetch.md"))
        self.assertEqual(mine.read_text(encoding="utf-8"), "my own /fetch")


class ExposeTest(unittest.TestCase):
    def test_stamped_copy_is_refreshed_and_links_report_in_sync(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp).resolve()
            skill = vault / ".claude" / "skills" / "my-wiki"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("v1", encoding="utf-8")

            copy = vault / ".agents" / "skills" / "my-wiki"
            init_vault.copy_skill(skill, copy)
            (skill / "SKILL.md").write_text("v2", encoding="utf-8")
            self.assertEqual(init_vault.expose_in(vault, skill, ".agents/skills"), "copy refreshed")
            self.assertEqual((copy / "SKILL.md").read_text(encoding="utf-8"), "v2")

            self.assertEqual(init_vault.expose_in(vault, skill, ".claude/skills"), "the install itself")

            other = vault / ".gemini" / "skills" / "my-wiki"
            other.mkdir(parents=True)
            self.assertIn("left alone", init_vault.expose_in(vault, skill, ".gemini/skills"))

            (vault / ".pi").mkdir()
            first = init_vault.expose_in(vault, skill, ".pi/skills")
            if not first.startswith("copied"):
                self.assertEqual(
                    init_vault.expose_in(vault, skill, ".pi/skills"), "linked (always in sync)"
                )


class RootFilesTest(unittest.TestCase):
    def test_seeds_once_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            files = init_vault.HUMAN_FILES + (init_vault.GUIDE_HTML,)
            (vault / "ME.md").write_text("mine", encoding="utf-8")

            steps = dict(init_vault.install_root_files(vault, ROOT, files))
            self.assertEqual(steps["HOME.md"], "created")
            self.assertEqual(steps["GUIDE.html"], "created")
            self.assertIn("left alone", steps["ME.md"])
            self.assertEqual((vault / "ME.md").read_text(encoding="utf-8"), "mine")
            self.assertIn("# HOME", (vault / "HOME.md").read_text(encoding="utf-8"))
            self.assertIn("File Naming", (vault / "GUIDE.html").read_text(encoding="utf-8"))

    def test_missing_source_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            steps = init_vault.install_root_files(vault, vault, init_vault.HUMAN_FILES)
            self.assertTrue(all(detail.startswith("skipped") for _, detail in steps))
            self.assertFalse((vault / "HOME.md").exists())


if __name__ == "__main__":
    unittest.main()
