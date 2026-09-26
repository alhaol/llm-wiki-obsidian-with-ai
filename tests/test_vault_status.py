import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("vault_status", ROOT / "scripts" / "vault_status.py")
vault_status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vault_status)


class VaultStatusTest(unittest.TestCase):
    def test_summarizes_every_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            guide = (ROOT / "guides" / "guide.md").read_text(encoding="utf-8")
            files = {
                "Systems/vault-guide.md": guide,
                "+/old note.md": "thought\n",
                "wiki/index.md": "# Knowledge Base Index\n",
                "wiki/log.md": "# Wiki Log\n",
                "raw/ml/2026-01-01-paper.md": "# Paper\n\n> Source: x\n\nBody\n",
                "Concepts/Bad Name.md": "---\ntags: [work]\n---\n",
            }
            for rel, text in files.items():
                (vault / rel).parent.mkdir(parents=True, exist_ok=True)
                (vault / rel).write_text(text, encoding="utf-8")

            rows = {check: (count, step) for check, count, _, step in vault_status.status(vault)}
            self.assertEqual(rows["inbox"], (1, "/organize"))
            self.assertEqual(rows["backlog"][0], 1)
            self.assertEqual(rows["evidence"][0], 0)
            self.assertEqual(rows["names"][0], 1)
            self.assertGreater(rows["guide"][0], 0)
            self.assertIn("git", rows)

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = vault_status.main(["vault_status.py", str(vault)])
            self.assertEqual(code, 1)
            self.assertIn("-> /organize", out.getvalue())
            self.assertIn("-> /ingest", out.getvalue())


if __name__ == "__main__":
    unittest.main()
