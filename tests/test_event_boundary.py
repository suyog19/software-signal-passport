import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from passport.__main__ import analyze, event_identity
from passport.defaults import DEFAULT
from passport.schema import Invalid
from test_passport import pr, evidence, comment, handoff, REPO

class EventBoundaryTests(unittest.TestCase):
    def test_unauthorized_trigger_stops_before_collection_or_model(self):
        cfg = copy.deepcopy(DEFAULT)
        cfg["model"]["enabled"] = True
        trigger = comment("refresh", login="outsider")
        trigger["issue_url"] = f"https://api.github.com/repos/{REPO}/issues/1"
        client = Mock()
        client.get.side_effect = [pr(), trigger]
        client.permission.return_value = "none"
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory)/"event.json"
            event.write_text(json.dumps({"comment":{"id":1}}))
            with patch.dict(os.environ, {"GITHUB_EVENT_NAME":"issue_comment", "GITHUB_EVENT_PATH":str(event)}), patch(
                "passport.__main__.event_identity", return_value=REPO), patch(
                "passport.__main__.api", return_value=client), patch(
                "passport.__main__.configuration", return_value=cfg), patch(
                "passport.__main__.collect") as collected, patch("passport.__main__.provider") as provider:
                with self.assertRaisesRegex(Invalid, "Unauthorized"):
                    analyze(1, str(Path(directory)/"out.json"))
                collected.assert_not_called()
                provider.assert_not_called()

    def test_fork_never_calls_provider(self):
        cfg = copy.deepcopy(DEFAULT)
        cfg["model"]["enabled"] = True
        pull = pr()
        pull["head"]["repo"]["full_name"] = "outsider/fork"
        client = Mock()
        client.get.return_value = pull
        client.permission.return_value = "write"
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"GITHUB_EVENT_NAME":"pull_request_target"}), patch(
            "passport.__main__.event_identity", return_value=REPO), patch(
            "passport.__main__.api", return_value=client), patch(
            "passport.__main__.configuration", return_value=cfg), patch(
            "passport.__main__.collect", return_value=evidence()), patch("passport.__main__.provider") as provider:
            target = Path(directory)/"state.json"
            analyze(1, str(target))
            provider.assert_not_called()
            self.assertIn("Fork PR", str(json.loads(target.read_text())["state"]["uncertainties"]))

    def test_event_identity_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)/"event.json"
            target.write_text(json.dumps({"repository":{"full_name":"other/repo"},"pull_request":{"number":1}}))
            with patch.dict(os.environ, {"GITHUB_ACTIONS":"true","GITHUB_REPOSITORY":REPO,
                "GITHUB_EVENT_NAME":"pull_request_target","GITHUB_EVENT_PATH":str(target)}):
                with self.assertRaisesRegex(Invalid, "repository mismatch"):
                    event_identity(1)
