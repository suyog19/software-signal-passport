# Handoff and clarification protocol

Commands are new PR comments starting exactly with /passport. JSON follows on the
same or subsequent lines, without a Markdown code fence. Edited commands are
ignored; submit a new comment to preserve attributable history.

## Handoff

```text
/passport handoff
{"schema_version":1,"assessed_commit":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","intent":"Remove duplicate parsing","participation":"Codex implemented; no human inspection claimed","verification":[],"business_rules":"Unknown","rollback":"Revert; no data migration","uncertainties":["Production workload not tested"]}
```

Replace the illustrated revision with the real PR head. verification is a list
of claim/evidence objects; evidence is a GitHub URL list. Empty means no reported
run. Handoff fields are declarations; passing-test claims need observed results.
Latest valid current-revision handoff wins.

## Answer

```text
/passport answer
{"question_id":"Q-verification","assessed_commit":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","role":"agent","text":"Current unit check completed; integration coverage unknown","evidence":["https://github.com/OWNER/REPO/pull/1/checks?check_run_id=123"]}
```

Use real same-repository links. Passport never fetches arbitrary answer URLs.
Separate review verifies receipt of a current handoff and reevaluates current
check outcomes. Other technical and authority answers remain answered until
a configured human records verification or acceptance. Mere citation membership
never resolves a substantive claim.

Eligible contributors are the PR author, configured agent accounts or current
write/maintain/admin collaborators. Human-authority answers require the additional
configured human conditions. Bots never satisfy human authority.

## Actions

```text
/passport action
{"question_id":"Q-authority","assessed_commit":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","role":"human","action":"accept-unresolved","reason":"Describe the actual accountable decision and remaining gap"}
```

Never use an example to fabricate a decision. Actions: request-evidence,
reassign-agent, escalate, accept-unresolved, supersede, reopen and close.
Reassignment to agent, acceptance, supersession and closure require human authority.
Human-addressed questions require human authority for all actions and answers.
close requires an answered question and records an authorized human verification declaration. accept-unresolved keeps the gap visible.
reopen and request-evidence return it to open; escalate routes to human.

Each question records ID, text, trigger, reason, role, status, effect, timestamps,
answer IDs, resolution reason and assessed commit. Answers retain author, comment
link, timestamp, revision and evidence. New commits reopen questions without
rewriting old answers.

## State and retention

[State schema](../passport/schemas/state.json) versions the complete assessment.
One canonical github-actions bot comment contains the brief and hidden encoded
JSON. CLI inspect decodes it and compares live PR head. Encoding is not encryption.

Commands, comment history and Actions snapshots provide history. Artifacts expire
after 30 days; export them when longer retention is required. GitHub permissions
govern deletion. This is not a tamper-proof ledger.

Capacity: 300 files/comments, 100 questions/answers, 200 consumed command IDs,
64 KB rendered comment, 24 KB model input. Overflow fails visibly and preserves
previous state. No unresolved question is silently evicted. Readers reject
incompatible schema versions.
