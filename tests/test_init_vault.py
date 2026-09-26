import importlib.util
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
