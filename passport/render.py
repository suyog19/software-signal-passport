import base64
import json
import re
from .schema import Invalid, check, parse
from .security import safe_text
MARKER = "<!-- software-signal-passport:v1 -->"

def extract(body):
    matches = re.findall(r"<!-- passport-state:([A-Za-z0-9+/=]+) -->", body)
    if len(matches) != 1:
        raise Invalid("Canonical Passport state is missing or ambiguous; preserve and investigate")
    try:
        return check("state", parse(base64.b64decode(matches[0], validate=True).decode()))
    except (ValueError, UnicodeError):
        raise Invalid("Malformed canonical state") from None

def render(state, current_head=None):
    check("state", state)
    stale = state["stale"] or (current_head and state["assessed_commit"] != current_head)
    root = "https://github.com/"+state["repository"]
    lines = [MARKER, "## Software Signal Passport", "",
        "**"+("STALE — reassessment required" if stale else state["advisory"])+"** · "+state["depth"]+" · advisory only",
        "", "Assessed ["+state["assessed_commit"][:12]+"]("+root+"/commit/"+state["assessed_commit"]+") · brief "+str(state["brief_revision"]),
        "", "**Intended outcome (declaration):** "+safe_text(state["intent"], 700),
        "", "**Depth:** "+safe_text(state["rationale"], 500)]
    if state["previous_commit"]:
        lines += ["", "Previous assessment and its answers became stale after a new commit."]
    outstanding = any(q["status"] not in {"resolved", "superseded"} for q in state["questions"])
    if state["depth"] != "None" or outstanding or state["command_errors"]:
        lines += ["", "**Accountable owner:** "+safe_text("; ".join(state["roles"]), 400)]
        handoff = state["handoff"][0]["data"] if state["handoff"] else {}
        lines += ["", "**Context / rules (declaration):** "+safe_text(handoff.get("business_rules") or "Unknown", 500),
                  "", "**Recovery (declaration):** "+safe_text(handoff.get("rollback") or "Unknown", 400),
                  "", "**Verification observed:**"]
        checks = [e for e in state["evidence"] if e["kind"] in {"check-result", "commit-status"}]
        lines += ["- ["+safe_text(e["summary"], 160)+"]("+e["url"]+")" for e in checks[:8]] or ["- Not found; test definitions and author claims are not performed checks."]
        lines += ["", "**Unverified / uncertainty:**"]
        gaps = state["uncertainties"] + state["review"]["findings"]
        lines += ["- "+safe_text(g, 400) for g in gaps[:8]] or ["- No additional deterministic gaps detected; correctness and human approval are not established."]
        for role in ("agent", "human"):
            questions = [q for q in state["questions"] if q["role"] == role and q["status"] not in {"resolved", "superseded"}]
            if questions:
                lines += ["", "**Questions for "+role+":**"]
                lines += ["- **"+q["id"]+"** ("+q["status"]+"): "+safe_text(q["text"], 500) for q in questions[:8]]
        if state["inferences"]:
            lines += ["", "**Model interpretation — not evidence:**"]
            lines += ["- "+safe_text(i["text"], 500)+" (sources: "+safe_text(", ".join(i["evidence_ids"]))+")" for i in state["inferences"][:3]]
        if state["command_errors"]:
            lines += ["", "**Commands needing correction:**"]+["- "+safe_text(x, 400) for x in state["command_errors"][-5:]]
    lines += ["", "<details><summary>Evidence and protocol</summary>", "",
              "Respond with /passport answer JSON or /passport action JSON. Use /passport refresh after checks finish.",
              "Agent takeover uses this state, PR history and handoff; no session resume is assumed.", "",
              "Separate review stage: "+safe_text(state["provenance"]["reviewer"])+".",
              "No merge approval, certification or safety score is granted.", ""]
    lines += ["- ["+safe_text(e["summary"], 200)+"]("+e["url"]+")" for e in state["evidence"][:30]]
    lines += ["", "</details>", ""]
    encoded = base64.b64encode(json.dumps(state, separators=(",", ":"), ensure_ascii=True).encode()).decode()
    lines.append("<!-- passport-state:"+encoded+" -->")
    result = "\n".join(lines)+"\n"
    if len(result.encode()) > 64000:
        raise Invalid("Passport state exceeds comment capacity; preserve previous state and split the change")
    return result
