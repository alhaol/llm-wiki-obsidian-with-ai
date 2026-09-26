import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("check_guide", ROOT / "scripts" / "check_guide.py")
check_guide = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_guide  # dataclasses look the module up by name
SPEC.loader.exec_module(check_guide)

SHIPPED = (ROOT / "guides" / "guide.md").read_text(encoding="utf-8")
GOOD = "tags: [afpish/professional, status/progress, urgency/medium, time/ongoing]"


class CharterTest(unittest.TestCase):
    def test_reads_values_counts_and_folders_from_the_shipped_guide(self):
        charter = check_guide.read_charter(SHIPPED)
        self.assertIn("afpish/professional", charter.values)
        self.assertIn("type/paper", charter.values)
        self.assertNotIn("people/<name>", charter.values)
        self.assertEqual(charter.counts["afpish"], (1, 3))
        self.assertEqual(charter.counts["status"], (1, 1))
        self.assertEqual(charter.counts["urgency"], (1, 1))
        self.assertEqual(charter.counts["time"], (1, 1))
        self.assertEqual(charter.counts["type"], (0, None))
        self.assertEqual(charter.counts["places"], (0, None))
        for folder in ["+", "Daily", "Areas/Day-Job", "Concepts", "assets", "Systems"]:
            self.assertIn(folder, charter.folders)


class VaultTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name)
        self.write("Systems/vault-guide.md", SHIPPED)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = self.vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def read(self, rel):
        return (self.vault / rel).read_text(encoding="utf-8")

    def run_main(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check_guide.main(["check_guide.py", str(self.vault), *args])
        return code, out.getvalue()

    def test_compliant_vault_passes(self):
        self.write("Concepts/second_order_thinking_md.md", f"---\n{GOOD}\n---\n# Idea\n")
        self.write("wiki/ml/transformer_architecture_md.md",
                   "---\ntags:\n  - afpish/professional\n  - afpish/independence\n"
                   "  - status/complete\n  - urgency/low\n  - time/2027\n  - type/paper\n---\n# T\n")
        self.write("raw/ml/2026-01-01-paper.md", "# Paper\n\n> Source: x\n\nIssue \\#42 and `#code`\n")
        self.write("assets/garden_bed_layout_png.png", "png")
        self.write("HOME.md", "#whatever\n")
        self.write("+/Untitled.md", "#anything\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)
        self.assertIn("4 file(s) checked, 0 guide violation(s)", out)

    def test_reports_tags_counts_raw_and_folders(self):
        self.write("Concepts/idea_notes_md.md",
                   "---\ntags: [Status/Progress, work, afpish/professional, afpish/family,"
                   " afpish/health, afpish/social]\n---\nSee #project-x here.\n")
        self.write("raw/ml/2026-01-01-paper.md", "---\ntags: [ml]\n---\n# P\n\nSee #ml\n")
        self.write("Projects/plan_notes_md.md", f"---\n{GOOD}\n---\n")
        self.write("loose_note_md.md", f"---\n{GOOD}\n---\n")
        self.write("wiki/deep/er/thing_notes_md.md", f"---\n{GOOD}\n---\n")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        for expected in [
            "Concepts/idea_notes_md.md: unknown tag: Status/Progress",
            "Concepts/idea_notes_md.md: unknown tag: work",
            "Concepts/idea_notes_md.md: unknown tag: project-x",
            "facet count: afpish has 4, needs 1-3",
            "facet count: status has 0, needs 1",
            "raw/ml/2026-01-01-paper.md: raw tag: ml",
            "folder Projects/ is not in the guide",
            "loose file at the vault root",
            "wiki/ files go exactly one level down",
        ]:
            self.assertIn(expected, out)

    def test_ignores_code_headings_links_and_numbers(self):
        self.write("Concepts/idea_notes_md.md",
                   f"---\n{GOOD}\n---\n# Heading\n\nIssue #42, [jump](#section), "
                   "https://x.com/#frag, `#inline`\n\n```\n#fenced\n```\n")
        code, out = self.run_main()
        self.assertEqual(code, 0, out)

    def test_strip_clears_only_non_compliant_tags(self):
        self.write("Concepts/idea_notes_md.md",
                   "---\ntitle: Idea\ntags: [work, afpish/professional, status/progress,"
                   " urgency/medium, time/ongoing]\n---\n"
                   "Tags: #todo #afpish/professional #misc\n\nWe ship #project-x soon.\n")
        self.write("Daily/2026_09_26_standup_md.md", "---\ntags: [random]\n---\nBody\n")
        self.write("raw/ml/2026-01-01-paper.md", "---\ntags: [ml]\nurl: x\n---\n# P\n\nSee #ml and #ai\n")

        self.run_main("--strip")

        idea = self.read("Concepts/idea_notes_md.md")
        self.assertIn("title: Idea", idea)
        self.assertIn("tags: [afpish/professional, status/progress, urgency/medium, time/ongoing]", idea)
        self.assertIn("Tags: #afpish/professional\n", idea)
        self.assertIn("We ship project-x soon.", idea)
        self.assertNotIn("#todo", idea)

        daily = self.read("Daily/2026_09_26_standup_md.md")
        self.assertEqual(daily, "Body\n")

        raw = self.read("raw/ml/2026-01-01-paper.md")
        self.assertEqual(raw, "---\nurl: x\n---\n# P\n\nSee \\#ml and \\#ai\n")

        # Strip never adds tags, so the daily note still lacks its facets.
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertNotIn("unknown tag", out)
        self.assertNotIn("raw tag", out)
        self.assertIn("Daily/2026_09_26_standup_md.md: facet count: status has 0", out)

    def test_removes_an_emptied_tags_line(self):
        self.write("Concepts/idea_notes_md.md", f"---\n{GOOD}\n---\nTags: #todo #misc\nText\n")
        self.run_main("--strip")
        self.assertEqual(self.read("Concepts/idea_notes_md.md"), f"---\n{GOOD}\n---\nText\n")

    def test_no_guide_is_not_an_error(self):
        (self.vault / "Systems/vault-guide.md").unlink()
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("no vault guide", out)


if __name__ == "__main__":
    unittest.main()
