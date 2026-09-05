# Passport repository policy

Repository governance and domain authority outrank Passport defaults.
Passport is advisory and never grants merge, deployment or risk authority.

## Start and apply

Read .passport/config.json. Disabled means no Passport work. None depth needs no
handoff or questions; Light keeps ordinary PR intent and observed checks.
Standard and High-consequence changes use the workflow below. Sensitive paths
raise depth; small changes do not erase sensitive consequences.

## Coding-agent lifecycle

1. Read the task and repository requirements. Implement and run permitted checks.
2. Open a draft PR early enough to receive Passport feedback:
   `gh pr create --draft --title "Describe the change" --body-file pr.md`.
   PR creation is a reversible collaboration step, not task completion.
3. Submit a structured handoff using a PR comment beginning
   `/passport handoff` followed by JSON. Run
   `python -m passport validate handoff handoff.json` first.
   Include schema_version, assessed_commit, intent, participation, verification,
   business_rules, rollback, uncertainties. Link existing evidence; never author
   the full Passport manually.
4. Poll `gh pr view NUMBER --comments` and `gh pr checks NUMBER`, or use
   `python -m passport inspect --repo OWNER/REPO --pr NUMBER`.
5. Investigate agent questions. Respond with a comment beginning
   `/passport answer` followed by JSON containing question_id, assessed_commit,
   role ("agent"), text and evidence (a list of same-repository GitHub URLs).
6. Update code/handoff if required. New commits invalidate prior answers.
   Wait for reassessment, investigate remaining technical gaps, and leave
   unresolved authority questions visibly routed to the human owner.
7. Before finishing, report the PR, assessed revision, current advisory result
   and unresolved question IDs. Do not claim closure before Passport has consumed
   answers. Do not invent tests, business rules, inspection, approvals or certainty.

## Takeover and humans

A replacement agent reads the task, PR diff, canonical Passport comment, handoff,
answers and current commit. Use the same commands with its own attributable GitHub
account; identify the agent in participation. No vendor session resume is assumed.
Human contributors open the same draft PR and may use role "human" for factual
answers. Business intent, source authority, risk acceptance and deployment decisions
must come from configured human_authorities and must not be submitted by an agent
using a human's credentials. Owner names and GitHub permission never prove human
review occurred. Empty authority configuration leaves these questions open.

Use `/passport action` with question_id, assessed_commit, action, reason and role.
Actions: request-evidence, reassign-agent, escalate, accept-unresolved, supersede,
reopen, close. Authority-bearing actions require a configured human and role human.
Accept-unresolved preserves the gap; it is never merge approval.
See the versioned product protocol documentation for exact JSON examples.

## Failure and completion

The Actions run is the operational status. A failed run is not a passing Passport.
Review Brief freshness is tied to a commit. Use `/passport refresh` after checks
finish or an interrupted run. Maximum clarification rounds stops automated churn
and leaves open questions for maintainers. Never work around repository protections.
