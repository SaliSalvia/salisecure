# Overview

SaliSecure assesses the externally visible security posture of a website. It does not need an agent, an account on the target, or access to source code. It looks at the site the way a careful outsider would, and reports what that outsider could learn or reach.

## How an assessment runs

```
 target domain
      │
      ▼
 1. Target safety check      Resolve the name; refuse private / internal addresses
      │
      ▼
 2. Scan profile             2 / 6 / 12 minute ceiling and budgets
      │
      ▼
 3. Passive modules (20)     DNS, TLS, headers, discovery, intelligence
      │
      ▼
 4. Active modules (19)      Only in passive + active scans; bounded probes
      │
      ▼
 5. Correlation              De-duplicate and merge related findings
      │
      ▼
 6. Scoring                  CVSS 3.1, confidence, priority P0–P4, 0–100 score
      │
      ▼
 7. History / delta          Compare with the previous scan of the same target
      │
      ▼
 8. Reports                  Technical PDF, executive PDF, optional JSON
```

### 1. Target safety check

Before anything else, the target is resolved and validated. Targets that resolve to private, loopback, link-local or otherwise non-public addresses are refused, and redirects are checked the same way. This prevents SaliSecure from being pointed at internal infrastructure.

### 2. Budgets and deadline

Every scan runs inside a hard wall-clock deadline and hard budgets for HTTP requests, DNS queries and response bytes. When a budget is exhausted or the deadline is reached, the remaining checks are marked *skipped* or *timeout* and listed in the report. See [scan profiles](scan-profiles.md).

### 3–4. Modules

Modules run one after another, each isolated: a failure in one module is recorded as a coverage note and never becomes a false security finding. The full list is in [modules](modules.md).

### 5. Correlation

Several modules can observe the same underlying problem. A correlation pass merges duplicates so you see one finding with combined evidence, not five copies.

### 6. Scoring

Each finding gets a CVSS 3.1 base score computed from its vector, a confidence level and a verification state. These feed a separate urgency ranking (P0–P4) and the overall 0–100 security score. See [methodology](methodology.md).

### 7. History and delta

If the same target was scanned before with the same score model, the report shows which findings are new, resolved or unchanged. Findings are matched by stable fingerprints, not by title.

### 8. Reports

See [reports](reports.md) and [JSON output](json-output.md).

## Design principles

1. **Never report an untested area as clean.** Coverage is part of the result.
2. **Never invent evidence.** CVE identifiers appear only when a note points to NVD/OSV for follow-up; none are fabricated.
3. **Detection, not exploitation.** Probes use benign markers and look for signs of a weakness; they do not try to take advantage of it.
4. **Bounded everything.** Time, requests, DNS queries, bytes, crawl depth, parameters.
5. **Re-checkable results.** Each CVSS score can be reproduced from the printed vector; each finding lists the evidence behind it.
