import argparse
import datetime
import json
import os
from pathlib import Path
import re
import sys
from .schema import Invalid, check, parse
from .security import REPO, SHA, digest
from .install import install
from .github import GitHub
from .evidence import configuration, collect
from .engine import assess
from .provider import provider
from .render import MARKER, extract, render

def api(repo):
    return GitHub(repo, os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))

def canonical(comments):
    matched = [c for c in comments if c.get("body", "").startswith(MARKER)
               and c["user"]["login"] == "github-actions[bot]" and c["user"]["type"] == "Bot"]
    if len(matched) > 1:
        raise Invalid("Multiple canonical bot comments; investigate before reassessment")
    return matched[0] if matched else None

def event_identity(number):
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise Invalid("Analyze/publish requires GitHub Actions event provenance; use fixture assessment for local tests")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    event = parse(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    if event.get("repository", {}).get("full_name") != repo:
        raise Invalid("Event repository mismatch")
    name = os.environ.get("GITHUB_EVENT_NAME")
    if name == "pull_request_target":
        actual = event.get("pull_request", {}).get("number")
    elif name == "issue_comment":
        actual = event.get("issue", {}).get("number") if event.get("issue", {}).get("pull_request") else None
        if not event.get("comment", {}).get("body", "").startswith("/passport "):
            raise Invalid("Not a Passport command")
    elif name == "workflow_dispatch":
        try:
            actual = int(event.get("inputs", {}).get("pr", 0))
        except (TypeError, ValueError):
            actual = None
    else:
        raise Invalid("Unsupported event provenance")
    if actual != number:
        raise Invalid("PR number does not match triggering event")
    return repo

def analyze(number, output):
    repo = event_identity(number)
    client = api(repo)
    pr = client.get(f"pulls/{number}")
    config = configuration(client, pr["base"]["sha"])
    if not config["enabled"]:
        Path(output).write_text(json.dumps({"disabled": True}))
        return
    evidence = collect(client, number, config, pr)
    existing = canonical(evidence["comments"])
    previous = extract(existing["body"]) if existing else None
    model = None
    if config["model"]["enabled"] and pr["head"]["repo"]["full_name"] == repo:
        model = provider(config["model"], os.environ.get("PASSPORT_MODEL_KEY"))
    state = assess(repo, pr, config, evidence, previous, datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   client.permission, model)
    if config["model"]["enabled"] and pr["head"]["repo"]["full_name"] != repo:
        state["uncertainties"].append("Fork PR: model provider disabled; no model credential used")
    current = client.get(f"pulls/{number}")["head"]["sha"]
    if current != state["assessed_commit"]:
        state["stale"] = True
        state["advisory"] = "stale"
    render(state, current)
    envelope = {"disabled": False, "state": state, "previous_digest": digest(previous), "config_digest": digest(config)}
    Path(output).write_text(json.dumps(envelope), encoding="utf-8")

def publish(number, source):
    repo = event_identity(number)
    envelope = parse(Path(source).read_text())
    client = api(repo)
    pr = client.get(f"pulls/{number}")
    config = configuration(client, pr["base"]["sha"])
    if not config["enabled"]:
        return
    if envelope.get("disabled"):
        raise Invalid("Configuration changed during assessment; rerun")
    state = check("state", envelope["state"])
    if state["repository"] != repo or state["pr"] != number or envelope["config_digest"] != digest(config):
        raise Invalid("Assessment identity/policy mismatch; rerun")
    comments = client.pages(f"issues/{number}/comments", maximum=300)
    existing = canonical(comments)
    previous = extract(existing["body"]) if existing else None
    if digest(previous) != envelope["previous_digest"]:
        raise Invalid("State changed during assessment; rerun to avoid overwriting")
    current = pr["head"]["sha"]
    if current != state["assessed_commit"]:
        state["stale"] = True
        state["advisory"] = "stale"
    body = render(state, current)
    if existing and existing["body"] == body:
        print("Duplicate assessment: canonical comment unchanged")
        return
    path = f"/repos/{repo}/issues/comments/{existing['id']}" if existing else f"/repos/{repo}/issues/{number}/comments"
    client.request(path, "PATCH" if existing else "POST", {"body": body})
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).write_text(body.split("<!-- passport-state:")[0], encoding="utf-8")
    print("Passport advisory state published")
    if state["stale"]:
        raise Invalid("Head changed during assessment; stale state published, rerun")

def main():
    p = argparse.ArgumentParser(description="Software Signal Passport advisory workflow")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("install", "update", "remove"):
        s = sub.add_parser(name)
        s.add_argument("--root", required=True)
        s.add_argument("--ref", required=True)
        s.add_argument("--dry-run", action="store_true")
    v = sub.add_parser("validate")
    v.add_argument("kind", choices=["config", "handoff", "answer", "action", "state", "model"])
    v.add_argument("file")
    for name in ("analyze", "publish", "inspect"):
        s = sub.add_parser(name)
        s.add_argument("--pr", required=True, type=int)
        if name == "inspect":
            s.add_argument("--repo", required=True)
        else:
            s.add_argument("--file", required=True)
    args = p.parse_args()
    try:
        if args.cmd in {"install", "update", "remove"}:
            install(args.root, args.ref, args.dry_run, args.cmd == "remove")
        elif args.cmd == "validate":
            check(args.kind, parse(Path(args.file).read_text()))
            print("Valid "+args.kind)
        elif args.cmd == "analyze":
            analyze(args.pr, args.file)
        elif args.cmd == "publish":
            publish(args.pr, args.file)
        else:
            client = api(args.repo)
            current = client.get(f"pulls/{args.pr}")
            c = canonical(client.pages(f"issues/{args.pr}/comments", maximum=300))
            if not c:
                raise Invalid("Passport not found; check installation and workflow status")
            state = extract(c["body"])
            state["stale"] = state["assessed_commit"] != current["head"]["sha"]
            print(json.dumps(state, indent=2))
    except (Invalid, OSError, KeyError, ValueError) as exc:
        print("Passport failed: "+str(exc) if isinstance(exc, Invalid) else "Passport failed: invalid input or inaccessible file; inspect configuration and event", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
