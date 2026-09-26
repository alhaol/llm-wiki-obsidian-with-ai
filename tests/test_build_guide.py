import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("build_guide", ROOT / "scripts" / "build_guide.py")
build_guide = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_guide)


class RenderTest(unittest.TestCase):
    def test_blocks_and_inline(self):
        page = build_guide.render(
            "# Title\n\n**Version:** 1.3  \n**Updated:** today\n\n"
            "## Section One\n\nA *soft* **bold** `a<b` [link](#section-one) that\nwraps **across\nlines**.\n\n"
            "> Quote with `code`\n\n"
            "1. First\n   - Nested **item**\n2. Second\n\n"
            "| A | B |\n|---|---|\n| `x` | y |\n\n"
            "```\n#not/a/heading <tag>\n```\n\n---\n\n## Section One\n",
            stamp="made by test",
        )
        self.assertIn("<title>Title</title>", page)
        self.assertIn("<strong>Version:</strong> 1.3<br><strong>Updated:</strong>", page)
        self.assertIn('<h2 id="section-one">', page)
        self.assertIn('<h2 id="section-one-1">', page)
        self.assertIn("<em>soft</em>", page)
        self.assertIn("<code>a&lt;b</code>", page)
        self.assertIn('<a href="#section-one">link</a>', page)
        self.assertIn("<strong>across lines</strong>", page)
        self.assertIn("<blockquote><p>Quote with <code>code</code></p></blockquote>", page)
        self.assertIn("<ol><li>First<ul><li>Nested <strong>item</strong></li></ul></li><li>Second</li></ol>", page)
        self.assertIn("<th>A</th>", page)
        self.assertIn("<td><code>x</code></td>", page)
        self.assertIn("<pre><code>#not/a/heading &lt;tag&gt;</code></pre>", page)
        self.assertIn("<hr>", page)
        self.assertIn("<!-- made by test -->", page)
        self.assertIn('<nav><p>Contents</p><a href="#section-one">', page)

    def test_callouts_render_as_cards(self):
        page = build_guide.render(
            "# T\n\n> [!important] Remember **this**\n> Body text.\n\n"
            "> [!tip]- Folded\n> Hidden.\n\n> [!summary]+\n> Open.\n\n> Plain quote.\n"
        )
        self.assertIn('<div class="callout" data-callout="important">'
                      '<p class="callout-title">Remember <strong>this</strong></p><p>Body text.</p></div>', page)
        self.assertIn('<details class="callout" data-callout="tip"><summary class="callout-title">Folded</summary>', page)
        self.assertIn('<details class="callout" data-callout="summary" open><summary class="callout-title">Summary</summary>', page)
        self.assertIn("<blockquote><p>Plain quote.</p></blockquote>", page)

    def test_shipped_html_is_built_from_the_shipped_guide(self):
        source = (ROOT / "guides" / "guide.md").read_text(encoding="utf-8")
        expected = build_guide.render(source, build_guide.REPO_STAMP)
        # A Windows checkout may convert the file to CRLF; compare content only.
        actual = (ROOT / "guides" / "guide.html").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(
            actual, expected, "guides/guide.html is stale: run python scripts/build_guide.py"
        )


if __name__ == "__main__":
    unittest.main()
