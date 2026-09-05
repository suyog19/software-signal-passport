# Example: retry transient payment failures

**Fictional example.** Northstar Shop, its people, repo `billing-worker`,
tickets, policies, snapshots, logs and checks are invented. Inline evidence is
an illustrative record, not a real test execution.

## Change identity

PR 72 / PAY-208; fictional assessed snapshot `retry-r4`.
**High-consequence:** payment retries can duplicate a charge or lose a retry.
Accountable human owner: Arun Rao, payments lead. Ownership does not imply merge
or rollout approval.

## Intent, scope and authority

Retry known transient failures at 30 seconds and 2 minutes after the initial
attempt, instead of immediately exhausting the retry budget. Scope is the worker
scheduler; no change to charged amount, provider account, or refund behavior.

Authority: PAY-208 acceptance note revision 3, confirmed 2026-08-14 by policy
owner Lena Ortiz; payments ADR-12 revision 2 owns idempotency. Relevant excerpts:

- At most three total attempts, including the initial attempt.
- Retry only explicit transient responses; permanent declines stop.
- A timeout with unknown charge outcome enters reconciliation; do not blindly retry.
- Reuse the order payment idempotency key across all attempts.

These excerpts are teaching context. A real Passport would link the maintained
policy and ADR instead of creating another authority.

## Boundaries and provenance

Touches worker scheduling, persisted attempt count and the provider adapter.
The existing unique key and atomic attempt reservation remain the concurrency
boundary. No schema change; payment identifiers remain in restricted logs.
Do not expose customer details in a public Passport.

An agent drafted scheduler changes and transient-response fixtures. Arun rejected
its proposal to retry every timeout, implemented reconciliation routing, and
inspected the transaction and key-reuse paths. The agent generated additional
concurrent-delivery tests; Arun compared expected outcomes with ADR-12.

## Performed verification and evidence

All entries below are simulated performed checks on `retry-r4`, Python 3.12,
isolated Postgres fixtures and a fake provider, run by Arun on 2026-08-14.

| Evidence record / procedure | Recorded result | What it establishes and does not |
| --- | --- | --- |
| PAY-208/unit-4: `pytest tests/test_retry_schedule.py` | 12 passed | Fake-clock delays, three-attempt ceiling, permanent-decline stop |
| PAY-208/integration-4: `pytest tests/test_retry_worker.py` | 8 passed | Persisted count; duplicate queue delivery creates one reservation |
| PAY-208/negative-4: `pytest tests/test_unknown_outcome.py` | 5 passed | Timeout goes to reconciliation; no automatic second charge request |
| PAY-208/key-review-4: compare adapter requests across attempts | Same key in three captured fake requests | Local adapter behavior; not provider-side idempotency |

## Unverified areas and uncertainty

Provider sandbox behavior has **not been verified**. The fake provider cannot
establish key-retention behavior during delayed redelivery. Restricted provider
contract PROV-7, revision 1, states 24-hour retention; its freshness is unconfirmed.
Arun must confirm the current contract and perform the delayed-delivery sandbox
check before enabling retries. These are proposed checks, not passing evidence.

Assumption: the queue's maximum redelivery age remains 6 hours. The configured
value was inspected in `retry-r4`; production drift was not checked.
The concurrency tests cover two workers, not arbitrary production load.

## Deployment and recovery

Proposed: deploy disabled, reconcile outstanding unknown outcomes, then enable
for a small controlled cohort after provider verification and Lena's recorded
risk decision. Operator: Arun. Monitor duplicate-request alarms and reconciliation
backlog; pause activation on any duplicate charge or unexpected backlog increase.

Recovery: disable the flag to stop new retry scheduling, quarantine pending retries
and reconcile them by payment key before requeueing. Revert the worker only after
in-flight tasks drain. Code rollback cannot undo a charge; use the existing
authorized reconciliation/refund process. Recovery rehearsal is **not performed**.

## Reviewer attention

Payments reviewer: inspect atomic reservation and idempotency across queue
redelivery. Operations reviewer: assess pause/drain/reconciliation procedure.
Lena's rollout decision, provider check and recovery rehearsal remain pending.
This Passport is complete as a record of current knowledge; the rollout is not ready.
