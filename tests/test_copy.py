import tempfile
import unittest
from pathlib import Path

from scripts.validate import VERSIONED, copy_errors


class CopyTests(unittest.TestCase):
    def test_comment_links_checked_before_publishing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = "<!-- Guide: " + VERSIONED + "docs/guide.md -->"
            self.assertTrue(copy_errors(root, sample))
            (root / "docs").mkdir()
            (root / "docs/guide.md").write_text("# Guide\n")
            self.assertEqual([], copy_errors(root, sample))

    def test_all_distributed_copy_links_resolve_to_bundle(self):
        root = Path(__file__).resolve().parents[1]
        for name in ("github-pr-passport.md", "software-signal-passport.md"):
            text = (root / "templates" / name).read_text(encoding="utf-8")
            self.assertEqual([], copy_errors(root, text))

    def test_copy_target_cannot_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(copy_errors(Path(directory), VERSIONED + "../outside.md"))
