# Software Signal Passport

Passport drafts an evidence-linked Review Brief for a GitHub pull request,
asks durable clarification questions, and incorporates attributable answers.
Developers correct gaps instead of manually writing the report.

**v0.2.0 — First Integrated Preview.**
Check [GitHub Releases](https://github.com/suyog19/software-signal-passport/releases)
for published versions; a source commit alone does not establish publication.
Controlled GitHub/Codex integration is tested; real-team usefulness is not yet validated.
[Installation](docs/installation.md) · [Workflow](docs/workflow.md) ·
[Protocol](docs/protocol.md) · [Configuration](docs/configuration.md) ·
[Example brief](docs/example-review-brief.md)

## Five-minute quick start

1. A maintainer installs policy, configuration and a GitHub workflow through a
   reviewed PR. Existing instructions and templates are preserved.
2. A human or coding agent opens a draft PR. Passport reads deterministic evidence:
   revisions, changed files, checks, policy, context and any implementation handoff.
3. Passport drafts structured state and a compact Review Brief automatically.
   A separate review stage checks evidence gaps and contradictions.
4. Agents investigate technical questions. Configured humans handle authority.
   Answers are PR comments with stable question IDs and evidence links.
5. Passport updates the brief and reviews again. New commits invalidate prior
   conclusions. Unanswered and accepted-unresolved questions remain visible.

The output is advisory. It never grants merge approval, certifies correctness,
scores developers or replaces repository governance. None and Light changes
avoid the Standard question set. Sensitive paths raise the configured depth.

## Install in a repository

Requires GitHub Actions and Python 3.12+ on the maintainer's computer.
The supported path is a reviewed source checkout and the built-in installer:

```sh
git clone https://github.com/suyog19/software-signal-passport
cd software-signal-passport
# Check out the reviewed release or exact revision first.
git rev-parse HEAD
python -m passport install --root ../your-repository --ref EXACT_40_CHARACTER_COMMIT --dry-run
python -m passport install --root ../your-repository --ref EXACT_40_CHARACTER_COMMIT
```

Review and merge the consumer installation using that repository's process.
See [installation](docs/installation.md) for permissions, generated-governance
adapters, model opt-in, updates and removal. No hosted service or database is used.

## Drafting and participation

Deterministic operation is the default and needs no model credential. Optional
OpenAI drafting and isolated model review use a customer credential and typed
outputs. Model statements stay labelled interpretations. Fork PRs use
deterministic mode; no PR code is executed.

The canonical policy describes Codex-compatible and Claude Code-compatible
instruction adapters, draft-PR handoff, polling and replacement-agent takeover.
[Supported integrations](docs/integrations.md) records tested status; an adapter
file alone is not proof that a platform works end to end.

## Version history

[v0.1.0](https://github.com/suyog19/software-signal-passport/releases/tag/v0.1.0)
is a **Concept Preview**: a manual prototype validating the initial information
model. First-user evaluation found manual authoring too burdensome for consistent
adoption. It is not recommended as a complete operational integration.
Its [templates](templates/software-signal-passport.md) and
[fictional examples](examples/README.md) remain useful teaching material.
The immutable v0.1.0 tag is preserved.

v0.2.0 targets repository integration, automatic drafting and the durable
clarification loop. See [changelog](CHANGELOG.md) and
[implementation decisions](docs/v0.2-decisions.md).
Publication and support claims depend on the actual release gate.

## Ownership and support

Apache-2.0. [Security](SECURITY.md) · [Threat model](docs/threat-model.md) ·
[Troubleshooting](docs/troubleshooting.md) · [Contributing](CONTRIBUTING.md).

[Software Signal](https://github.com/suyog19/software-signal/blob/main/artifacts/ai-change-passport.md)
owns the canonical concept. This repository owns the implementation.
Software Signal Gate remains a separate future workflow-decision product.
