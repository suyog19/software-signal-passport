# Choosing Passport depth

Use the consequence of being wrong, reversibility, uncertainty, and review
complexity. Agent use alone does not make a change high-consequence. Follow any
stronger repository or domain requirements.

1. Identify behavior, rules, boundaries, data and operational effects.
2. Choose the highest applicable level below. A tiny authorization edit can be
   High-consequence; a large generated formatting diff may need no Passport.
3. Explain the choice in one sentence. Investigate unknown impact; do not use
   Light merely because the diff is small.
4. Reassess when scope, evidence, or uncertainty changes.

| Level | Typical changes | Cumulative content |
| --- | --- | --- |
| None | Spelling, formatting, or an obvious trivial edit with no consequential effect | Existing PR description and required repository controls |
| Light | Reversible internal refactor without behavior, interface or sensitive impact | All core fields; a few specific sentences and one evidence bullet can suffice |
| Standard | Application logic, data, dependencies, interfaces, production configuration | Light plus applicable business rules, boundaries, deployment and recovery |
| High-consequence | Authentication, authorization, payments, sensitive data, destructive migrations, safety-critical or regulated work | Standard plus explicit applicability of every conditional area, authoritative rule ownership, adverse-case evidence, recovery limits and specialist decisions |

Core means identity/revision/depth, intent/scope/context, material provenance,
performed evidence, unverified areas/uncertainty, accountable human owner, and
reviewer attention. Short **None identified, because...** statements are useful;
do not pad the form.

For Standard, include a conditional field when it affects evaluation; delete
irrelevant prompts. For High-consequence, address each conditional area or give
a concrete reason it does not apply. Link applicable domain/security reviews,
negative scenarios and operational checks; retain **Not run** if evidence is
missing. The Passport does not prescribe or approve your organization's controls.

## Examples of proportional judgment

- Internal helper extraction with unchanged behavior and straightforward revert:
  Light. A spelling fix beside it can use None.
- Non-sensitive API pagination change: Standard, including contract compatibility,
  limits and consumer tests.
- Payment retry interval change: High-consequence because duplicate charges and
  financial state matter, even behind a feature flag.
- Refund eligibility preview: High-consequence if it influences entitlement or
  money. Read-only computation can still drive consequential decisions.

## When the record is insufficient

Missing authority, inaccessible evidence, conflicting policy, irreversible effects,
or unacceptable residual risk cannot be repaired by adding prose. Surface the
gap, name the decision owner and use the repository's normal escalation process.
An assigned owner is not evidence that they approved the change.

If another maintained change record already carries the information, link it and
fill only the gaps. Do not maintain competing copies. Never include secrets or
private customer data to make a Passport appear complete.
