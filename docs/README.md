# SaliSecure documentation

> Documentation only. The SaliSecure engine is proprietary and its source code is not published. See the [README](../README.md).

| Document | Contents |
|---|---|
| [Overview](overview.md) | How an assessment runs, end to end |
| [Scan profiles](scan-profiles.md) | The 2 / 6 / 12 minute scans, their ceilings and outputs |
| [Modules](modules.md) | All 39 checks, grouped as passive or active |
| [Methodology](methodology.md) | CVSS 3.1, confidence, verification, P0–P4 priority, the 0–100 score |
| [Reports](reports.md) | Structure of the technical report and the executive summary |
| [Free trial](free-trial.md) | What the free preview shows and what stays locked |
| [JSON output](json-output.md) | Machine-readable result format |
| [Safety and authorization](safety-and-authorization.md) | The safety boundary and your responsibilities |
| [FAQ](faq.md) | Common questions |
| [Roadmap](roadmap.md) | Direction (not a commitment) |
| [Maintainers](maintainers.md) | How this public repository is kept free of source code |

Persian: [docs/fa](fa/README.md)

## Conventions

- **Passive** check: uses only what a normal page load, a DNS lookup, a TLS handshake or a certificate-transparency query already reveals.
- **Active** check: sends additional, deliberately probing requests. Always bounded, always detection-only.
- **Finding**: a weakness or an indicator of one, with severity, confidence, evidence and a fix.
- **Indicator**: a finding whose state is *not verified*. It tells you where to look; it is not proof.
- Documentation describes release **5.5.x**. Behaviour can change between releases; see the [changelog](../CHANGELOG.md).
