# Example: paginate an internal catalog API

**Fictional example.** Lantern Tools, `catalog-api`, people, tickets, records
and results here are invented, not real evidence.

- **Identity:** PR 36 / CAT-64, snapshot `pagination-r2`; **Standard** because an
  internal non-sensitive API contract changes. Owner: Mira Chen, catalog lead.
- **Intent / scope:** Add optional `limit` and `cursor` to reduce large responses.
  Requests without either parameter retain existing behavior. No authentication,
  schema, or sensitive-data change.
- **Authority:** CAT-64 acceptance note revision 2 (2026-08-15), owner Mira;
  API decision ADR-8 revision 1. Rule: limit 1–100, default 25 only when pagination
  is requested; sort by immutable ID and reject malformed cursors.
- **Boundaries:** Additive response cursor; internal inventory client opts in.
  Concurrent inserts may appear on a later page; snapshot consistency is excluded.
- **Provenance:** Assistant drafted handler/tests; Mira corrected the default
  behavior and inspected old-client response fixtures.
- **Performed evidence:** Mira ran `pytest tests/test_catalog_pages.py` on
  `pagination-r2`, Python 3.12, SQLite fixtures, 2026-08-15.
  Record CAT-64/check-2: 18 passed covering empty/final pages, invalid cursor,
  min/max limits and unchanged old-client responses.
- **Unverified / uncertainty:** No production-volume benchmark. SQLite fixtures
  do not establish production query performance. Mira owns a proposed staging
  load check; it has not run.
- **Deployment / recovery:** Deploy with client opt-in disabled, run staging
  check, then enable the client. Mira will disable opt-in on query latency
  regression; old callers continue their existing path. No data migration.
- **Reviewer attention:** Confirm compatibility default and cursor ordering.
  Staging performance remains a rollout prerequisite; no approval is recorded.
