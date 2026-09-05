# v0.1 implementation decisions

Historical scope record. Current integrated-product decisions are in
[v0.2 decisions](v0.2-decisions.md); the owner-approved v0.2 request supersedes
the manual-only implementation boundary below.

Scope authority: [epic #1](https://github.com/suyog19/software-signal-passport/issues/1)
and its implementation issues. Owner: Suyog Joshi.

## Source baseline

Inspected the latest default branches on 2026-09-05:

- [Software Signal at 584f704](https://github.com/suyog19/software-signal/tree/584f704ed84dc7d40d69a6dcd9fef6a6c69c2727):
  AGENTS, vision, thesis, principles, audience, Products and Business Architecture,
  Reliable Engineering, Review Readiness, Context Supply Chain and Process-as-Code,
  Passport, Business Rule Card, Architecture Drift Radar, Starter Kit, Gate and its
  product strategy, artifact status and current priorities.
- [Software Engineering Process 1.4.1](https://github.com/suyog19/software-engineering-process/tree/9f023d4bfd11552b17175698892efe6d9402e4f8):
  current default-branch version; no published GitHub release was available.

The locked owner request selects Software Signal Passport as the name and
Apache-2.0 as the license. These explicit product-specific terms override the
earlier concept label and generic commercial licensing options without changing
the Products work stream.

## Smallest usable distribution

Use Markdown templates and GitHub PRs. Preserve the existing canonical artifact
path and name its AI Change Passport history. No consumer runtime, CLI, scoring,
hosted app or Gate functionality. Development checks protect this distribution;
they do not evaluate consumer Passports or decide merges.

Core fields apply whenever a Passport is useful. Conditional detail accumulates
with consequence. A fourth, Standard API example makes all three depths visible;
the two money examples remain High-consequence despite their small diffs.

Manual copy/use and evidence inspection precede any product automation.
Fictional examples are teaching fixtures, not real-team validation. The release
change can exercise manual authoring; it cannot substitute for the five-change
human reviewer trial.

## Governance and publication boundary

Use the generic process profile, immutable process revision and solo-maintainer
mode. Bootstrap governance files and Actions are Protected changes. The canonical
process requires independent review and **manual owner merge/promotion**, even
when an agent has broad implementation authorization. A second human is optional.

Do not declare bootstrap workflows trusted by themselves. Initial repository
trust requires an owner-reviewed baseline; green structural checks are not
process readiness. Preserve this distinction in release evidence and status.

No portfolio reprioritization is intended: a small manual artifact fits the
existing lightweight Products trial priority. Update maturity after publication,
not merely after creating files.
