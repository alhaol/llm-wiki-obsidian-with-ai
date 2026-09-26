import contextlib
import importlib.util
import io
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("check_names", ROOT / "scripts" / "check_names.py")
check_names = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_names)


class ProblemTest(unittest.TestCase):
    def test_valid_names(self):
        for name in [
            "second_order_thinking_md.md",
            "transformer_architecture_md.md",
            "2026_09_26_standup_md.md",
            "a_b_c_d_e_md.md",
            "garden_bed_layout_png.png",
            "attention_paper_original_pdf.pdf",
            "login_flow_sketch_excali.excalidraw.md",
            "login_flow_excali.excalidraw",
            "side_business_roadmap_canvas.canvas",
        ]:
            with self.subTest(name=name):
                self.assertIsNone(check_names.problem(name))

    def test_invalid_names(self):
        cases = {
            "Untitled 3.md": "identifier",
            "claude-code-statusline.md": "identifier",
            "thinking_md.md": "1 word(s)",
            "a_b_c_d_e_f_md.md": "6 word(s)",
            "Second_Order_md.md": "lowercase",
            "garden_bed_png.jpg": "expected 'jpg'",
            "login_flow_md.excalidraw.md": "expected 'excali'",
            "garden_bed_png.PNG": "extension",
            "README": "no extension",
        }
        for name, reason in cases.items():
            with self.subTest(name=name):
                self.assertIn(reason, check_names.problem(name) or "")


class ExemptTest(unittest.TestCase):
    def test_scope(self):
        for rel in ["raw/ml/2026-01-01-paper.md", "+/Untitled.md", ".obsidian/app.json",
                    "HOME.md", "ME.md", "GUIDE.html", "wiki/index.md", "wiki/log.md",
                    "Systems/vault-guide.md", "Daily/.gitkeep"]:
            with self.subTest(rel=rel):
                self.assertTrue(check_names.exempt(Path(rel)))
        for rel in ["wiki/ml/attention.md", "Concepts/Idea.md", "Systems/moc.md", "notes.md"]:
            with self.subTest(rel=rel):
                self.assertFalse(check_names.exempt(Path(rel)))


class MainTest(unittest.TestCase):
    def run_main(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check_names.main(["check_names.py", *args])
        return code, out.getvalue()

    def test_reports_only_non_exempt_violations(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for rel in ["wiki/ml/attention_heads_md.md", "wiki/ml/Bad Name.md",
                        "raw/ml/2026-01-01-paper.md", "+/whatever.md", "HOME.md",
                        "wiki/index.md", "assets/IMG_2041.jpg"]:
                (vault / rel).parent.mkdir(parents=True, exist_ok=True)
                (vault / rel).write_text("x", encoding="utf-8")

            code, out = self.run_main(str(vault))
            self.assertEqual(code, 1)
            self.assertIn("wiki/ml/Bad Name.md", out)
            self.assertIn("assets/IMG_2041.jpg", out)
            self.assertNotIn("attention_heads", out)
            self.assertIn("3 file(s) checked, 2 naming violation(s)", out)

            code, out = self.run_main(str(vault), "wiki/ml/attention_heads_md.md", "raw/x.md")
            self.assertEqual(code, 0)
            self.assertIn("1 file(s) checked, 0 naming violation(s)", out)


class ShippedDocsTest(unittest.TestCase):
    def test_every_example_name_in_the_guides_is_valid(self):
        name_re = re.compile(r"[a-z0-9_]+_[a-z0-9]+(?:\.excalidraw)?\.[a-z]+")
        for doc in ["guides/guide.md", "guides/guide.html", "SKILL.md"]:
            text = (ROOT / doc).read_text(encoding="utf-8")
            names = set(re.findall(r"(?:`|<code>|/)(" + name_re.pattern + r")(?=`|</code>)", text))
            self.assertTrue(names, doc)
            for name in (n for n in names if not n.endswith(".py")):
                with self.subTest(doc=doc, name=name):
                    self.assertIsNone(check_names.problem(name))


if __name__ == "__main__":
    unittest.main()
