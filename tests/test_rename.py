import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("rename", ROOT / "scripts" / "rename.py")
rename = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rename)


class RenameTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text="x"):
        path = self.vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def read(self, rel):
        return (self.vault / rel).read_text(encoding="utf-8")

    def test_rewrites_markdown_links_and_wikilinks(self):
        self.write("Fleeting/Untitled 3.md", "# Idea\n")
        self.write("Daily/2026_09_26_standup_md.md",
                   "See [idea](../Fleeting/Untitled%203.md#plan) and [[Untitled 3|the idea]].\n"
                   "Also ![[Untitled 3]] and [[Fleeting/Untitled 3#h]] and "
                   "[x](<../Fleeting/Untitled 3.md> \"title\").\n"
                   "```\n[[Untitled 3]]\n```\n")
        self.write("wiki/index.md", "| [Idea](../Fleeting/Untitled%203.md) |\n")
        self.write(".obsidian/notes.md", "[[Untitled 3]]\n")

        rename.rename(self.vault, "Fleeting/Untitled 3.md", "Concepts/pricing_experiment_ideas_md.md")

        daily = self.read("Daily/2026_09_26_standup_md.md")
        self.assertIn("[idea](../Concepts/pricing_experiment_ideas_md.md#plan)", daily)
        self.assertIn("[[pricing_experiment_ideas_md|the idea]]", daily)
        self.assertIn("![[pricing_experiment_ideas_md]]", daily)
        self.assertIn("[[Concepts/pricing_experiment_ideas_md#h]]", daily)
        self.assertIn('[x](<../Concepts/pricing_experiment_ideas_md.md> "title")', daily)
        self.assertIn("```\n[[Untitled 3]]\n```", daily)  # code untouched
        self.assertIn("(../Concepts/pricing_experiment_ideas_md.md)", self.read("wiki/index.md"))
        self.assertEqual(self.read(".obsidian/notes.md"), "[[Untitled 3]]\n")
        self.assertFalse((self.vault / "Fleeting/Untitled 3.md").exists())
        self.assertTrue((self.vault / "Concepts/pricing_experiment_ideas_md.md").is_file())

    def test_moved_note_keeps_its_own_links_working(self):
        self.write("assets/garden_bed_layout_png.png")
        self.write("Concepts/other_note_md.md")
        self.write("+/note.md", "![bed](../assets/garden_bed_layout_png.png) "
                                "[o](../Concepts/other_note_md.md) [web](https://x.com/a.md) [s](#top)\n")
        rename.rename(self.vault, "+/note.md", "Areas/Day-Job/garden_plan_notes_md.md")
        moved = self.read("Areas/Day-Job/garden_plan_notes_md.md")
        self.assertIn("(../../assets/garden_bed_layout_png.png)", moved)
        self.assertIn("(../../Concepts/other_note_md.md)", moved)
        self.assertIn("(https://x.com/a.md)", moved)
        self.assertIn("(#top)", moved)

    def test_renames_assets_by_full_name(self):
        self.write("assets/IMG_2041.jpg")
        self.write("Concepts/garden_notes_md.md",
                   "![[IMG_2041.jpg]] ![p](../assets/IMG_2041.jpg) [[IMG_2041]]\n")
        rename.rename(self.vault, "assets/IMG_2041.jpg", "assets/garden_bed_layout_jpg.jpg")
        text = self.read("Concepts/garden_notes_md.md")
        self.assertIn("![[garden_bed_layout_jpg.jpg]]", text)
        self.assertIn("(../assets/garden_bed_layout_jpg.jpg)", text)

    def test_ambiguous_bare_wikilinks_are_reported_not_changed(self):
        self.write("Fleeting/plan.md")
        self.write("Archive/plan.md")
        self.write("Daily/2026_09_26_log_md.md", "[[plan]] and [[Fleeting/plan]]\n")
        report = rename.rename(self.vault, "Fleeting/plan.md", "Fleeting/launch_plan_md.md")
        text = self.read("Daily/2026_09_26_log_md.md")
        self.assertIn("[[plan]] and [[Fleeting/launch_plan_md]]", text)
        self.assertTrue(any("left unchanged" in line for line in report))

    def test_dry_run_and_refusals(self):
        self.write("Fleeting/a.md")
        self.write("Concepts/idea_notes_md.md", "[[a]]\n")
        report = rename.rename(self.vault, "Fleeting/a.md", "Fleeting/b_c_md.md", dry_run=True)
        self.assertTrue(report[0].startswith("would move"))
        self.assertTrue((self.vault / "Fleeting/a.md").is_file())
        self.assertEqual(self.read("Concepts/idea_notes_md.md"), "[[a]]\n")

        with self.assertRaises(rename.RenameError):
            rename.rename(self.vault, "Fleeting/a.md", "Concepts/idea_notes_md.md")
        with self.assertRaises(rename.RenameError):
            rename.rename(self.vault, "Fleeting/missing.md", "Fleeting/x_y_md.md")
        with self.assertRaises(rename.RenameError):
            rename.rename(self.vault, "Fleeting/a.md", "../outside.md")


if __name__ == "__main__":
    unittest.main()
