"""Reviewable, idempotent installation with managed-file conflict detection."""
import copy
import difflib
import json
import re
from pathlib import Path
from .defaults import DEFAULT
from .schema import Invalid, check
from .security import SHA, digest, path_ok

START = "<!-- passport:begin -->"
END = "<!-- passport:end -->"
MANIFEST = ".passport/install.json"

def workflow(ref):
    return """name: Software Signal Passport
on:
  pull_request_target:
    types: [opened, synchronize, reopened, edited, ready_for_review]
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      pr:
        description: Pull request number to reassess
        required: true
permissions: {}
concurrency:
  group: passport-${{ github.event.pull_request.number || github.event.issue.number || inputs.pr }}
  cancel-in-progress: false
jobs:
  passport:
    if: >-
      github.event_name != 'issue_comment' ||
      (github.event.issue.pull_request && startsWith(github.event.comment.body, '/passport '))
    permissions:
      contents: read
      pull-requests: write
      issues: read
      checks: read
      actions: read
    uses: suyog19/software-signal-passport/.github/workflows/passport.yml@""" + ref + """
    with:
      runtime-ref: """ + ref + """
      pr: ${{ github.event.pull_request.number || github.event.issue.number || inputs.pr }}
    secrets:
      model-key: ${{ secrets.PASSPORT_MODEL_KEY }}
"""

def safe_file(root, name):
    if not path_ok(name):
        raise Invalid("Unsafe install path")
    p = root/name
    if any(x.is_symlink() for x in [p, *p.parents]) or not p.resolve().is_relative_to(root.resolve()):
        raise Invalid("Symlink or escaping install path: "+name)
    return p

def install(root, ref, dry_run=False, remove=False):
    root = Path(root).resolve()
    if not re.fullmatch(SHA, ref):
        raise Invalid("Installation requires a reviewed immutable 40-character --ref")
    manifest_path = safe_file(root, MANIFEST)
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"files": {}, "blocks": {}}
    if set(old) != {"files", "blocks"}:
        raise Invalid("Invalid installation manifest")
    config_path = safe_file(root, ".passport/config.json")
    config = json.loads(config_path.read_text()) if config_path.exists() else copy.deepcopy(DEFAULT)
    check("config", config)
    target = {
        ".passport/config.json": json.dumps(config, indent=2)+"\n",
        ".passport/POLICY.md": (Path(__file__).parent/"policy.md").read_text(),
        ".github/workflows/passport-review.yml": workflow(ref)
    }
    blocks = {
        "AGENTS.md": "Read .passport/POLICY.md before changing code. Follow its draft-PR, handoff, question and takeover workflow. Repository governance retains precedence.",
        "CLAUDE.md": "Read .passport/POLICY.md before changing code. Follow its draft-PR, handoff, question and takeover workflow. Repository governance retains precedence.",
        ".github/PULL_REQUEST_TEMPLATE.md": "Passport drafts the Review Brief automatically. Open a draft PR early; see [.passport/POLICY.md](../.passport/POLICY.md). Supply intent and answer genuine gaps; do not manually author a Passport."
    }
    # Preserve all GitHub template locations; do not shadow an existing default.
    guidance = blocks.pop(".github/PULL_REQUEST_TEMPLATE.md")
    templates = []
    for folder in ("", ".github", "docs"):
        parent = root/folder
        if parent.is_dir():
            for candidate in parent.iterdir():
                if candidate.is_file() and candidate.name.lower() == "pull_request_template.md":
                    templates.append(candidate.relative_to(root).as_posix())
                elif candidate.is_dir() and candidate.name.lower() == "pull_request_template":
                    templates.extend(p.relative_to(root).as_posix() for p in candidate.iterdir() if p.is_file())
    for name in templates or [".github/PULL_REQUEST_TEMPLATE.md"]:
        prefix = "../"*len(Path(name).parent.parts)
        blocks[name] = guidance.replace("../.passport/POLICY.md", prefix+".passport/POLICY.md")
    if remove:
        blocks = {name: blocks.get(name, "") for name in old["blocks"]}
    changes = {}
    new = {"files": {}, "blocks": {}}
    for name, content in target.items():
        p = safe_file(root, name)
        before = p.read_bytes().decode("utf-8") if p.exists() else ""
        if name in old["files"]:
            if digest(before) != old["files"][name] and name != ".passport/config.json":
                raise Invalid("Modified managed file; reconcile before update/removal: "+name)
        elif p.exists() and (name != ".passport/config.json" or before != content):
            raise Invalid("Existing unmanaged file; preserve and reconcile: "+name)
        if remove:
            if p.exists() and digest(before) != old["files"].get(name):
                raise Invalid("Modified file preserved; reconcile before removal: "+name)
            after = None
        else:
            after = content
            new["files"][name] = digest(content)
        changes[name] = (before, after)
    for name, text in blocks.items():
        p = safe_file(root, name)
        before = p.read_bytes().decode("utf-8") if p.exists() else ""
        block = START+"\n"+text+"\n"+END
        if START in before or END in before:
            if before.count(START) != 1 or before.count(END) != 1:
                raise Invalid("Ambiguous Passport markers: "+name)
            a, tail = before.split(START)
            middle, b = tail.split(END)
            existing = START+middle+END
            if digest(existing) != old["blocks"].get(name, {}).get("digest"):
                raise Invalid("Modified or unmanaged instruction block: "+name)
            entry = old["blocks"][name]
            if remove and entry.get("prefix") and a.endswith(entry["prefix"]):
                a = a[:-len(entry["prefix"])]
            if remove and entry.get("suffix") and b.startswith(entry["suffix"]):
                b = b[len(entry["suffix"]):]
            after = a+("" if remove else block)+b
        else:
            if name in old["blocks"]:
                raise Invalid("Managed instruction block removed: "+name)
            if "GENERATED BY" in before:
                raise Invalid("Generated instructions preserved. Integrate the canonical policy through your generator before installing: "+name)
            prefix = ("\n" if before and not before.endswith("\n") else "")+"\n"
            entry = {"digest": digest(block), "prefix": prefix, "suffix": "\n", "created": not p.exists()}
            after = before if remove else before+prefix+block+"\n"
        if not remove:
            new["blocks"][name] = {**entry, "digest": digest(block)}
        changes[name] = (before, None if remove and entry.get("created") and not after else after)
    old_manifest = manifest_path.read_text() if manifest_path.exists() else ""
    changes[MANIFEST] = (old_manifest, None if remove else json.dumps(new, indent=2)+"\n")
    if remove and not manifest_path.exists():
        raise Invalid("No Passport installation manifest; nothing removed")
    for name, (before, after) in changes.items():
        if before != (after or ""):
            print("".join(difflib.unified_diff(before.splitlines(True), (after or "").splitlines(True), fromfile=name, tofile=name)), end="")
    if not dry_run:
        # Validate every conflict and destination before the first mutation.
        for name, (_, after) in changes.items():
            p = safe_file(root, name)
            if after is None:
                p.unlink(missing_ok=True)
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(after.encode("utf-8"))
    return [name for name, (before, after) in changes.items() if before != (after or "")]
