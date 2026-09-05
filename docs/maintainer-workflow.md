# Maintainer workflow

This document governs this distribution's maintenance, not consumer repositories.
The [decisions](decisions.md) record scope and the canonical baseline.

## Work and checks

Use issue-first branches and PRs. Run:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Python 3.12+ suffices; these development checks have no third-party dependencies.
The local checker verifies required nonempty distribution files, version,
supported inline Markdown links and heading targets, and common secret/private
path patterns. It ignores fenced code/comments and external URL liveness.
It is not a full Markdown parser, secret scanner or truth validator.
Use ordinary inline links in maintained documents; review other link syntax
manually. Generated process files are validated by the canonical process.

For the same isolated tools as CI, build both development targets from
[checks.Dockerfile](../.github/checks.Dockerfile), using the commands in
[quality.yml](../.github/workflows/quality.yml). Run the Python target with
`scripts/validate.py` or `-m unittest discover -s tests -v`, and the Markdown
target with `**/*.md`, using the read-only mounts and network isolation shown
there. Builds target Linux amd64; native Python checks remain portable.
The configuration excludes unchanged generated guidance and allows long tables
and HTML comments. No development image is part of the consumer product.

The small image recipes remove unused package installers and apply exact
SHA-256-checked vendor security patches. Build steps run without network;
BuildKit fetches only digest-pinned images and the checksum-verified Alpine
packages named in the recipe. Review upstream availability and scan both resulting
images before release. A missing package or checksum mismatch must fail the build;
do not substitute an unverified download. See [dependency decisions](dependency-review.md).

Review external canonical/GitHub links before release with authorized read-only
GitHub access. Versioned self-links are checked against local files before the tag
exists and checked online after publication. Network outages and login-gated links
must not be falsely reported as missing files.

Actions run read-only source checks on PRs and main. Their successful result
means structural checks passed; it is **not** authenticated process readiness,
human approval, or proof of a consumer change's correctness. The generated process
validation workflow uses upstream action major tags as rendered by process 1.4.1;
repository-owned workflow actions, base images and patch content are pinned to immutable IDs.
Dependabot tracks GitHub Actions monthly; review image digests during maintenance.

## Execution and evidence

Implementation and local checks use a credential-free Docker container with
`--network none`, a read-only root, dropped capabilities and no privilege
escalation. Only the task checkout is writable for authoring; checks mount it
read-only. Docker's native network isolation enforces deny-all egress.
The host performs scoped Git/GitHub transport requested by the owner; production
promotion remains unavailable to the agent. Tool invocations and outputs are
recorded by the task host; CI retains run logs. Do not copy host paths or
credentials into source.

Classify and evaluate the full exact base/head diff, not a hand-picked path list.
Keep effective obligations and evidence outside committed source. Use the pinned
process's independent-review and other selected Skills. Store exact-revision
results in the review/run artifact store, not self-authenticating source JSON.
An edit after review requires fresh evidence for the new commit.

## Initial trust and solo-maintainer boundary

Process 1.4.1 says a target workflow cannot authorize itself. The empty initial
main branch is only a comparison baseline, not approved product or trusted CI.
The first governance PR needs the owner's manual bootstrap/trust decision and
manual merge. Do not label green lint/validation as `engineering-process`
readiness to evade that boundary.

Configure a main branch rule requiring PRs, passing quality checks, resolved
conversations, no force pushes/deletion and no bypass; zero required human
approvals supports solo maintenance. Independent fresh-context review remains
required separately. Branch protection is verified through GitHub settings/API
and reported with the PR; this document alone does not prove it exists.

Before subsequent protected work, establish approved trusted validation/review
workflow identities and exact-SHA evidence transport using the
[canonical reference flow](https://github.com/suyog19/software-engineering-process/blob/9f023d4bfd11552b17175698892efe6d9402e4f8/enforcement/github/reference-flow.md).
The generated workflow validates configuration only. Do not claim full process
readiness enforcement until the authenticated evidence join is installed and
tested from the owner-approved base.

## Repository self-hosting

This source repository keeps reusable orchestration pinned to merged commit
e83cb738d3149498f253fc2919a8a98c61a3d173 and selects runtime source using
github.workflow_sha, the immutable commit containing the trusted caller workflow.
For automatic PR/comment events that caller comes from the default branch;
manual dispatch requires a trusted maintainer-selected branch. It never selects
the assessed PR head or merge ref. This avoids an orphaned pre-squash runtime pin.

This is an intentional repository-owned customization of the installed caller.
The installer retains its original managed hash, so update/removal refuses to
overwrite the customization. Reconcile this caller deliberately during maintenance.
Consumer installations continue to pin both orchestration and runtime to the same
explicit reviewed upstream commit.

[GitHub's workflow context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
defines workflow_sha; [its security guidance](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
describes the default-branch trust boundary.

## Release

The [v0.2 release gate](release-gate.md) owns the integrated preview checklist.
The [dogfood record](dogfood.md) separates exercised behavior from remaining gates.

The owner must manually authorize and promote production under the locked
canonical process. A second human is not mandatory. Agents prepare reviewable
artifacts and commands; they must not perform the manual boundary on the owner's
behalf.

After exact-revision checks, independent review and the required bootstrap or
readiness decision, the owner merges. Revalidate the resulting main revision,
update the unreleased status/date through review, and prepare an annotated
`v0.2.0` tag at that verified revision. The owner publishes the tag and GitHub
Release using the prepared release notes. Never move a published version tag.

After publication, verify release/default-branch files, copied versioned links
and secret/private-path checks; then synchronize canonical Software Signal's
existing artifact page and maturity inventory in a focused reviewed PR. Keep
the historical artifact path and do not change portfolio priority without cause.
