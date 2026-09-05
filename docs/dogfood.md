# Controlled end-to-end demonstration

[Dogfood PR #15](https://github.com/suyog19/software-signal-passport/pull/15)
is an isolated fixture branch in the implementation repository, not a production
change and not intended for merge into main.

## Executed on 2026-09-05

- Installer dry-run and installation preserved existing AGENTS.md, CLAUDE.md and
  the root PR template. No competing .github template shadowed it.
- Codex read the installed policy and opened a draft PR before ending its session.
- The first handoff was deliberately omitted. A real GitHub Actions dispatch
  [collected/drafted/reviewed/published](https://github.com/suyog19/software-signal-passport/actions/runs/33962412733)
  one canonical brief with Q-handoff and separate human-authority questions.
- Codex submitted a [structured handoff](https://github.com/suyog19/software-signal-passport/pull/15#issuecomment-5551349154)
  and [role-agent answer](https://github.com/suyog19/software-signal-passport/pull/15#issuecomment-5551349263).
  [Reassessment](https://github.com/suyog19/software-signal-passport/actions/runs/33962451979)
  recorded attribution and resolved handoff receipt.
- A new commit reopened questions, preserved prior answers and identified the old
  assessment as stale. A fresh independent agent read GitHub history and supplied
  a [recovery investigation](https://github.com/suyog19/software-signal-passport/pull/15#issuecomment-5551361724).
  It identified that reverting only the latest commit would leave the first edit.
- A further commit added a real, read-only fixture check. Its
  [successful run](https://github.com/suyog19/software-signal-passport/actions/runs/33962619685)
  produced a JUnit report for one performed documentation assertion.
- The updated runtime [collected the actual report](https://github.com/suyog19/software-signal-passport/actions/runs/33962677935),
  parsed one test with zero failures/errors/skips, observed check success and
  reassessed the new revision. This is fixture evidence, not product correctness.
- Codex supplied the [current handoff](https://github.com/suyog19/software-signal-passport/pull/15#issuecomment-5551378985).
  A fresh agent also [reassessed recovery at the new head](https://github.com/suyog19/software-signal-passport/pull/15#issuecomment-5551380338).
  Human authorities remain deliberately unconfigured. No human approval or risk
  acceptance is fabricated.

[Final reassessment](https://github.com/suyog19/software-signal-passport/actions/runs/33962802283)
published brief 6: handoff receipt and current checks resolved; recovery answered
but unverified; human authority and business rules open. See the
[sanitized Review Brief](example-review-brief.md).

The tested advisory result retains open human questions and unverified recovery.
A technical answer citing a URL does not automatically establish its truth.

## Real model adapter test

The OpenAI Responses adapter made two real calls with gpt-5.4-mini: one draft and
one isolated review. Both outputs passed the typed schema. Input was synthetic
fixture evidence only; no repository/private transcript was sent. The test
container used an internal Docker network and a separate CONNECT proxy limited
to api.openai.com:443. The key was supplied only to that test process, never stored
in GitHub or source. Both temporary network resources were removed afterward.

This is local author-supplied test evidence retained in the task audit. It does
not establish model factual accuracy, provider availability for other accounts
or production assurance. Provider source was exercised at candidate 8b591539f804f832a30b82d02fb8723fd083cd72.

## Automatic default-branch events after owner merge

The owner merged implementation PR #14 at e83cb738d3149498f253fc2919a8a98c61a3d173
and canonical PR #59 at c892f5de40695bef828ab0bbcd1d70825d030d30.

[Controlled PR #16](https://github.com/suyog19/software-signal-passport/pull/16)
was opened against the installed default branch, with a harmless Markdown file
under a sensitive path. The initial run exposed an orphaned reusable-workflow
pin after squash merge and branch deletion. Restoring the reviewed source branch
allowed GitHub to resolve the same immutable code. The release preparation pins
orchestration to merged main and runs this source repository from its trusted
workflow commit; consumer installations retain explicit upstream pins.

- [Automatic PR assessment](https://github.com/suyog19/software-signal-passport/actions/runs/33963394890)
  collected evidence, drafted/reviewed state and published a single canonical brief.
- [Automatic comment assessment](https://github.com/suyog19/software-signal-passport/actions/runs/33963434176)
  consumed the handoff and agent recovery answer; handoff receipt resolved,
  recovery remained answered/unverified, and human-authority questions stayed open.
- A new commit bc50c7c00c39e496d4cecf7966a445475f3d7dc7 made the old assessment stale.
  [Automatic synchronize assessment](https://github.com/suyog19/software-signal-passport/actions/runs/33963470210)
  recorded the previous commit, reopened questions and retained previous answers.
- The agent submitted a [current handoff](https://github.com/suyog19/software-signal-passport/pull/16#issuecomment-5551463747)
  and [current answer](https://github.com/suyog19/software-signal-passport/pull/16#issuecomment-5551464065).
  [Automatic reassessment](https://github.com/suyog19/software-signal-passport/actions/runs/33963528227)
  consumed these responses. Human authority and business-rule questions remain
  deliberately unresolved, while technical recovery is answered but unverified.
- [Release preparation PR #17](https://github.com/suyog19/software-signal-passport/pull/17)
  also received automatic assessment on its opened event.

The fixture is not intended for merge. Its assertions do not validate customer
behavior or production recovery. Owner publication and released-state verification
are recorded separately in [release issue #13](https://github.com/suyog19/software-signal-passport/issues/13).

No real-team time/effort study, Claude Code execution, GitHub Enterprise support,
vendor resume API or production readiness is claimed.
