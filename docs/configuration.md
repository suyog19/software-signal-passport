# Configuration reference

The authoritative [JSON schema](../passport/schemas/config.json) is version 1.
Validate with `python -m passport validate config .passport/config.json`.
Unknown fields, unsupported versions, invalid types and out-of-range limits fail.

| Field | Meaning |
| --- | --- |
| schema_version | 1; incompatible versions fail closed |
| enabled | Disable assessment |
| mode | advisory only |
| change_classes | Named path-glob classes with None, Light, Standard or High-consequence depth; highest match wins |
| default_depth | Unmatched paths; Standard by default |
| sensitive_paths | Raise matching current or renamed paths to High-consequence |
| owners | Path lists mapped to owner/escalation labels; not an approval |
| human_authorities | GitHub logins eligible for authority declarations; empty by default |
| agent_accounts | Agent logins; cannot make human-authority decisions |
| state_location | pr-comment |
| model | enabled, provider, model and timeout_seconds (5–60); OpenAI adapter |
| routing | Technical to agent; authority to human |
| evidence_sources | pr and files required; checks, context and handoff optional |
| context_paths | Up to 20 permitted small files from trusted base |
| required_fields | participation, verification, business_rules, rollback |
| max_rounds | 1–30 accepted clarification commands per head revision |

[Defaults](../passport/defaults.py) do not understand every organization's risk.
Review path rules. Python fnmatch patterns are case-sensitive. Documentation
defaults to Light; text files to None. Sensitive renamed paths retain depth.

Model context includes permitted evidence, configured context files and handoff.
Arbitrary issue links and answer URLs are not retrieved. No provider is used for
None, Light or fork PRs.

Authority requires role human, GitHub User account, listed human authority,
not a configured agent account, and current write/maintain/admin permission.
GitHub cannot prove whether a human or agent typed a comment using a human's
credential. Never falsely declare role human; dedicated agent accounts provide
stronger separation. This limitation is explicit, not assurance.
