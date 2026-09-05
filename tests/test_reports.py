import io
import json
import unittest
import zipfile
from urllib.error import HTTPError
from passport.reports import summarize
from passport.github import GitHub
from passport.schema import Invalid

def archive(name, text):
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w") as z:
        z.writestr(name, text)
    return target.getvalue()

class ReportTests(unittest.TestCase):
    def test_junit_counts(self):
        output = summarize(archive("junit.xml", '<testsuite tests="5" failures="1" errors="0" skipped="2"/>'))
        self.assertIn('"failures": 1', output[0])
        self.assertIn('"tests": 5', output[0])

    def test_missing_counts_are_unknown(self):
        self.assertIn("Unknown", summarize(archive("junit.xml", "<testsuite/>"))[0])

    def test_coverage_and_sarif(self):
        self.assertIn("88", summarize(archive("coverage.json", json.dumps({"total":{"lines":{"pct":88}}})))[0])
        self.assertIn("1 reported results", summarize(archive("analysis.sarif", '{"runs":[{"results":[{"level":"error"}]}]}'))[0])

    def test_traversal_rejected(self):
        with self.assertRaises(Invalid):
            summarize(archive("../outside.xml", "<testsuite/>"))

    def test_xml_entities_rejected(self):
        with self.assertRaises(Invalid):
            summarize(archive("test.xml", '<!DOCTYPE x [<!ENTITY a "a">]><testsuite/>'))

    def test_archive_capacity(self):
        with self.assertRaises(Invalid):
            summarize(archive("large.txt", "x"*200001))

    def test_malformed_report(self):
        with self.assertRaises(Invalid):
            summarize(archive("bad.xml", "<invalid"))

    def test_artifact_redirect_strips_credentials(self):
        requests = []
        def opened(req, **kwargs):
            requests.append(req)
            if len(requests) == 1:
                raise HTTPError(req.full_url, 302, "Found", {"Location":"https://fixture.blob.core.windows.net/artifact?sig=fixture"}, None)
            return io.BytesIO(b"zip fixture")
        api = GitHub("fixture/repo", "not-a-real-token", opened)
        self.assertEqual(b"zip fixture", api.artifact(1))
        self.assertIn("Authorization", requests[0].headers)
        self.assertNotIn("Authorization", requests[1].headers)

    def test_artifact_ssrf_rejected(self):
        def opened(req, **kwargs):
            raise HTTPError(req.full_url, 302, "Found", {"Location":"http://169.254.169.254/latest"}, None)
        with self.assertRaises(Invalid):
            GitHub("fixture/repo", "fixture", opened).artifact(1)
