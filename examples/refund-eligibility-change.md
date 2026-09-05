# Example: correct refund eligibility

**Fictional example.** Northstar Shop, `orders-service`, people, tickets, policy,
snapshots and results are invented. The records below illustrate evidence format;
they are not real checks or approvals.

## Change identity

PR 91 / REF-310; fictional snapshot `refund-r3`.
**High-consequence:** eligibility changes can affect customer entitlements and money.
Accountable human owner: Elena Park, orders lead.

## Intent, scope and authoritative business rules

Bring the full-order eligibility preview into line with Support Policy RP-6,
revision 5, effective 2026-08-20. The current implementation incorrectly denies
damaged-item exceptions after 30 days. Policy owner: Nia Desai, support operations.

The fictional authority record REF-310/policy-5 identifies these rules:

- At or before 30 elapsed days from delivery, a full-order claim may proceed through
  ordinary eligibility checks.
- After 30 days, manager approval is required unless the item arrived damaged.
- The damaged-item exception removes the age-based manager requirement only;
  it does not bypass identity, prior-refund, or fraud checks.
- Elapsed time uses UTC instants; 30 days exactly is in the ordinary window.

Scope: the full-order preview decision and reason code. Issuing a refund, manager
authorization, and payment ownership are excluded. Partial refunds are excluded
because the policy's damaged-item allocation is not specified. Existing
partial-refund behavior is unchanged, not declared correct.

## Boundaries and machine participation

Orders owns the preview. The existing payments API supplies prior-refund status;
no direct payments database access is introduced. The reason-code enumeration gains
`DAMAGED_AGE_EXCEPTION`; support clients must accept that value. Authorization
checks remain mandatory even though this endpoint does not move funds.

An assistant drafted the rule function and boundary tests from RP-6 revision 5.
Elena changed a draft comparison from calendar dates to elapsed UTC time and
restored fraud checks that the draft exception had skipped. She inspected the
decision table, API diff and test assertions. An agent proposed partial-refund
tests; Elena did not implement guessed policy.

## Performed verification and inspectable evidence

Fictional checks executed by Elena on 2026-08-21, `refund-r3`, Node 22,
local fixtures with a stub payments API:

| Evidence record / procedure | Actual result in the example | Coverage / limit |
| --- | --- | --- |
| REF-310/unit-3: `npm test -- refund-eligibility` | 22 passed | Before/at/after 30 days; damaged exception; approved/unapproved manager paths |
| REF-310/security-3: `npm test -- refund-authorization` | 9 passed | Unauthenticated/cross-customer denied; fraud and prior-refund checks retained |
| REF-310/contract-3: `npm test -- refund-preview-contract` | 6 passed | New reason code and existing response fields against stub contract |
| REF-310/table-review-3: compare eight policy decision rows | All eight matched | Elena's manual policy comparison; not Nia's approval |

## Unverified areas and uncertainty

Support-client compatibility has **not been checked** against the deployed client.
Nia has not decided partial-refund handling; REF-311 tracks that question.
No live provider or production customer data was used.

Assumption: support staff will interpret the new reason code correctly. That is
untested. Proposed follow-up: Elena checks deployed-client compatibility; Nia
reviews the wording and owns the policy decision. Proposed work is not evidence.

## Deployment and recovery

Proposed: keep the new decision behind a flag; verify support-client compatibility
before enabling it for full-order previews. Elena operates the flag; Nia decides
policy activation after inspecting the exact decision table. Neither activation
decision nor support-flow walkthrough is recorded yet.

Monitor preview reason counts and support escalations. Disable the flag if the
client cannot handle the reason code or eligibility mismatches appear; Elena owns
rollback. Reverting restores the old, known-wrong damaged-item behavior, so support
must route affected claims to manual policy review. Previously communicated
eligibility decisions cannot be erased by code rollback. Recovery is documented,
not rehearsed.

## Reviewer attention

Inspect age boundary, the limited exception, retained authorization/fraud checks
and API compatibility. Ask Nia to resolve partial-refund authority separately
without expanding this PR by assumption. Full-order activation awaits the client
check and policy-owner decision. Ownership alone is not approval.
