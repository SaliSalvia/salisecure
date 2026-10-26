# FAQ

## General

**What is SaliSecure?**
A website security assessment tool that runs 39 bounded checks and produces PDF reports (technical, executive one-page) and optional JSON. See the [overview](overview.md).

**Is it open source?**
No. This repository contains documentation only. The engine is proprietary.

**Does it replace a penetration test?**
No. It is an automated, external, point-in-time assessment with a strict safety boundary. It finds many common misconfigurations and indicators quickly and repeatably, but it does not replace manual testing, code review or an internal assessment.

**Is the score a certification?**
No. It is a heuristic index for tracking improvement over time. See [methodology](methodology.md).

## Scans

**How long does a scan take?**
At most 2, 6 or 12 minutes, depending on the profile. Small sites finish sooner. See [scan profiles](scan-profiles.md).

**What is the difference between passive and active?**
Passive checks use only what a normal visit, a DNS lookup and a TLS handshake reveal. Active checks send additional, bounded, detection-only probes. See [modules](modules.md).

**Will an active scan harm my site?**
It is designed not to, and it is strictly bounded, but it is not zero-risk: it sends more requests than a visitor and a few probes use `POST`. Prefer staging, or warn your operations team. See [safety and authorization](safety-and-authorization.md).

**Can I scan a site that I don't own?**
Only with the owner's written permission.

**Can it scan `localhost`, a private IP or an intranet host?**
No. Targets resolving to non-public addresses are refused by design.

**Does it log in to my site?**
No. It never uses real credentials and does not submit `POST` login forms. It only analyses the login page (HTTPS action, CSRF field, MFA indicators).

**Does it scan behind a login?**
No. It assesses the external, unauthenticated surface.

## Results

**What does "indicator" or "TO VERIFY" mean?**
A heuristic signal (for example a response that behaves like an injectable parameter) that has not been confirmed. Check it manually before treating it as proven. See [methodology](methodology.md#verification-states).

**Why does a finding with a high CVSS score have a low priority?**
CVSS describes impact if the weakness is real. Priority also weighs confidence, verification and evidence. An unconfirmed indicator ranks below a confirmed fact of equal CVSS.

**Why did my score not change after I fixed one issue?**
The score uses a diminishing union: the worst finding counts fully and the rest at half weight, so one fix may not move it if a more severe finding remains. Use the delta section (new / resolved / unchanged) to see progress.

**Does "no findings" mean my site is secure?**
No. It means the covered checks found nothing. A report with no findings is capped at a score of 90 for that reason.

**A check says SKIPPED / TIMEOUT. Is that bad?**
It means the check did not run (mode, budget or deadline). It is not counted as clean and is not a finding. Re-run with a deeper profile if you need it covered.

**Are CVE numbers reported?**
Only as review notes that point you to NVD / OSV. SaliSecure never invents a CVE identifier and does no live CVE lookup.

## Free trial

**What does the free report include?**
The verdict, the real total and severity counts, and one or two fully explained weaknesses with their fixes. The rest is locked. See [free trial](free-trial.md).

**Can the locked findings be recovered from the PDF?**
No. Their text is not written into the file.

## Reports and data

**Can I get the results as JSON?**
Yes. See [JSON output](json-output.md).

**Who should see my report?**
Only the people who fix the problems. A full report describes real weaknesses.
