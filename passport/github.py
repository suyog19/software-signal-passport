"""Bounded GitHub API transport. Never executes repository content."""
import base64
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from .schema import Invalid, parse
from .security import REPO, SHA, path_ok

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

class GitHub:
    def __init__(self, repo, token, opener=None, sleep=time.sleep):
        if not re.fullmatch(REPO, repo):
            raise Invalid("Invalid repository identity")
        if not token:
            raise Invalid("Missing GitHub token; provide GITHUB_TOKEN with documented permissions")
        self.repo, self.token = repo, token
        self.open = opener or build_opener(NoRedirect()).open
        self.sleep = sleep

    def request(self, path, method="GET", data=None):
        if not path.startswith("/repos/"+self.repo+"/") or ".." in path or "\\" in path:
            raise Invalid("API path outside repository")
        body = None if data is None else json.dumps(data).encode()
        for attempt in range(3):
            try:
                req = Request("https://api.github.com"+path, data=body, method=method, headers={
                    "Authorization": "Bearer "+self.token, "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json",
                    "User-Agent": "software-signal-passport/0.2.0"})
                with self.open(req, timeout=30) as response:
                    raw = response.read(1000001)
                if len(raw) > 1000000:
                    raise Invalid("GitHub response exceeds 1 MB; narrow the change")
                return parse(raw.decode()) if raw else {}
            except HTTPError as exc:
                if method == "GET" and exc.code in {429, 500, 502, 503, 504} and attempt < 2:
                    self.sleep(2**attempt)
                    continue
                raise Invalid(f"GitHub {method} failed (HTTP {exc.code}); check permissions or rerun") from None
            except (URLError, TimeoutError):
                if method == "GET" and attempt < 2:
                    self.sleep(2**attempt)
                    continue
                raise Invalid("GitHub connection failed; inspect run and rerun (writes are not blindly retried)") from None

    def get(self, suffix):
        return self.request("/repos/"+self.repo+"/"+suffix)

    def pages(self, suffix, key=None, maximum=400):
        result = []
        for page in range(1, maximum//100+2):
            data = self.get(suffix+("&" if "?" in suffix else "?")+f"per_page=100&page={page}")
            items = data[key] if key else data
            if not isinstance(items, list):
                raise Invalid("Unexpected GitHub list response")
            result.extend(items)
            if len(result) > maximum:
                raise Invalid("GitHub evidence exceeds bounded capacity; split the PR or archive old discussion")
            if len(items) < 100:
                return result
        raise Invalid("GitHub pagination exceeded capacity")

    def file(self, path, revision):
        if not path_ok(path) or not re.fullmatch(SHA, revision):
            raise Invalid("Unsafe repository context path/revision")
        try:
            item = self.get("contents/"+quote(path, safe="/")+"?ref="+revision)
        except Invalid as exc:
            if "HTTP 404" in str(exc):
                return None
            raise
        if item.get("type") != "file" or item.get("encoding") != "base64" or item.get("size", 100000) > 32000:
            raise Invalid("Context is not a small ordinary file: "+path)
        return base64.b64decode(item["content"], validate=False).decode("utf-8")

    def permission(self, login):
        if not re.fullmatch(r"[A-Za-z0-9_\[\]-]{1,100}", login):
            return "none"
        try:
            return self.get("collaborators/"+quote(login)+"/permission").get("permission", "none")
        except Invalid as exc:
            if "HTTP 404" in str(exc):
                return "none"
            raise

    def artifact(self, ident):
        if type(ident) is not int or ident < 1:
            raise Invalid("Invalid artifact identity")
        request = Request(f"https://api.github.com/repos/{self.repo}/actions/artifacts/{ident}/zip",
                          headers={"Authorization": "Bearer "+self.token, "User-Agent": "software-signal-passport"})
        try:
            self.open(request, timeout=30)
            raise Invalid("Expected GitHub artifact redirect")
        except HTTPError as exc:
            if exc.code != 302:
                raise Invalid(f"Artifact unavailable (HTTP {exc.code})") from None
            location = exc.headers.get("Location", "")
        target = urlsplit(location)
        host = target.hostname or ""
        if target.scheme != "https" or target.username or target.password or target.port not in (None, 443) or not (
            host.endswith(".blob.core.windows.net") or host.endswith(".actions.githubusercontent.com")):
            raise Invalid("Artifact download host is not permitted")
        # No Authorization header is forwarded to the signed artifact location.
        try:
            with self.open(Request(location, headers={"User-Agent": "software-signal-passport"}), timeout=30) as response:
                content = response.read(1000001)
            if len(content) > 1000000:
                raise Invalid("Report archive exceeds 1 MB")
            return content
        except (HTTPError, URLError, TimeoutError):
            raise Invalid("Artifact download failed; report content unavailable") from None
