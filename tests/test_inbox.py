import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("inbox", ROOT / "scripts" / "inbox.py")
inbox = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inbox)


def run(*args: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = inbox.main(["inbox.py", *args])
    return code, out.getvalue()


class InboxTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name)
        self.inbox = self.vault / inbox.INBOX
        self.inbox.mkdir()
        (self.inbox / inbox.KEEP).touch()

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel: str, content: str | bytes) -> Path:
        path = self.vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def test_list_classifies_and_flags_duplicates(self):
        self.write("+/idea.md", "# An idea\n\nsome thought\n")
        self.write(
            "+/clips/post.md",
            "# Post\n\n> Source: https://example.com/post\n> Collected: 2026-09-26\n",
        )
        self.write("+/photo.png", b"\x89PNG fake")
        self.write("Concepts/old.md", "same bytes\n")
        self.write("+/old copy.md", "same bytes\n")
        self.write("+/.obsidian/workspace.json", "{}")

        code, out = run("list", str(self.vault))
        self.assertEqual(code, 0)
        rows = {line.split()[0]: line for line in out.splitlines() if line.startswith("+/")}
        self.assertIn("note", rows["+/idea.md"])
        self.assertIn("clip", rows["+/clips/post.md"])
        self.assertIn("asset", rows["+/photo.png"])
        self.assertIn("duplicate of Concepts/old.md", out)
        self.assertNotIn(".obsidian", out)
        self.assertNotIn(".gitkeep", out)
        self.assertIn("4 item(s)", out)

    def test_list_flags_duplicates_within_the_inbox(self):
        self.write("+/a.md", "twin\n")
        self.write("+/b.md", "twin\n")
        _, out = run("list", str(self.vault))
        self.assertIn("duplicate of +/a.md", out)
        self.assertIn("1 duplicate(s)", out)

    def test_list_empty_inbox(self):
        _, out = run("list", str(self.vault))
        self.assertIn("+/ is empty", out)

    def test_finish_prunes_empty_dirs_and_keeps_gitkeep(self):
        (self.inbox / "a" / "b").mkdir(parents=True)
        (self.inbox / inbox.KEEP).unlink()
        code, out = run("finish", str(self.vault))
        self.assertEqual(code, 0)
        self.assertIn("+/ is empty", out)
        self.assertFalse((self.inbox / "a").exists())
        self.assertTrue((self.inbox / inbox.KEEP).is_file())

    def test_finish_fails_while_files_remain(self):
        self.write("+/sub/left.md", "still here\n")
        code, out = run("finish", str(self.vault))
        self.assertEqual(code, 1)
        self.assertIn("+/sub/left.md", out)
        self.assertTrue((self.inbox / "sub").is_dir())


if __name__ == "__main__":
    unittest.main()
