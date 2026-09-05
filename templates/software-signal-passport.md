# Software Signal Passport

<!-- v0.1.0. Copy this file for one change. Core sections are required whenever
you use a Passport. Keep Light short; include conditional sections only when
relevant. Standard adds applicable conditional sections; High-consequence makes
their applicability explicit. Unknown is not the same as not applicable.
A completed Passport is evidence for judgment, not proof or merge approval. -->

## Change identity — core

- Change: <title and PR/issue link>
- Assessed revision: <commit or precise diff/version; refresh after changes>
- Depth and reason: <Light / Standard / High-consequence; consequence/reversibility>
- Accountable human owner: <name/handle and role; ownership is not an approval>

## Intent, scope and context — core

- Need and expected outcome: <why; observable outcome>
- Scope and exclusions: <what changes; what deliberately does not>
- Authority and context: <requirement/decision/source links with revision/date;
  distinguish authoritative source from supporting example or assumption>

## Provenance — core

- Material participation: <what humans, assistants, agents or automation
  generated, transformed, checked or decided; name artifacts, not percentages>
- Human inspection and decisions: <what was actually inspected, changed or
  accepted; say when inspection has not happened>

## Verification and inspectable evidence — core

| Performed check | Revision / environment | Actual result and inspectable evidence | Supports / limits |
| --- | --- | --- | --- |
| <command or manual procedure, executor and date> | <revision, fixtures/environment> | <pass/fail, counts if known, stable log/report link> | <claim supported and coverage limits> |

If nothing ran, say **Not run** and why. A proposed test is not performed evidence.

- Unverified areas: <not run, unavailable, skipped, failing, or stale evidence>
- Assumptions and uncertainty: <claim; basis; unresolved question and owner>
- Proposed follow-up: <not yet performed; who will resolve it and when>

## Reviewer attention — core

- Requested attention: <specific questions and why they matter>
- Decisions/approvals still needed: <who has authority; status and evidence if
  actually recorded; never infer approval from authorship or ownership>

## Business rules — conditional

<Include when domain behavior depends on rules. Link the authority and its
revision/effective date, name its owner, and state relevant thresholds,
exceptions and conflict/missing-source questions. Do not duplicate full policy.>

## Boundaries and sensitive areas — conditional

<Include affected modules/services, interfaces, dependencies, data ownership,
privacy/security areas, and compatibility constraints. Say whether the boundary
changes or only its implementation changes. Link governing decisions.>

## Deployment and recovery — conditional

- Deployment: <activation, prerequisites, monitoring, staged rollout, operator>
- Rollback/recovery: <reversal procedure, trigger, operator and recovery limits;
  distinguish code rollback from irreversible business/data effects>
- Outstanding checks: <plans, rehearsal gaps and required decisions>

For High-consequence work, explicitly address rules, boundaries, deployment and
recovery or explain non-applicability. Link adverse-case/security evidence and
needed domain/specialist decisions. More complete documentation cannot substitute
for missing authority, evidence, or a viable recovery plan.
