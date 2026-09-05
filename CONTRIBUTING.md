# Contributing

Open a [focused issue](https://github.com/suyog19/software-signal-passport/issues/new)
with the problem, affected artifact, a sanitized example and desired improvement.
Small corrections can use a short issue. See the [code of conduct](CODE_OF_CONDUCT.md).

Use a `codex/<topic>` or `contrib/<topic>` branch and a pull request linked to its
issue. Preserve stable filenames and the canonical concept. Behavior, scope or
policy changes need evidence, not broad speculative redesign.

For content changes, review the rendered Markdown, copy a template into a sample
PR, check the three depth levels, and verify examples remain explicitly fictional.
Run the checks in [maintainer workflow](docs/maintainer-workflow.md). Custom
validation changes need negative-case tests. Keep generated engineering-process
files unchanged; use its init/upgrade/render flow.

A fresh implementation-independent reviewer evaluates the exact final revision.
New commits invalidate previous evidence. Fix material findings before merge.
The solo maintainer may perform the manual merge; a second human is not required.
An agent may prepare changes and review independently, but cannot perform the
canonical process's manual production promotion.

Contributions are under [Apache-2.0](LICENSE). Do not submit confidential evidence,
customer data or secrets. Prefer specific field improvements from a
[five-change trial](docs/team-trial-guide.md) over new automation.
