# JSON output

For automation, dashboards and CI, a scan can emit one JSON document per target instead of (or in addition to) the PDFs. By default JSON scans are passive-only unless an active mode is chosen explicitly.

## Top-level fields

| Field | Type | Description |
|---|---|---|
| `version` | string | Engine version, e.g. `5.5.3` |
| `target` | string | Normalized domain |
| `timestamp` | string | UTC, ISO 8601 |
| `scan_id` | string | Identifies this assessment (printed in every PDF footer) |
| `mode` | string | `passive` or `active` |
| `scan_profile` | string | `2m`, `6m` or `12m` |
| `scan_duration_ms` | integer | Wall-clock duration |
| `overall_score` | integer | 0–100, higher is better ([methodology](methodology.md)) |
| `vector_scores` | object | Per-vector scores used by the radar chart; a vector that could not be assessed is `null` |
| `risk_summary` | object | Counts per priority P0–P4 and aggregate risk |
| `finding_count` | integer | Number of findings |
| `findings` | array | The findings, see below |
| `finding_deltas` | object | `new`, `resolved`, `unchanged` fingerprints versus the previous scan |
| `module_status` | object | Module id → `COMPLETED` / `SKIPPED` / `TIMEOUT` / `FAILED` |
| `coverage` | array | One entry per check: status, detail, confidence, limitation |
| `coverage_summary` | object | Totals of the above |
| `check_registry` | array | Every registered check with its level (passive / active) |
| `attack_surface` | object | Discovered endpoints, parameters, scripts, APIs, WebSocket URLs, OpenAPI documents, endpoint graph |
| `active_tier_stats` | object or `null` | Parameters, forms and tests executed / skipped / timed out. `null` for passive scans |
| `resource_profile` | object | The ceilings and budgets this scan ran with |
| `resource_events` | array | Budget and adaptive-scaling events |
| `complexity_score`, `complexity_factors`, `adaptive_stage` | | How the target's size affected effort |
| `limitations` | array | Human-readable limitations collected from coverage |

On an invalid or blocked target the document contains `error` and empty `module_status` / `coverage`.

## Finding object

| Field | Description |
|---|---|
| `finding_id`, `fingerprint` | Stable identifiers; the fingerprint is what scan-to-scan comparison uses |
| `title`, `impact`, `fix` | Human-readable text |
| `cvss`, `vector` | CVSS 3.1 base score and vector (the score is always recomputed from the vector) |
| `severity` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` (the CVSS band) |
| `priority`, `risk_score` | P0–P4 urgency and the 0–100 value behind it |
| `confidence`, `verification_state` | How sure the tool is, and what kind of observation it is |
| `evidence` | Array of short observations |
| `cwe`, `owasp`, `wstg`, `asvs`, `cve` | Standards tags. `cve` is only set from a note pointing to NVD / OSV |
| `affected_asset`, `affected_endpoint` | Where |
| `category` | Risk category used by the score |
| `scan_level` | `passive` or `active` |
| `detection_source` | Module that produced it |
| `limitations` | What the check cannot establish |
| `status`, `remediation_effort` | Workflow hints |

## Stability

New fields may be added in later releases, so consumers should ignore fields they do not know. A change to the scoring maths bumps the *score model*, so history is never compared across incompatible models.
