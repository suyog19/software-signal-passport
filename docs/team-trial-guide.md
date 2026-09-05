# Run a small team trial

Choose approximately five representative changes with an author and an
experienced reviewer. Aim for one trivial candidate, one Light refactor, two
Standard changes (for example logic and an interface), and one consequential
domain change. Use historical changes if a live high-consequence change is not
available. Do not create risk to fill the sample.

1. Select changes before seeing whether the Passport helps. Include an awkward
   case with missing context; avoid only choosing successful examples.
2. For historical work, use information available at review time. Record later
   knowledge separately; do not backfill the Passport with the eventual outcome.
3. Record the author's preparation time. Use existing issue and evidence links;
   do not manufacture evidence to fill a field. For the trivial candidate, test
   whether an ordinary PR description is sufficient.
4. Ask a reviewer to time their first meaningful understanding: can they explain
   intent, relevant rules/boundaries, evidence, gaps and owner? Record remaining
   reconstruction effort and the sources consulted.
5. Compare with the existing workflow on comparable changes. Where two reviewers
   are available, alternate which receives the Passport first. With one reviewer,
   acknowledge recall/order bias; do not portray before/after timing as causal.
6. Complete one [evaluation worksheet](evaluation-worksheet.md) per change.
   For a live PR, observe whether attention actually changed. Do not treat the
   Passport or this trial as an alternative to normal review and release controls.
7. Discuss all five results, including neutral and negative experiences. Keep
   fields that helped, shorten noisy ones, and identify missing authoritative
   context in its owning system.

Compare usefulness, time to understand, remaining reconstruction, author cost,
irrelevant fields, and false confidence together. Faster review alone is not a
success if important uncertainty becomes less visible.

Publish only sanitized feedback with the template version, depths tried and
specific improvements. Do not collect customer data, raw agent transcripts or
private evidence in this public repository. Use [feedback issues](https://github.com/suyog19/software-signal-passport/issues/new).

Decide whether to keep using, adapt, or stop using the template for each change
class. Five changes cannot establish product-market fit, causal risk reduction or
general safety. Real usage should guide template refinements before automation.
