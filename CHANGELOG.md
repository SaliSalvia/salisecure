# Changelog

User-visible changes to SaliSecure Core. Internal refactors are not listed. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [5.5.3]

### Fixed
- **Passive-only scans now always produce a PDF.** A lookup error in the radar-chart scoring could crash report generation when active modules were skipped. Vectors that could not be assessed now display as "N/A".
- The 12-minute profile now honours its full parameter budget for injection-indicator testing instead of a smaller hidden cap.
- Zone-transfer checks no longer connect to a name server that resolves to a private or internal address.
- Reverse-DNS lookups now count against the DNS query budget like every other lookup.
- Certificates were mislabelled as expired / invalid on older cryptography libraries; certificate dates are now read compatibly.
- Large logo images no longer overflow the report letterhead; temporary logo files are cleaned up after the run.
- `crossdomain.xml` / `clientaccesspolicy.xml` wildcard detection now handles single quotes and padded attributes.
- Open-port detection for HTTP ports now requires a real HTTP response before reporting a port as open.
- Error-page checks ignore normal (non-error) responses, removing false positives on single-page applications.
- Login forms: when a page has several forms, the real login form is now chosen.

### Changed
- Smaller outbound allow-list: only services that are actually used are permitted.

## [5.5.2]

### Fixed
- **CVSS accuracy.** 18 stored scores did not match their own vector. Every base score is now computed from the vector with the exact CVSS 3.1 formula, so a score and its vector can never disagree.

### Added
- The findings appendix prints the CVSS 3.1 vector of every finding, so any score can be re-checked with the FIRST calculator.
- The methodology section documents the real scoring model.

## [5.5.1]

### Fixed
- Priority bands no longer drop findings between band edges into P4 (an 89.5 now correctly ranks P1).
- **Non-monotonic score.** Adding a minor finding could previously raise the overall score. The aggregate and the three category risks now use a diminishing union, so adding a finding can never improve the score.
- A category with only trivial findings can no longer score better than a category with none.
- Five medium header gaps can no longer outweigh one verified critical exposure.
- Severity and priority are now consistent between JSON and PDF: severity is the CVSS band; urgency is P0–P4.
- Terminal severity counters now show correct values.

### Changed
- Scan history records the score model; scores from a different model are not used as the trend baseline.

## [5.5.0]

### Added
- **Dual-depth assessment**: passive-only and passive + active modes.
- Three bounded scan profiles: 2 minutes (passive), 6 minutes (standard) and 12 minutes (deep), with adaptive budget scaling inside hard ceilings.
- **39 modules**, including DNS intelligence, deep technology fingerprinting, injection indicators, SSRF-candidate flagging, authentication / session posture and offline CPE / CVE review notes.
- Evidence trail, OWASP Top 10 (2021) back-fill by CWE, WSTG and ASVS tags, and a correlation pass that merges duplicate findings.
- Safe WebSocket URL intelligence and authorization-candidate discovery.
- Richer machine-readable resource and coverage metadata.
- An offline self-test.

## [5.0.0]

### Added
- A normalized result model, stable finding fingerprints, deterministic risk prioritization, attack-surface graph, bounded OpenAPI / Swagger discovery, scan-to-scan diffing and richer JSON export.
- Evidence-aware risk engine: confidence, verification and exposure influence a separate priority score, so informational observations cannot dominate customer risk.

## Earlier (3.x – 4.x)

Branded report typography, logo and signature letterhead, TLS and certificate deep analysis, HSTS / CORS / CSP analysis, passive exposure and technology recon, reflected-input check, a unified request layer with request, DNS and byte budgets, and the target-safety guard that refuses non-public addresses.
