# Software Signal Passport

**What does a reviewer need to know—beyond the diff—to evaluate this change responsibly?**

A copyable Markdown record of a change's intent, context, provenance, evidence,
uncertainty, and accountable ownership. For developers, reviewers, technical
leads, architects, and engineering managers, including teams using coding
assistants and agents.

**[Copy the Passport](templates/software-signal-passport.md)** ·
[PR section](templates/github-pr-passport.md) · [Examples](examples/README.md)

Reviewers often reconstruct the reason for a change across issues, policy,
architecture decisions, CI, and conversations. A Passport brings pointers to
that information to the pull request. It is advisory: completing one does not
establish correctness, safety, compliance, certification, or permission to merge.

## Five-minute quick start

1. Choose a consequential change. For a typo or another obvious trivial edit,
   use your usual PR description.
2. Copy the [PR section](templates/github-pr-passport.md) into its description.
   Choose Light, Standard, or High-consequence using the short guidance below.
3. Fill the core bullets with specifics. Link the requirement and actual evidence;
   write **Unknown** or **Not run** where information is missing.
4. Add only the conditional details the change needs. For more space, copy the
   [full template](templates/software-signal-passport.md) to
   `docs/passports/<issue-or-pr>.md` and link it from the PR.
5. Name the accountable human owner and the questions needing reviewer attention.
   After a new commit, refresh the revision and evidence before review.

Start with the [Light example](examples/low-risk-refactor.md).
No installation, account, model, or command execution is needed to use a Passport.

## Choose the depth

| Depth | Use for | What to include |
| --- | --- | --- |
| None | Trivial edits with obvious intent, no meaningful behavior or sensitive impact | Ordinary PR description; keep repository requirements |
| Light | Reversible, low-consequence changes | Core bullets; short evidence and uncertainty statements |
| Standard | Application logic, data, dependencies, interfaces, production configuration | Core plus relevant rules, boundaries, rollout and recovery |
| High-consequence | Authentication, authorization, payments, sensitive data, destructive migrations, safety-critical or regulated work | Standard plus authority, adverse-case evidence, specialist attention and explicit unresolved decisions |

Small diffs can have large consequences. Uncertain impact calls for investigation
and greater depth. More fields cannot make an unacceptable change safe.
[Choosing depth](docs/choosing-passport-depth.md) explains the accumulation rule.

Do not use a Passport to reproduce an existing adequate change record, collect
secrets, assess an agent brand, score developers, or replace experienced review.

## Install in a repository

For one PR, paste the [embedded section](templates/github-pr-passport.md).
For a team default:

1. Copy `templates/github-pr-passport.md` to your repository's
   `.github/PULL_REQUEST_TEMPLATE.md`.
2. If that file already exists, append the Passport section or map its bullets to
   equivalent existing fields. Preserve required checklists and governance.
3. Optionally copy the full template to `docs/passports/TEMPLATE.md`; authors
   copy it for individual consequential changes and link the file from their PR.
4. Commit the installation through your normal review process.

The distributed PR section uses absolute versioned links, so they still work
after copying. Use an embedded section for a short, single-PR change. Use a full
file when tables, retained evidence pointers, or several reviewers need a stable
record. Keep one authoritative Passport per change; the PR should link to the
file rather than maintain a second copy.

Passports can reference access-controlled evidence without making it public.
Confirm reviewers can access it, give its revision/date, and redact private
details. Never paste credentials, customer data, private transcripts, or raw
agent sessions.

## What is included

- [Core template](templates/software-signal-passport.md) and
  [GitHub PR template](templates/github-pr-passport.md).
- Completed, explicitly fictional
  [refactor, payment retry, refund eligibility, and API pagination examples](examples/README.md).
- Optional [drafting](prompts/draft-passport.md) and
  [review](prompts/review-passport.md) prompts; no model is required.
- [Team trial guide](docs/team-trial-guide.md) and
  [evaluation worksheet](docs/evaluation-worksheet.md).

## Try it with a team

Use about five representative historical or live changes. Record author effort,
reviewer time to understand, remaining reconstruction work, usefulness, ceremony,
and false confidence. Use the [trial guide](docs/team-trial-guide.md); share
sanitized findings in a [feedback issue](https://github.com/suyog19/software-signal-passport/issues/new).
A trial is learning evidence, not proof of product-market fit.

## Status and boundaries

Version **0.1.0**, the initial Markdown template distribution.
Consult [Releases](https://github.com/suyog19/software-signal-passport/releases)
for published versions. Free and openly usable under [Apache-2.0](LICENSE),
including team and commercial use under its terms.

This version has no runtime service, database, telemetry, scoring, automatic
approval, or enforcement of consumer PRs. Examples are fictional; real-team
benefit has not yet been established. Links and declarations can become stale,
and a completed form can create false confidence. Review source evidence and
reassess uncertainty when the change moves.

[Software Signal](https://github.com/suyog19/software-signal/blob/main/artifacts/ai-change-passport.md)
owns the canonical concept, originally called AI Change Passport. This repository
owns implementation and distribution. Software Signal Gate remains a separate
future product.

See [contributing](CONTRIBUTING.md), [support](SUPPORT.md),
[security](SECURITY.md), and the [changelog](CHANGELOG.md).
