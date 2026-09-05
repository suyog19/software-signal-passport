# Security and threat model

Assets: repository token, optional model key, trusted policy, revision-bound
evidence, human authority and comment history. Threats include forks, malicious
contributors, injected content, forged comments, model output and concurrency.

| Threat | Enforced control and limitation |
| --- | --- |
| PR code accesses secrets | No PR checkout/build/execution; pinned runtime only |
| Model gains write authority | Separate analysis/publication jobs; model has no tools |
| Fork causes provider calls | Provider disabled for forks |
| Comment injection | Strict JSON parsing; no eval or shell construction |
| Forged state | Canonical bot author, schema and PR identity checked |
| Malformed output | Strict schemas, bounded JSON and duplicate-key rejection |
| Prompt injection changes authority | Models populate interpretation only; deterministic lifecycle owns decisions |
| Unauthorized acceptance | Explicit human accounts, role, account type and permission |
| Traversal/SSRF | Scoped API paths, fixed API hosts, redirect refusal and safe context paths |
| Secret disclosure | No token/response logging, common-token redaction, no raw transcripts |
| Stale overwrite | Head recheck, prior-state digest and per-PR concurrency |
| Duplicate loops | Command prefix filtering and assessment digest |
| Unbounded activity | Timeouts, limited GET retries, no blind write retry, bounded state/rounds |

A role declaration does not cryptographically establish human identity. Agents
using delegated human credentials must never impersonate authority. Dedicated
agent accounts and repository governance remain necessary.

Administrators and trusted workflows can alter bot comments or remove artifacts.
Storage is not tamper-proof. No external evidence URL is dereferenced. Context
comes from permitted trusted-base files. Model use is opt-in. Redaction is defense
in depth, not a complete detector; never supply secrets or private transcripts.

Publisher permissions permit PR-comment writes, not source/branch/merge/deployment.
Actions use immutable pins. Customer policy outranks defaults.

Sources: [GitHub privileged-event security](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
and [OpenAI typed outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
Schema conformance is not proof of factual correctness.
