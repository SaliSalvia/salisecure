# Methodology

How SaliSecure turns observations into findings, severities, priorities and a score. The same explanation is printed in Section 18 of every full report.

## Finding model

Every finding carries:

| Field | Meaning |
|---|---|
| Title, impact, fix | What was found, why it matters, how to remove it |
| CVSS 3.1 vector and score | See below |
| Severity | Standard CVSS band |
| Confidence | `HIGH`, `MEDIUM`, `LOW` or `INFORMATIONAL` |
| Verification state | `VERIFIED`, `OBSERVED`, `NOT VERIFIED` or `INCONCLUSIVE` |
| Evidence | The concrete observations behind it |
| Standards tags | CWE, OWASP Top 10 (2021); WSTG and ASVS where the mapping is clear |
| Scan level | Whether it came from a passive or an active module |
| Fingerprint | A stable identifier used to compare scans over time |
| Limitations | What the check could **not** establish |

### Verification states

- **OBSERVED** — a directly observed fact, for example a missing header or a certificate that expires soon. Most findings are in this state.
- **NOT VERIFIED** — a heuristic *indicator*, such as a response that behaves like an injectable parameter. It tells you where to look. Confirm it manually before treating it as proven.
- **VERIFIED** — the strongest state, reserved for findings that were confirmed beyond a single observation.
- **INCONCLUSIVE** — used in the coverage section when a check could not decide (for example, no common DKIM selector answered, which cannot prove DKIM is absent).

An unconfirmed indicator never outranks a directly observed fact of equal CVSS.

## CVSS 3.1

Every base score is computed with the exact FIRST CVSS 3.1 formula from the vector stored with the finding. The vector is printed in the report's findings appendix, so any score can be re-checked with the public [FIRST calculator](https://www.first.org/cvss/calculator/3.1).

Severity is the standard qualitative band:

| Band | CVSS |
|---|---|
| Critical | 9.0 – 10.0 |
| High | 7.0 – 8.9 |
| Medium | 4.0 – 6.9 |
| Low | 0.1 – 3.9 |

CVSS expresses impact **if the weakness is real**. It does not include how well the tool verified it. That is what priority is for.

## Priority P0–P4 (urgency)

Priority starts from `CVSS × 10` and is weighted by confidence, verification state, amount of evidence, asset exposure and category.

| Priority | Score |
|---|---|
| P0 | 90 and above |
| P1 | 75 and above |
| P2 | 55 and above |
| P3 | 30 and above |
| P4 | below 30 |

So a *High* indicator with low confidence can land at P3, while a verified *High* lands at P1. Severity tells you how bad it would be; priority tells you what to fix first.

## Security score (0–100, higher is better)

```
score = 100 − weighted deduction of three category risks
        (infrastructure 35 %, data breach 35 %, client side 30 %),
        blended 75 / 25 with an aggregate-risk term
```

Properties:

- **Diminishing union.** Within a category, and in the aggregate, the worst finding counts fully and every further finding counts at half weight. Five medium header gaps cannot outweigh one verified critical exposure.
- **Monotonic.** Adding a finding can never raise the score.
- **Floor.** Reporting a trivial finding can never make a category look better than having no findings at all.
- **Cap.** A report with **no** findings is capped at 90. Absence of findings is not proof of absence of risk.
- **Comparable only to itself.** Each scan stores the *score model* version. A score is only compared with earlier scores from the same model.

| Score | Grade |
|---|---|
| 85 – 100 | Strong |
| 70 – 84 | Moderate |
| 50 – 69 | Weak |
| below 50 | High exposure |

The score is a heuristic index for tracking change over time. It is **not** a certification or a compliance attestation.

## Risk exposure index

The executive summary shows three heuristic percentages: infrastructure (ransomware / intrusion), data breach (leaks / email spoofing) and client side (XSS / phishing). They summarise the three category risks above and are indicative, not probabilities.

## Standards mappings

CWE and OWASP Top 10 (2021) tags are attached to findings; missing OWASP tags are back-filled from the CWE. WSTG and ASVS identifiers are a best-effort mapping. Treat them as a starting point, not as an audited compliance claim, and verify against the edition you work with. No CVE identifier is ever invented; CVE-related notes point you to NVD / OSV for manual follow-up.

## Interpreting results

- A **PASS** means the specific check completed without a finding. It does not prove the absence of vulnerabilities outside the covered scope.
- **Skipped**, **failed** and **timed-out** modules are listed in the coverage section. *Not found* is never confused with *not tested*.
- The scan is a point-in-time, external view. It does not replace a manual penetration test, a code review or an internal assessment.
