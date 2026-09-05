import copy
import fnmatch
import json
from .evidence import select_depth
from .protocol import command, eligible, apply
from .schema import Invalid, check, parse
from .security import digest, redact
from .review import run as review

def assess(repo, pr, config, collected, previous, now, permission, model=None):
    head, base = pr["head"]["sha"], pr["base"]["sha"]
    previous = check("state", previous) if previous else None
    if previous and (previous["repository"] != repo or previous["pr"] != pr["number"]):
        raise Invalid("Previous Passport belongs to a different PR")
    depth, rationale = select_depth(collected["files"], config)
    event_ids = list(previous["provenance"]["event_ids"]) if previous else []
    state = {
        "schema_version": 1, "repository": repo, "pr": pr["number"], "assessed_commit": head, "base_commit": base,
        "depth": depth, "rationale": rationale, "intent": redact(pr["title"])[:2000],
        "context": collected["context"], "handoff": [], "evidence": collected["evidence"],
        "declarations": copy.deepcopy(previous["declarations"]) if previous else [],
        "inferences": [], "uncertainties": [],
        "questions": copy.deepcopy(previous["questions"]) if previous else [],
        "answers": copy.deepcopy(previous["answers"]) if previous else [], "roles": [],
        "review": {"revision": head, "stage": "independent-review", "findings": [], "model": {"interpretations": [], "uncertainties": []}},
        "stale": False, "previous_commit": previous["assessed_commit"] if previous and previous["assessed_commit"] != head else "",
        "brief_revision": previous["brief_revision"]+1 if previous else 1,
        "created_at": previous["created_at"] if previous else now, "updated_at": now,
        "provenance": {"collector": "github-rest/0.2.0", "drafting": "deterministic/0.2.0",
                       "reviewer": "separate-deterministic-stage/0.2.0", "event_ids": event_ids,
                       "round": previous["provenance"]["round"] if previous and previous["assessed_commit"] == head else 0,
                       "input_digest": ""},
        "advisory": "advisory-with-open-questions", "command_errors": []
    }
    if state["previous_commit"]:
        state["uncertainties"].append("Previous assessment "+state["previous_commit"]+" is stale; prior answers and conclusions require reassessment")
        for q in state["questions"]:
            q.update(status="open", assessed_commit=head, answer_ids=[], updated_at=now,
                     resolution_reason="Reopened after new commit; prior evidence stale")
    for owner in config["owners"]:
        if any(fnmatch.fnmatchcase(f["filename"], p) for f in collected["files"] for p in owner["paths"]):
            state["roles"].append(owner["owner"])
    if not state["roles"]:
        state["roles"] = ["Accountable owner Unknown; PR author is not inferred approval"]
    pending = []
    for comment in collected["comments"]:
        if not comment.get("body", "").startswith("/passport "):
            continue
        try:
            parsed = command(comment)
            if parsed is None:
                raise Invalid("Unknown Passport command")
            kind, data = parsed
            if comment.get("updated_at", comment["created_at"]) != comment["created_at"]:
                raise Invalid("Edited command ignored; submit a new attributable comment")
            perm = permission(comment["user"]["login"])
            if not eligible(comment, pr, config, perm):
                raise Invalid("Command author is not an eligible contributor")
            if kind == "handoff":
                if "handoff" in config["evidence_sources"] and data["assessed_commit"] == head:
                    state["handoff"] = [{"author": comment["user"]["login"], "url": comment["html_url"],
                                         "received_at": comment["created_at"], "data": parse(redact(json.dumps(data)))}]
            elif str(comment["id"]) not in event_ids:
                pending.append((comment, data, kind, perm))
        except Invalid as exc:
            state["command_errors"].append(str(comment["id"])+": "+str(exc))
    handoff = state["handoff"][0]["data"] if state["handoff"] else {}
    if handoff:
        state["intent"] = handoff["intent"]
        state["uncertainties"].extend(handoff["uncertainties"])
    def question(qid, text, reason, role, trigger):
        if any(q["id"] == qid for q in state["questions"]):
            return
        state["questions"].append({"id": qid, "text": text, "reason": reason, "trigger": trigger,
            "role": role, "status": "open", "effect": "Visible gap in Review Brief",
            "created_at": now, "updated_at": now, "answer_ids": [], "resolution_reason": "",
            "assessed_commit": head})
    if depth in {"Standard", "High-consequence"}:
        if not handoff:
            question("Q-handoff", "Supply the structured implementation handoff and identify material participation.",
                     "Implementation facts and participation are not supplied", "agent", ["pr"])
        successful = [e for e in state["evidence"] if e["kind"] in {"check-result", "commit-status"} and e["summary"].endswith(": success")]
        if not successful:
            question("Q-verification", "What verification supports this revision? Link a completed check; preserve failures and not-run areas.",
                     "No successful current-revision check observed", "agent", ["pr"])
        required = set(config["required_fields"])
        if depth == "High-consequence":
            required |= {"business_rules", "rollback"}
            question("Q-authority", "Which authorized human owns the sensitive change and its unresolved decisions?",
                     "Sensitive paths require human attention; ownership and approvals cannot be inferred", "human", ["pr"])
        for field in sorted(required):
            if not handoff.get(field):
                question("Q-"+field, "Provide "+field.replace("_", " ")+" or explain its applicability with evidence.",
                         "Applicable repository field is missing", "human" if field == "business_rules" else "agent", ["pr"])
    for comment, data, kind, perm in pending:
        if len(event_ids) >= 200:
            raise Invalid("Command history capacity reached; retain state and archive/export before a new assessment")
        event_ids.append(str(comment["id"]))
        if kind == "refresh":
            continue
        if state["provenance"]["round"] >= config["max_rounds"]:
            state["command_errors"].append("Clarification round limit reached; maintainer must review and raise policy limit deliberately")
            continue
        try:
            apply(state, comment, data, kind, config, perm)
            state["provenance"]["round"] += 1
        except Invalid as exc:
            state["command_errors"].append(str(comment["id"])+": "+str(exc))
    state["provenance"]["input_digest"] = digest({"head": head, "base": base, "commands": [(c["id"], c.get("updated_at"), digest(c.get("body", ""))) for c in collected["comments"] if c.get("body", "").startswith("/passport ")], "config": config, "evidence": state["evidence"], "context": state["context"],
                                                "handoff": state["handoff"], "events": event_ids})
    # Repeat deliveries with unchanged evidence never consume a model call or new state revision.
    if previous and previous["provenance"]["input_digest"] == state["provenance"]["input_digest"]:
        return previous
    if model and depth in {"Standard", "High-consequence"}:
        permitted = {"evidence": state["evidence"], "context": state["context"], "handoff": state["handoff"]}
        try:
            drafted = model.interpret(permitted, "draft")
            state["inferences"] = drafted["interpretations"]
            state["uncertainties"].extend(drafted["uncertainties"])
            state["provenance"]["drafting"] = "openai/"+model.model
        except Invalid as exc:
            state["uncertainties"].append(str(exc))
    state["review"] = review(state, head)
    if model and state["inferences"]:
        try:
            separate = model.interpret({"evidence": state["evidence"], "draft": state["inferences"],
                                        "uncertainties": state["uncertainties"]}, "review")
            state["review"]["model"] = separate
            state["provenance"]["reviewer"] += "; isolated openai invocation"
        except Invalid as exc:
            state["uncertainties"].append("Independent model review unavailable: "+str(exc))
    if depth == "None" and not state["questions"]:
        state["advisory"] = "no-passport-needed"
    elif any(q["status"] in {"open", "answered"} for q in state["questions"]):
        state["advisory"] = "advisory-with-open-questions"
    elif any(q["status"] == "accepted-unresolved" for q in state["questions"]):
        state["advisory"] = "advisory-with-accepted-uncertainty"
    elif state["uncertainties"] or state["review"]["findings"]:
        state["advisory"] = "advisory-with-uncertainty"
    else:
        state["advisory"] = "advisory-reviewed"
    state["command_errors"] = state["command_errors"][-30:]
    return check("state", state)
