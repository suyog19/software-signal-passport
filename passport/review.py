"""A separate deterministic review stage; no draft-stage authority."""
from .security import github_url

def run(state, current_head):
    findings = []
    if state["assessed_commit"] != current_head:
        state["stale"] = True
        findings.append("Assessed revision is stale; reassessment required")
    known = {e["url"]: e for e in state["evidence"]}
    for e in state["evidence"]:
        if e["revision"] != current_head:
            findings.append("Stale evidence: "+e["id"])
    handoff = state["handoff"][0]["data"] if state["handoff"] else {}
    for claim in handoff.get("verification", []):
        if not claim["evidence"] or not all(u in known for u in claim["evidence"]):
            findings.append("Handoff test declaration lacks observed evidence: "+claim["claim"][:300])
        if "pass" in claim["claim"].lower() and any(
            any(word in e["summary"].lower() for word in ("failure", "cancelled", "timed_out", ": error"))
            for e in state["evidence"] if e["kind"] in {"check-result", "commit-status"}
        ):
            findings.append("Claimed passing verification contradicts observed failed/cancelled checks")
    for q in state["questions"]:
        if q["status"] != "answered":
            continue
        answers = [a for a in state["answers"] if a["id"] in q["answer_ids"] and a["data"]["assessed_commit"] == current_head]
        if not answers:
            continue
        answer = answers[-1]
        links = answer["data"]["evidence"]
        verified = bool(links) and all(url in known for url in links)
        if q["id"] == "Q-verification":
            verified = verified and any(known[url]["kind"] in {"check-result", "commit-status"} and (
                known[url]["summary"].endswith(": success")) for url in links)
        if q["id"] == "Q-handoff":
            verified = verified and bool(handoff)
        if verified:
            q["status"] = "resolved"
            q["resolution_reason"] = "Separate review matched cited evidence to the assessed revision; answer remains an attributable declaration, not proof of correctness"
        else:
            findings.append(q["id"]+": answer recorded, but evidence is missing, inaccessible, stale or not among observed sources")
    if state["depth"] in {"None", "Light"} and state["questions"]:
        findings.append("Review proportionality: questions persisted from prior consequential assessment")
    for q in state["questions"]:
        if q["status"] in {"open", "answered", "accepted-unresolved"}:
            findings.append(q["id"]+": "+q["status"]+"; "+q["reason"])
    return {"revision": current_head, "stage": "independent-review", "findings": findings[:100],
            "model": {"interpretations": [], "uncertainties": []}}
