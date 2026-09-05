# Example: extract an internal formatting helper

**Fictional example.** All names, records and results below are illustrative;
no command here was run against a real system.

- **Change / revision / depth:** Lantern Tools, `console-utils`, PR 18 / TASK-41;
  fictional snapshot `refactor-r2`; **Light**, an internal helper extraction with
  no behavior or interface change and a single-commit revert.
- **Accountable human owner:** Mira Chen, tools maintainer.
- **Intent and scope:** Remove duplicate duration formatting in two internal
  report renderers. Output strings, rounding, public API and dependencies stay
  unchanged; no business rule or sensitive boundary is affected.
- **Authority and context:** TASK-41 acceptance note, revision 1 (2026-08-12),
  owned by Mira: “Both reports must preserve byte-for-byte output for existing
  fixtures.” Existing golden fixtures are supporting behavior evidence.
- **Material participation:** A coding assistant proposed helper extraction and
  replaced the two callers. Mira compared both caller diffs and rewrote the
  zero-duration case; she inspected the golden-output diff, not every test file.
- **Performed verification:** In the fictional scenario, Mira ran
  `python -m unittest tests.test_duration tests.test_reports` on
  `refactor-r2`, Python 3.12, local fixtures, 2026-08-12.
  Evidence record `TASK-41/check-2`: 14 tests, 0 failures; both report snapshots
  unchanged. Covers zero, subsecond, rounded minute and hour cases.
- **Unverified / uncertain:** No performance benchmark; output equivalence for
  inputs outside fixtures is inferred from the unchanged expression, not proven.
  Mira owns any follow-up if review finds another input class.
- **Reviewer attention:** Check helper visibility and the preserved rounding
  expression. No specialist decision requested; PR approval is not yet recorded.
