# Human and coding-agent workflow

The installed [canonical policy](../passport/policy.md) is the procedure.
Codex and Claude adapters point to it instead of duplicating it.

## Human-written change

Open a draft PR describing intent. Passport observes its revision, files and
checks. For consequential work, submit a short handoff or answer specific gaps.
You need not manually write the Review Brief.

Read the assessed commit, advisory state, evidence and questions. Answer facts
with evidence links. Authority actions require configured role and permission.
A resolved question means its recorded resolution basis passed separate review;
it does not establish code correctness or approve merge.

## Agent-executed change

Read governance and configuration. Open a draft PR early, publish a validated
handoff and poll for review. Investigate technical questions and post
/passport answer with role agent and the assessed revision. Update code or
handoff when evidence exposes a defect. Poll until the response is consumed.
Leave human-authority gaps visible.

Use a body file with gh commands; never interpolate untrusted PR text into shell.
The agent's final report names the PR, current assessment and open questions.
PR creation is a collaboration checkpoint, not the end of work.

## Replacement agent

A fresh agent reads the issue, PR, current head, state, handoff and answer comments,
then investigates an agent-addressable question. It posts an attributable answer.
No private transcript, vendor callback or session-resume API is required.

## Reassessment and failures

New commits reopen previous questions and retain answers as history.
A publisher detecting a newer head publishes a stale brief and fails the run.
Use /passport refresh after checks complete. Check-completion-triggered
reassessment is not yet implemented.

A failed analysis leaves the prior revision-labelled comment untouched.
Actions is the operational status. A green run is not approval.
Maximum rounds and state capacity stop churn and expose actionable failures.
