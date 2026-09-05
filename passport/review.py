"""Separately recorded deterministic evidence review, not code assurance."""
def run(state, current_head):
    findings = []
    if state["assessed_commit"] != current_head:
        state["stale"] = True
        findings.append("Assessed revision is stale; reassessment required")
    known = {e["url"]: e for e in state["evidence"]}
    checks = [e for e in state["evidence"] if e["kind"] in {"check-result", "commit-status"}]
    failed = [e for e in checks if any(word in e["summary"].lower() for word in (": failure", ": error", ": cancelled", ": timed_out", ": action_required"))]
    pending = [e for e in checks if not any(e["summary"].endswith(": "+v) for v in ("success", "neutral", "skipped", "failure", "error", "cancelled", "timed_out", "action_required"))]
    for e in state["evidence"]:
        if e["revision"] != current_head:
            findings.append("Stale evidence: "+e["id"])
    for e in failed:
        findings.append("Verification failed: "+e["summary"])
    for e in pending:
        findings.append("Verification not completed: "+e["summary"])
    handoff = state["handoff"][0]["data"] if state["handoff"] else {}
    for claim in handoff.get("verification", []):
        if not claim["evidence"] or not all(u in known and known[u]["kind"] in {"check-result", "commit-status"} for u in claim["evidence"]):
            findings.append("Handoff test declaration lacks observed evidence: "+claim["claim"][:300])
        if "pass" in claim["claim"].lower() and failed:
            findings.append("Claimed passing verification contradicts observed failed/cancelled checks")
    for q in state["questions"]:
        before_status = q["status"]
        if q["status"] in {"accepted-unresolved", "superseded"}:
            continue
        if q["id"] == "Q-handoff":
            supplied = bool(handoff) and bool(handoff.get("participation", "").strip())
            q["status"] = "resolved" if supplied else "open"
            q["resolution_reason"] = "Current-revision structured handoff observed; contents remain declarations" if supplied else "No current handoff observed"
        elif q["id"] == "Q-verification":
            successful = [e for e in checks if e["revision"] == current_head and e["summary"].endswith(": success")]
            supplied = bool(successful) and not failed and not pending
            q["status"] = "resolved" if supplied else "open"
            q["resolution_reason"] = "Current checks completed successfully; scope is limited to named checks, not overall correctness" if supplied else "Current verification missing, pending or failing"
        elif q["status"] == "answered":
            # Arbitrary metadata/file URLs never establish recovery, business rules
            # or the truth of a technical claim. Human verification can close it.
            findings.append(q["id"]+": answer received; substantive verification is not automated")
        if q["status"] != before_status:
            q["updated_at"] = state["updated_at"]
    if state["depth"] in {"None", "Light"} and state["questions"]:
        findings.append("Review proportionality: questions persisted from prior consequential assessment")
    for q in state["questions"]:
        if q["status"] in {"open", "answered", "accepted-unresolved"}:
            findings.append(q["id"]+": "+q["status"]+"; "+q["reason"])
    return {"revision": current_head, "stage": "independent-review", "findings": findings[:100],
            "model": {"interpretations": [], "uncertainties": []}}
