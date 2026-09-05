# Troubleshooting

| Symptom | Action |
| --- | --- |
| No comment | Confirm installation, Actions and event; inspect workflow run |
| Config absent on base | Merge reviewed installation before assessing changes |
| Generated instructions conflict | Use the owning generator |
| Invalid or edited command | Validate JSON and submit a new comment |
| Human authority required | Ask the configured human; agents cannot impersonate |
| Evidence not verified | Link current observed checks/files; other links stay declarations |
| Stale assessment | Inspect current head, refresh and resubmit current answers |
| Model unavailable | Check opt-in, key, quota and timeout; deterministic evidence remains |
| GitHub API error | Inspect permissions/rate limits, then rerun |
| State/round capacity | Export history, split changes or deliberately review policy limits |
| Multiple canonical comments | Investigate provenance and reconcile |
| State changed during run | Rerun instead of overwriting |

Actions status remains visible when publication fails. A revision-labelled brief
does not prove the latest run succeeded. Model failure never converts missing
evidence into confidence. Local validation works without GitHub, but does not
establish live integration.

## Reusable workflow not found after squash merge

Verify that the pinned upstream commit remains reachable from its default branch
or a release tag. Restore the deleted reviewed source branch temporarily if needed,
then use the installer update command to pin the merged default-branch commit.
Review that diff. Do not replace an immutable pin with a moving branch name.
