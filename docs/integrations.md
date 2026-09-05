# Integration status

Current implementation status, not release certification:

| Integration | Status and limits |
| --- | --- |
| GitHub.com REST and Actions | Implemented; live end-to-end dogfood pending |
| Deterministic drafting and separate review | Fixture-tested, all four depths and answer convergence |
| OpenAI Responses | Implemented and contract-tested; live test pending |
| Codex-compatible AGENTS.md | Policy coherence tested; live lifecycle pending |
| Claude Code-compatible CLAUDE.md | Instruction adapter tested; Claude execution not exercised |
| Replacement-agent takeover | Durable protocol; live fresh-agent demonstration pending |
| Generated process guidance | Conflict preserved; automatic integration pending |
| Vendor resume/callback APIs | Not integrated |
| GitHub Enterprise, GitLab, Bitbucket | Unsupported |
| Hosted App, database, dashboards | Not implemented |

The protocol does not depend on an agent session. Protocol definition is not
proof of platform integration. Update release claims only after inspectable tests.
