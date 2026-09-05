# Integration status

Current implementation status, not release certification:

| Integration | Status and limits |
| --- | --- |
| GitHub.com REST and Actions | Live dispatch, publication, answer update and stale-revision dogfood passed; automatic default-branch events pending |
| Deterministic drafting and separate review | Fixture-tested, all four depths and answer convergence |
| OpenAI Responses | Two real schema-validated draft/review calls passed with synthetic evidence and restricted egress |
| Codex-compatible AGENTS.md | Live Codex handoff, polling and agent answer exercised on controlled PR #15 |
| Claude Code-compatible CLAUDE.md | Instruction adapter tested; Claude execution not exercised |
| Replacement-agent takeover | Fresh-context agent investigated and answered Q-rollback on PR #15 |
| Generated process guidance | Owning generator adds policy pointer; installer preserves generated files |
| Vendor resume/callback APIs | Not integrated |
| GitHub Enterprise, GitLab, Bitbucket | Unsupported |
| Hosted App, database, dashboards | Not implemented |

The protocol does not depend on an agent session. Protocol definition is not
proof of platform integration. Update release claims only after inspectable tests.
