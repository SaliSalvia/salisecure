# Reports

SaliSecure produces three kinds of PDF, all in the same visual identity (brand typography embedded in the file, optional logo and signature letterhead, A4, every page numbered with the scan id).

| Report | Pages | Audience | Scan |
|---|---|---|---|
| **Technical report** | Multi-page (the sample has 12) | Developers, DevOps, security staff | General, Deep |
| **Executive summary** | 1 | Managers, owners, decision makers | Deep |
| **Preview (demo / free trial)** | Short, partly locked | Prospective customers | Standard |

Samples: [executive summary](../assets/samples/SaliSecure-Sample-Executive-Summary.pdf) · [technical report](../assets/samples/SaliSecure-Sample-Technical-Report.pdf)

## Technical report: sections

| # | Section | What you get |
|---|---|---|
| 1 | Executive summary | Verdict, score, KPI tiles, control assessment table |
| 2 | Risk landscape | Radar chart across security vectors, overall gauge, severity donut |
| 3 | Prioritized findings (top 5) | The five things to fix first, with effort |
| 4 | Attack-surface inventory | Endpoints, subdomains, forms, APIs, scripts discovered |
| 5 | Security controls matrix | Transport, email authentication, headers, exposure, input handling |
| 6 | High-value asset status | Certificate, HTTPS redirect, DMARC, database exposure, WAF … |
| 7 | Business threat exposure | Heuristic infrastructure / data-breach / client-side index |
| 8 | TLS and certificate analysis | Protocol, cipher, key size, signature, issuer, lifetime |
| 9 | HTTP security posture | Header-by-header matrix, cookie flags, CORS, CSP |
| 10 | Reflected input and active-test statistics | What was tested, how many parameters and forms |
| 11 | Technical proof and self-verification log | Re-checkable evidence and reproduction commands |
| 12 | Discovered attack surface | robots, sitemap, `.well-known`, JavaScript, API, WebSocket |
| 13 | Findings appendix | Every finding with its CVSS 3.1 vector |
| 14 | Evidence dossiers | One card per finding: classification, impact, evidence, fix, limitations |
| 15 | Coverage, confidence and limitations | Completed / skipped / timed-out / failed checks |
| 16 | Endpoint, API and attack-surface inventory | Full inventory tables |
| 17 | Scan delta and traceability | New / resolved / unchanged findings since the last scan |
| 18 | Methodology and safety boundary | How to read the report ([methodology](methodology.md)) |

## Executive summary: sections

1. **Control assessment** — pass / review / risk / verify per control area (transport and TLS, email authentication, web security headers, exposed network services, input handling, attack-surface discovery).
2. **Priority actions** — the five most urgent actions with reason, action and effort.
3. **Risk exposure index** — the three heuristic percentages.

Plus the headline: score out of 100, grade, number of weaknesses, number of confirmed or observed items versus unverified indicators, check coverage, and the trend versus the previous scan.

## Reading a finding

Each finding card shows:

```
P2 / CRITICAL / CVSS 9.3 / TO VERIFY                    <finding id>
Title            what was found
Asset / endpoint where
Classification   CWE, OWASP Top 10 (2021), WSTG, ASVS
Confidence       HIGH | MEDIUM | LOW  /  verification state  /  detection source
Impact           why it matters
Evidence         the observation behind it
Remediation      what to change
Limitations      what the check could not establish
```

`TO VERIFY` marks an indicator that should be confirmed by a person before action. It is a feature, not a flaw: SaliSecure tells you how sure it is.

## Machine-readable output

The same data is available as JSON: see [JSON output](json-output.md).
