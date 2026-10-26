# Scan profiles

SaliSecure ships three fixed scan depths. Each has a hard time ceiling and hard budgets. The profile decides how much is checked, not how aggressively.

| | Scan 1 · General | Scan 2 · Standard | Scan 3 · Deep |
|---|---|---|---|
| Profile id | `2m` | `6m` | `12m` |
| Mode | Passive only | Passive + active | Passive + active |
| Time ceiling | 120 s | 360 s | 720 s |
| HTTP request budget | 200 | 500 | 1200 |
| DNS query budget | 40 | 90 | 260 |
| Subdomains resolved (max) | 15 | 40 | 120 |
| Crawl pages (max) | 15 | 35 | 100 |
| Crawl depth (max) | 2 | 3 | 4 |
| JavaScript files analysed (max) | 8 | 20 | 60 |
| API paths probed (max) | 10 | 30 | 80 |
| Parameters tested for injection indicators (max) | 10 | 35 | 80 |
| Login pages analysed (max) | 5 | 12 | 30 |
| OpenAPI documents (max) | 4 | 8 | 15 |

Values describe release 5.5.x. They are **ceilings**: a small site finishes well inside them.

## Adaptive budgets

Within the ceiling, SaliSecure scales its effort to the size of the target. After discovery modules (crawl, JavaScript, API, OpenAPI, subdomains, authentication) it estimates a *complexity score* from pages, endpoints, parameters, forms, scripts, APIs and subdomains, and spends more of the budget on complex sites. It never exceeds the profile's hard ceiling. The complexity score and the budget events are recorded in the JSON output.

## What each scan produces

| Scan | PDF output |
|---|---|
| 1 · General | Full technical report |
| 2 · Standard | Locked preview reports: a demo and a free-trial edition (see [free trial](free-trial.md)) |
| 3 · Deep | Full technical report **and** one-page executive summary |

## Choosing a scan

- **General (2 min)** — first look, recurring monitoring, sites you don't want to probe. Nothing beyond what a visitor, a DNS resolver and a TLS client already do.
- **Standard (6 min)** — a balanced assessment with active checks. Good for a trial and for most small and medium sites.
- **Deep (12 min)** — larger sites, many pages, APIs, forms and subdomains. Recommended before a launch or an audit.

Active scans send more traffic than normal browsing. Read [safety and authorization](safety-and-authorization.md) first.
