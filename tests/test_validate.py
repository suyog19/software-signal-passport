"""Negative cases protect the checker against misleading success."""
import tempfile
import unittest
from pathlib import Path

from scripts.validate import anchors, link_errors, public_text_errors, required_errors, validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "README.md"
        self.source.write_text("# Start\n", encoding="utf-8")

    def test_existing_link_and_heading(self):
        self.assertEqual([], link_errors(self.root, self.source, "[start](README.md#start)"))

    def test_missing_file(self):
        self.assertIn("missing link", link_errors(self.root, self.source, "[x](missing.md)")[0])

    def test_missing_heading(self):
        self.assertIn("missing heading", link_errors(self.root, self.source, "[x](README.md#absent)")[0])

    def test_duplicate_heading(self):
        self.assertEqual({"same", "same-1"}, anchors("# Same\n## Same\n"))

    def test_encoded_filename(self):
        (self.root / "two words.md").write_text("# Fine\n", encoding="utf-8")
        self.assertEqual([], link_errors(self.root, self.source, "[x](two%20words.md#fine)"))

    def test_parent_escape_rejected(self):
        self.assertIn("escapes", link_errors(self.root, self.source, "[x](../private.md)")[0])

    def test_remote_link_not_claimed_checked(self):
        self.assertEqual([], link_errors(self.root, self.source, "[x](https://example.invalid/missing)"))

    def test_versioned_copy_link_checked_locally(self):
        self.assertIn("missing link", link_errors(
            self.root, self.source,
            "[x](https://github.com/suyog19/software-signal-passport/blob/v0.1.0/missing.md)")[0])

    def test_code_and_comment_placeholders_ignored(self):
        sample = "<!-- [x](absent.md) -->\n```md\n[x](absent.md)\n```\n"
        self.assertEqual([], link_errors(self.root, self.source, sample))

    def test_required_file_missing_empty_and_escape(self):
        (self.root / "empty").touch()
        self.assertEqual(3, len(required_errors(self.root, ["missing", "empty", "../outside"])))

    def test_empty_manifest(self):
        self.assertEqual(["distribution manifest is empty"], required_errors(self.root, []))

    def test_private_path_detected(self):
        self.assertTrue(public_text_errors("C:" + "/" + "Users" + "/" + "example" + "/private.md"))

    def test_fake_credential_detected_without_real_secret(self):
        self.assertTrue(public_text_errors("ghp_" + "x" * 36))
        self.assertTrue(public_text_errors("-----BEGIN " + "PRIVATE KEY-----"))

    def test_ordinary_public_text(self):
        self.assertEqual([], public_text_errors("Use accountable ownership and unknown evidence."))

    def test_missing_manifest_fails(self):
        self.assertEqual(["missing distributable-files.txt"], validate(self.root))

    def test_bad_version_fails(self):
        (self.root / "distributable-files.txt").write_text("README.md\nVERSION\n")
        (self.root / "VERSION").write_text("9.9.9\n")
        self.assertIn("VERSION must match the v0.1.0 distribution", validate(self.root))

    def test_unsupported_file_protocol(self):
        self.assertIn("unsupported", link_errors(self.root, self.source, "[x](file:///tmp/private)")[0])


if __name__ == "__main__":
    unittest.main()
