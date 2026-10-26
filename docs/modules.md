# Modules

Release 5.5.x runs **39 modules**: 20 passive and 19 active. The module id is what appears in the JSON output (`module_status`) and in the coverage section of the report.

In a passive-only scan every active module is recorded as `SKIPPED` ("not run in passive-only mode"), so you can always see what was left out.

## Passive modules (20)

| Id | Area | What it checks |
|---|---|---|
| `dns` | Infrastructure | DNS records (A / AAAA / MX / NS) and public-IP posture; SPF, DMARC and DKIM |
| `http` | Transport | HTTP status, server response and HTTPS redirect posture |
| `ssl` | Transport | Certificate validity and expiry |
| `tls_depth` | Transport | Negotiated TLS protocol, acceptance of legacy TLS versions |
| `tls_certificate` | Transport | Key size, signature algorithm, issuer, self-signed detection |
| `tls_cipher_enum` | Transport | Bounded check for legacy / weak cipher suites and protocols |
| `http_posture` | Web | Security headers (HSTS directives, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy …) and cookie flags |
| `csp_directives` | Web | Content-Security-Policy directive and `frame-ancestors` analysis |
| `dns_posture` | Email / DNS | CAA records and DNSSEC posture |
| `dns_wildcard` | DNS | Wildcard DNS presence |
| `dns_zone_transfer` | DNS | Bounded AXFR exposure indicator (public name servers only) |
| `reverse_dns` | Infrastructure | Reverse-DNS (PTR) enrichment |
| `dns_intelligence` | Infrastructure | MX / NS intelligence and bounded common-subdomain resolution |
| `tech_fingerprint_deep` | Software | Passive technology and framework fingerprinting (headers, generator tags, JS frameworks) |
| `robots_sitemap` | Discovery | `robots.txt` and sitemap posture |
| `well_known` | Discovery | RFC 8615 `/.well-known` resource discovery |
| `crossdomain` | Web | `crossdomain.xml` / `clientaccesspolicy.xml` policy inspection |
| `subdomains` | Discovery | Subdomain enrichment from certificate transparency |
| `ip_reputation` | Infrastructure | Optional IP reputation lookup (only when an API key is supplied) |
| `cpe_cve_correlation` | Software | Offline product → CPE mapping with review notes pointing to NVD / OSV. No live lookup; no CVE is ever invented |

## Active modules (19)

All active modules are bounded and detection-only.

| Id | Area | What it checks |
|---|---|---|
| `ports` | Network | Bounded TCP connection probe of a predefined list of common ports. Includes a check for network middleboxes that answer on every port, and validates service responses to avoid false "open" results |
| `waf` | Web | Lightweight WAF fingerprinting |
| `cors_reflection` | Web | Whether an arbitrary `Origin` is reflected in CORS headers |
| `exposure` | Discovery | **Existence-only** check for common sensitive paths (contents are never downloaded or stored), CMS / technology hints, and the presence of `security.txt` (RFC 9116) |
| `reflection` | Application | One harmless marker to detect unencoded reflection (XSS indicator); nothing is executed |
| `crawl_surface` | Attack surface | Bounded same-origin crawl; collects links, parameters and forms |
| `js_intelligence` | Attack surface | Endpoints and secret-like patterns referenced in JavaScript files |
| `api_discovery` | API | Common REST and GraphQL paths; GraphQL introspection check |
| `openapi_surface` | API | Same-origin JSON OpenAPI / Swagger documents and the endpoints they declare |
| `websocket_intelligence` | API | WebSocket URLs found in the already-observed surface. No handshake is performed |
| `authorization_candidates` | Identity | Object-level API endpoints worth manual authorization testing. No unauthorized access is attempted |
| `http_methods` | Web | `OPTIONS` / `Allow` method posture |
| `security_misconfig` | Web | Non-destructive misconfiguration checks |
| `error_pages` | Web | Error-page information disclosure indicators (only on genuine error responses) |
| `open_redirect` | Application | Bounded, benign open-redirect indicator |
| `host_header` | Web | Benign Host-header reflection indicator |
| `injection_indicators` | Application | Benign error-signature and response-difference probes for SQLi, NoSQLi, SSTI, LDAP and XPath injection. Detection only; results are *indicators* until verified |
| `ssrf_candidates` | Application | Flags URL-shaped parameters. **No callback and no fetch** is performed |
| `auth_session` | Identity | Login-form analysis: HTTPS action, CSRF field, MFA indicators, verbose-error indicators. No real credentials are used and login forms that use `POST` are never submitted |

### A note on request methods

Most probes are `GET`. A few active checks use other methods in a benign way:

- `OPTIONS` to read the allowed methods;
- a single GraphQL **introspection query** (read-only) against GraphQL endpoints that were found;
- `POST` of a harmless marker value to form parameters in `injection_indicators`.

Because a `POST` can reach application logic, run Standard and Deep scans against production only with the owner's awareness, or against a staging copy. See [safety and authorization](safety-and-authorization.md).

## Module status values

| Status | Meaning |
|---|---|
| `COMPLETED` | The module ran to the end |
| `SKIPPED` | Not run: passive-only mode, budget exhausted, or blocked target |
| `TIMEOUT` | The scan deadline was reached first |
| `FAILED` | The module hit an internal error. This is **not** a security finding |

Anything other than `COMPLETED` is listed in the report's coverage section and is never counted as clean.
