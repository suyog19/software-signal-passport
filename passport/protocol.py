import re
from .schema import Invalid, check, parse
from .security import redact, redact_data, github_url

def command(comment):
    body = comment.get("body", "")
    m = re.fullmatch(r"/passport (handoff|answer|action|refresh)(?:\s+([\s\S]*))?", body)
    if not m:
        return None
    kind, payload = m.groups()
    if kind == "refresh":
        if payload and payload.strip():
            raise Invalid("refresh takes no payload")
        return kind, {}
    data = check(kind, parse(payload or ""))
    return kind, data

def eligible(comment, pr, config, permission):
    login = comment["user"]["login"]
    return login == pr["user"]["login"] or login in config["agent_accounts"] or permission in {"write", "maintain", "admin"}

def human(comment, data, config, permission):
    return (data.get("role") == "human" and comment["user"]["type"] == "User"
            and comment["user"]["login"] in config["human_authorities"]
            and comment["user"]["login"] not in config["agent_accounts"]
            and permission in {"write", "maintain", "admin"})

def apply(state, comment, data, kind, config, permission):
    if data.get("assessed_commit") != state["assessed_commit"]:
        raise Invalid("Command revision is stale; inspect current head and resubmit")
    question = next((q for q in state["questions"] if q["id"] == data.get("question_id")), None)
    if question is None:
        raise Invalid("Unknown question ID; inspect Passport questions")
    is_human = human(comment, data, config, permission)
    if question["role"] == "human" and not is_human:
        raise Invalid("Human authority required; agent cannot resolve this question")
    now = comment["created_at"]
    if kind == "answer":
        if not all(github_url(url, state["repository"]) for url in data["evidence"]):
            raise Invalid("Evidence must use same-repository GitHub URLs; external URLs are not retrieved")
        answer = {"id": str(comment["id"]), "author": comment["user"]["login"], "url": comment["html_url"],
                  "received_at": now, "data": check("answer", redact_data(data))}
        state["answers"].append(answer)
        question["answer_ids"].append(answer["id"])
        question["status"] = "answered"
        question["resolution_reason"] = "Answer recorded; separate review must verify evidence"
        state["declarations"].append({"author": answer["author"], "text": answer["data"]["text"], "url": answer["url"]})
    else:
        action = data["action"]
        if action in {"accept-unresolved", "supersede", "close", "reassign-agent"} and not is_human:
            raise Invalid("This action requires configured human authority")
        if action == "close" and question["status"] not in {"answered", "resolved"}:
            raise Invalid("Cannot close without an answer for human verification")
        status = {"request-evidence": "open", "reassign-agent": "open", "escalate": "open",
                  "accept-unresolved": "accepted-unresolved", "supersede": "superseded",
                  "reopen": "open", "close": "resolved"}[action]
        question["status"] = status
        if action == "escalate":
            question["role"] = "human"
        if action == "reassign-agent":
            question["role"] = "agent"
        question["resolution_reason"] = ("Authorized human verification declaration: " if action == "close" else "")+redact(data["reason"])[:1000]+" (by "+comment["user"]["login"]+"; "+comment["html_url"]+")"
    question["updated_at"] = now
