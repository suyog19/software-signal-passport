import hashlib
import html
import json
import re
from pathlib import PurePosixPath
from urllib.parse import urlsplit

SHA = r"[0-9a-f]{40}"
REPO = r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def path_ok(value):
    p = PurePosixPath(value)
    return bool(value) and not p.is_absolute() and all(x not in {"", ".", ".."} for x in value.split("/")) and not re.search(r"[\\:\x00-\x1f]", value)

def redact(value):
    text = str(value)
    for pattern in (r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
                    r"\bsk-[A-Za-z0-9_-]{15,}\b", r"\bAKIA[A-Z0-9]{16}\b",
                    r"-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?-----END [^-]*PRIVATE KEY-----"):
        text = re.sub(pattern, "[REDACTED]", text)
    text = re.sub(r"(?i)(authorization|api[_-]?key|password|secret|token)\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", text)
    return text

def safe_text(value, limit=1000):
    text = html.escape(redact(value)[:limit], quote=True)
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = text.replace("@", "@\u200b")
    return re.sub(r"([\\\x60*_{}\[\]()#+.!|>~-])", r"\\\1", text)

def github_url(url, repo):
    p = urlsplit(url)
    return p.scheme == "https" and p.netloc == "github.com" and p.path.startswith("/"+repo+"/") and (not p.query or bool(re.fullmatch(r"check_run_id=[0-9]+", p.query))) and not p.fragment.startswith("javascript")
