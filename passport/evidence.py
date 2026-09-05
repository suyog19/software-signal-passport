import fnmatch
import re
from urllib.parse import quote
from .schema import Invalid, check, parse
from .security import path_ok, redact
from .reports import summarize

DEPTHS = ["None", "Light", "Standard", "High-consequence"]

def configuration(api, base):
    raw = api.file(".passport/config.json", base)
    if raw is None:
        raise Invalid("Passport config not on trusted base; merge reviewed installation first")
    config = check("config", parse(raw))
    if not {"pr", "files"}.issubset(config["evidence_sources"]):
        raise Invalid("pr and files evidence sources are required for truthful assessment")
    if any(not path_ok(p) for p in config["context_paths"]):
        raise Invalid("Unsafe context path")
    return config

def select_depth(files, config):
    values, reasons = [], []
    for item in files:
        for path in [item["filename"], item.get("previous_filename", item["filename"])]:
            if any(fnmatch.fnmatchcase(path, p) for p in config["sensitive_paths"]):
                values.append(3)
                reasons.append("Sensitive path: "+path)
            else:
                matches = [c for c in config["change_classes"] if any(fnmatch.fnmatchcase(path, p) for p in c["paths"])]
                level = max((DEPTHS.index(c["depth"]) for c in matches), default=DEPTHS.index(config["default_depth"]))
                values.append(level)
    return DEPTHS[max(values, default=0)], "; ".join(reasons)[:900] or "Highest matching repository change class; default applies to unmatched paths"

def collect(api, number, config, pr):
    head, base = pr["head"]["sha"], pr["base"]["sha"]
    files = api.pages(f"pulls/{number}/files", maximum=300)
    if len(files) != pr["changed_files"]:
        raise Invalid("Incomplete changed-file evidence; rerun or split the PR")
    comments = api.pages(f"issues/{number}/comments", maximum=300)
    checks = api.pages(f"commits/{head}/check-runs", "check_runs", 100) if "checks" in config["evidence_sources"] else []
    statuses = api.pages(f"commits/{head}/statuses", maximum=100) if "checks" in config["evidence_sources"] else []
    url = "https://github.com/"+api.repo
    evidence = [{"id": "pr", "kind": "observed-metadata", "summary": redact(pr["title"])[:1000], "url": url+f"/pull/{number}", "revision": head}]
    for index, f in enumerate(files):
        path = f["filename"]
        if not path_ok(path):
            raise Invalid("Unsafe changed filename")
        tags = []
        for label, pattern in [("dependency", r"(lock|requirements|package.json|pyproject|go.mod)"),
                               ("migration", r"migration|\.sql$"), ("interface", r"schema|openapi|\.proto$"),
                               ("deployment/recovery", r"deploy|rollback|Dockerfile|terraform")]:
            if re.search(pattern, path, re.I):
                tags.append(label)
        evidence.append({"id": f"file-{index}", "kind": "changed-file",
                         "summary": redact(f"{path}: {f['status']}, +{f['additions']} -{f['deletions']}; signals: {', '.join(tags) or 'none detected'}")[:1000],
                         "url": url+"/blob/"+head+"/"+quote(path, safe="/"), "revision": head})
    for c in checks:
        evidence.append({"id": "check-"+str(c["id"]), "kind": "check-result",
                         "summary": redact(c["name"]+": "+str(c.get("conclusion") or c["status"]))[:1000],
                         "url": url+f"/pull/{number}/checks?check_run_id={c['id']}", "revision": c["head_sha"]})
    seen = set()
    for c in statuses:
        if c["context"] in seen:
            continue
        seen.add(c["context"])
        evidence.append({"id": "status-"+str(c["id"]), "kind": "commit-status",
                         "summary": redact(c["context"]+": "+c["state"])[:1000],
                         "url": url+"/commit/"+head, "revision": head})
    report_gaps = []
    if "checks" in config["evidence_sources"]:
        runs = api.pages(f"actions/runs?head_sha={head}", "workflow_runs", 100)
        reports = []
        for run in runs[:5]:
            if run.get("head_sha") != head:
                continue
            artifacts = api.pages(f"actions/runs/{run['id']}/artifacts", "artifacts", 100)
            reports.extend((run, a) for a in artifacts if re.search(r"test|junit|coverage|sarif|security|static|lint", a["name"], re.I))
        if not reports:
            report_gaps.append("Test, coverage, static-analysis and security report artifacts: Not found; check status alone does not establish report coverage")
        for run, artifact in reports[:4]:
            report_url = url+f"/actions/runs/{run['id']}/artifacts/{artifact['id']}"
            try:
                if artifact.get("expired") or artifact.get("size_in_bytes", 1000001) > 1000000:
                    raise Invalid("Report expired or exceeds 1 MB")
                summaries = summarize(api.artifact(artifact["id"]))
                for i, summary in enumerate(summaries[:8]):
                    evidence.append({"id": f"report-{artifact['id']}-{i}", "kind": "workflow-report",
                        "summary": "Observed publisher report: "+summary, "url": report_url, "revision": head})
            except Invalid as exc:
                report_gaps.append("Report "+artifact["name"]+": "+str(exc))
        if len(reports) > 4 or len(runs) > 5:
            report_gaps.append("Report collection bounded to five runs and four matching artifacts; additional reports uninspected")
    else:
        report_gaps.append("Checks and report collection disabled by repository policy")
    context = []
    if "context" in config["evidence_sources"]:
        for path in config["context_paths"]:
            content = api.file(path, base)
            context.append({"path": path, "revision": base, "url": url+"/blob/"+base+"/"+quote(path, safe="/"),
                            "text": redact(content or "")[:6000], "status": "Not found" if content is None else "Observed at trusted base; truncated" if len(content)>6000 else "Observed at trusted base"})
    issue_refs = re.findall(r"(?<![A-Za-z0-9])#([0-9]+)", (pr.get("body") or ""))[:20]
    for n in dict.fromkeys(issue_refs):
        evidence.append({"id": "issue-"+n, "kind": "declared-issue-reference", "summary": "PR body references issue #"+n,
                         "url": url+"/issues/"+n, "revision": head})
    return {"files": files, "comments": comments, "evidence": evidence, "context": context, "checks": checks, "statuses": statuses, "report_gaps": report_gaps}
