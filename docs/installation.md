# Installation, update and removal

Use the source-checkout commands in the [README](../README.md). The installer
requires an exact reviewed 40-character upstream commit and prints a unified diff.
It does not commit, push, change branch rules or merge anything.
Use a commit retained by the upstream default branch or a release tag. A feature
commit can become unavailable to reusable-workflow resolution after squash merge
and branch deletion, even when the contents API still returns it. Update consumer
pins to the merged upstream commit before removing temporary source branches.

The installed files are:

- .passport/config.json: project-owned versioned configuration.
- .passport/POLICY.md: canonical human/agent procedure.
- .passport/install.json: managed content hashes for safe updates.
- .github/workflows/passport-review.yml: event integration pinned to the runtime.
- Small managed sections in AGENTS.md, CLAUDE.md and the standard PR template.

Existing files and instructions are not replaced. Conflicting managed content,
ambiguous markers, symlinks and unsafe paths fail before mutation. Fix conflicts
deliberately. The installer does not yet provide transactional recovery from
filesystem failure during a write; use a clean Git checkout for recovery.

## Generated governance

The installer refuses to edit generated AGENTS.md or CLAUDE.md. Their generator
owns those files. Add the canonical Passport policy as repository-owned local
context through that generator, preserving process controls. For Software Engineering Process, add .passport/POLICY.md to local_context and
run its reviewed upgrade/render workflow. Retry the installer: it detects the
existing canonical pointer and leaves the generated adapters untouched. Remove
that pointer through the generator before uninstalling Passport.

Repositories with hand-maintained instruction files use the installer directly.
Existing PR template content is retained. Repositories selecting a different
template must also link the policy in their selected contributor guidance.

## Permissions and secrets

The caller grants contents/read, issues/read, checks/read, actions/read and
pull-requests/write. The reusable workflow splits read-only analysis from the
publisher with PR-comment write permission. It never receives contents/write,
merge, administration or deployment permission. Actions must be enabled.

Deterministic mode needs only the workflow GITHUB_TOKEN. For optional model
assistance, configure model.enabled and add the PASSPORT_MODEL_KEY repository
secret using a customer-controlled OpenAI key. Provider/model are explicit.
No personal coding-agent credential is installed by Passport.

The consumer workflow listens to pull_request_target for metadata analysis only:
it checks out the pinned Passport runtime, never the consumer PR.
issue_comment processes new commands; dispatch permits manual reassessment.
Installation must exist on the trusted branch before events work.
Comment/dispatch availability depends on GitHub's default-branch rules.

## Update

Check out the next reviewed upstream revision. Use the same command with update
instead of install, first with --dry-run. Configuration customization is retained
and validated. Modified managed policy/workflow content causes an actionable
conflict rather than silent replacement.

## Remove

Use remove instead of install, first with --dry-run. Review and merge the removal.
Modified managed content is preserved by refusal and requires reconciliation.
Old PR comments, answers and run artifacts remain for history. Removing the
workflow does not erase evidence. Remove the model secret through normal
repository controls when no workflow needs it.

## v0.1 migration

Keep manual Passports as historical declarations tied to their original revision.
Do not reinterpret them as automatically verified evidence. The installer preserves
their PR-template content; maintainers can retire duplicate manual fields through
a reviewed edit once the automatic workflow works.
