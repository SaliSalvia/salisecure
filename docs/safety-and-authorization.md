# Safety and authorization

## You need permission

Only assess systems that you **own** or for which you hold **written authorization** from the owner. This applies to the free trial as well as to paid scans.

- Passive checks use information that is publicly visible to anyone (DNS, TLS, public pages, certificate transparency). They are still *an assessment of someone else's system*; get permission.
- Active checks send more than ordinary browsing traffic. Unauthorized testing can violate computer-misuse and cybercrime laws in many countries, and can breach your hosting provider's terms.
- Third-party hosting (shared hosting, CDN, SaaS platforms) often has its own rules about security testing. Check them first.

You are responsible for making sure you are authorized to test the target before you request or run an assessment.

## The safety boundary

### What SaliSecure does

- Resolves and validates the target, and **refuses private, loopback, link-local and other non-public addresses**, including when a redirect points there.
- Runs inside a hard **time limit** and hard **budgets** (requests, DNS queries, response bytes, crawl size, parameters).
- Uses **benign markers** to detect behaviour, and records indicators together with their limitations.
- Reads **existence only** for sensitive paths; file contents are never downloaded or stored.
- Records every skipped, failed or timed-out check instead of hiding it.

### What SaliSecure does not do

- No brute force, password guessing or credential stuffing
- No submission of `POST` login forms; no real credentials are ever used
- No exploit execution, no destructive or persistent payloads
- No file upload
- No SSRF callbacks or out-of-band fetches; URL-shaped parameters are only *flagged*
- No WebSocket handshakes; URLs are only noted
- No live CVE lookups and no invented CVE identifiers
- No access to data behind authentication

### Honest caveats about active scans

Active scans are designed to be non-destructive, but they are not invisible and not zero-risk:

- They send many more requests than a visitor, in a short time. A fragile server may react.
- A few probes use `POST` or `OPTIONS` (see [modules](modules.md#a-note-on-request-methods)). A `POST` of a harmless value to a form handler can still be logged, trigger an email, or create a record, depending on how that handler is written.
- Security tooling such as WAFs and intrusion detection may alert or block the scan. That is expected.

**Recommendation:** run Standard and Deep scans against a staging copy when you have one, or tell the people who monitor production beforehand.

## Recognizing SaliSecure traffic

- The `User-Agent` begins with `SaliSecure/`.
- Scans are time-boxed (2, 6 or 12 minutes).
- Besides the target, SaliSecure contacts only DNS resolvers (public resolvers and, as a fallback, the system resolver), `crt.sh` for certificate-transparency data and, when the operator supplies a key, `api.abuseipdb.com`.

If you see unexpected traffic that matches this description and you did not request a scan, please tell us (see [SECURITY.md](../SECURITY.md)).

## Data handling

- The assessment collects **technical observations about the target** (headers, certificate facts, DNS records, discovered paths). It is not designed to collect personal data about your visitors or users.
- Sensitive-path checks keep only whether a path exists.
- Secret-like patterns found in JavaScript are reported as a pattern type and a file name, not as the secret value.
- Preview reports mask addresses and banners.
- Treat a full report as **confidential**: it describes weaknesses of a real system. Share it only with people who need to fix them.

## What a report is not

A SaliSecure report is a point-in-time, external assessment. It is not a penetration test, a certification, a compliance attestation or a guarantee that a site is secure. A clean result means only that the covered checks found nothing.
