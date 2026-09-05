# Example Review Brief

Sanitized snapshot of real fixture PR #15, brief 6, after run 33962802283.
The embedded machine state is omitted here; the live comment and run artifact
retain structured state. This historical snapshot is not a current release verdict.

<!-- software-signal-passport:v1 -->
## Software Signal Passport

**advisory-with-open-questions** · High-consequence · advisory only

Assessed [9a387a3bddeb](https://github.com/suyog19/software-signal-passport/commit/9a387a3bddeb5b607982f54d57f3630a6fed79f6) · brief 6

**Intended outcome (declaration):** Exercise Passport questions on an isolated documentation fixture

**Depth:** Sensitive path: \.github/workflows/fixture\-checks\.yml; Sensitive path: \.github/workflows/fixture\-checks\.yml; Sensitive path: docs/dogfood\-input\.md; Sensitive path: docs/dogfood\-input\.md

**Accountable owner:** suyog19 \(owner named by task; no human decision recorded\)

**Context / rules (declaration):** Unknown: configured human authority is deliberately unavailable in this fixture\.

**Recovery (declaration):** Proposed: revert the fixture documentation commit; no data migration or production deployment is involved\. Recovery has not been rehearsed\.

**Verification observed:**
- [fixture: success](https://github.com/suyog19/software-signal-passport/pull/15/checks?check_run_id=101297027959)

**Unverified / uncertainty:**
- No customer behavior is tested\. Human authority remains unavailable\.
- Q\-rollback: answer received; substantive verification is not automated
- Q\-authority: open; Sensitive paths require human attention; ownership and approvals cannot be inferred
- Q\-business\_rules: open; Applicable repository field is missing
- Q\-rollback: answered; Applicable repository field is missing

**Questions for agent:**
- **Q-rollback** (answered): Provide rollback or explain its applicability with evidence\.

**Questions for human:**
- **Q-authority** (open): Which authorized human owns the sensitive change and its unresolved decisions?
- **Q-business_rules** (open): Provide business rules or explain its applicability with evidence\.

<details><summary>Evidence and protocol</summary>

Respond with /passport answer JSON or /passport action JSON. Use /passport refresh after checks finish.
Agent takeover uses this state, PR history and handoff; no session resume is assumed.

Separate review stage: separate\-deterministic\-stage/0\.2\.0.
No merge approval, certification or safety score is granted.

- [Dogfood: durable Passport clarification and stale revision](https://github.com/suyog19/software-signal-passport/pull/15)
- [\.github/workflows/fixture\-checks\.yml: added, \+24 \-0; signals: none detected](https://github.com/suyog19/software-signal-passport/blob/9a387a3bddeb5b607982f54d57f3630a6fed79f6/.github/workflows/fixture-checks.yml)
- [docs/dogfood\-input\.md: modified, \+4 \-1; signals: none detected](https://github.com/suyog19/software-signal-passport/blob/9a387a3bddeb5b607982f54d57f3630a6fed79f6/docs/dogfood-input.md)
- [fixture: success](https://github.com/suyog19/software-signal-passport/pull/15/checks?check_run_id=101297027959)
- [Observed publisher report: junit\.xml: JUnit \{&quot;errors&quot;: 0, &quot;failures&quot;: 0, &quot;skipped&quot;: 0, &quot;tests&quot;: 1\}](https://github.com/suyog19/software-signal-passport/actions/runs/33962619685/artifacts/9968401760)
- [PR body references issue \#13](https://github.com/suyog19/software-signal-passport/issues/13)

</details>

