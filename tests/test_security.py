import unittest
from scripts.validate import public_text_errors


class SecurityTests(unittest.TestCase):
    def test_private_path_styles(self):
        for path in ("C:" + "/" + "Users" + "/example/private",
                     "/" + "home" + "/example/private",
                     "/" + "Users" + "/example/private"):
            self.assertTrue(public_text_errors(path))

    def test_credential_families(self):
        for token in ("ghp_" + "x" * 36, "github_pat_" + "x" * 36,
                      "AKIA" + "X" * 16, "-----BEGIN " + "OPENSSH PRIVATE KEY-----"):
            self.assertTrue(public_text_errors(token))

    def test_regular_public_text(self):
        self.assertEqual([], public_text_errors("Accountable owner: project maintainer."))
