"""Development-only checks for the distributed Markdown; not a Passport evaluator."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".engineering", "node_modules", "__pycache__", ".validation"}
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[\"'][^\"']*[\"'])?\)")
VERSIONED = "https://github.com/suyog19/software-signal-passport/blob/v0.1.0/"


def prose(text: str) -> str:
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"(?m)^\s*(`{3,}|~{3,})[^\n]*\n[\s\S]*?^\s*\1\s*$", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def anchors(text: str) -> set[str]:
    result: set[str] = set()
    counts: dict[str, int] = {}
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", text):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        index = counts.get(slug, 0)
        counts[slug] = index + 1
        result.add(slug if index == 0 else f"{slug}-{index}")
    return result


def link_errors(root: Path, path: Path, text: str) -> list[str]:
    errors = []
    for raw in LINK.findall(prose(text)):
        target = raw.strip("<>")
        if target.startswith(VERSIONED):
            target = "/" + target[len(VERSIONED):]
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue  # Network liveness is a separate maintainer check.
        if parsed.scheme or target.startswith("//"):
            errors.append(f"unsupported link: {raw}")
            continue
        location = unquote(parsed.path)
        destination = ((root / location.lstrip("/")) if location.startswith("/")
                       else (path.parent / location if location else path)).resolve()
        if not destination.is_relative_to(root.resolve()):
            errors.append(f"link escapes repository: {raw}")
        elif not destination.exists():
            errors.append(f"missing link target: {raw}")
        elif parsed.fragment and destination.is_file() and destination.suffix == ".md":
            if unquote(parsed.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                errors.append(f"missing heading: {raw}")
    return errors


def copy_errors(root: Path, text: str) -> list[str]:
    """Check versioned template help URLs even when inside HTML comments."""
    errors = []
    for target in re.findall(re.escape(VERSIONED) + r"[^\s<>)]+", text):
        relative = target[len(VERSIONED):]
        parsed = urlsplit(relative)
        path = (root / parsed.path).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            errors.append(f"missing copied-template help target: {target}")
    return errors


def public_text_errors(text: str) -> list[str]:
    patterns = {
        "private workstation path": r"(?i)(?:[a-z]:[\\/](?:users|home)[\\/]|/" r"Users/[^/]+/|/" r"home/[^/]+/)",
        "private key": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        "GitHub credential": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b",
        "AWS access key": r"\bAKIA[A-Z0-9]{16}\b",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]


def required_errors(root: Path, required: list[str]) -> list[str]:
    errors = []
    if not required:
        return ["distribution manifest is empty"]
    for name in required:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f"distribution path escapes repository: {name}")
        elif not path.is_file() or not path.stat().st_size:
            errors.append(f"missing or empty distribution file: {name}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    manifest = root / "distributable-files.txt"
    if not manifest.is_file():
        return ["missing distributable-files.txt"]
    required = [line.strip() for line in manifest.read_text().splitlines()
                if line.strip() and not line.startswith("#")]
    errors = required_errors(root, required)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or set(path.relative_to(root).parts) & SKIP:
            continue
        if path.is_symlink():
            errors.append(f"{path.relative_to(root)}: symlink not permitted")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path.relative_to(root)}: unexpected binary/non-UTF-8 file")
            continue
        found = public_text_errors(text)
        if path.suffix == ".md":
            found += link_errors(root, path, text)
            found += copy_errors(root, text)
        errors += [f"{path.relative_to(root)}: {error}" for error in found]
    version = root / "VERSION"
    if version.is_file() and version.read_text().strip() != "0.1.0":
        errors.append("VERSION must match the v0.1.0 distribution")
    return errors


if __name__ == "__main__":
    problems = validate(ROOT)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("Distribution files, supported Markdown links, version and public-text checks passed.")
