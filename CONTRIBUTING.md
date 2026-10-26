# Contributing

Thanks for your interest in SaliSecure.

## What this repository is

A **documentation-only** repository. The SaliSecure engine is proprietary and closed-source, so there is no code here to fix or extend, and **we cannot accept code contributions** (pull requests that add source code, scan logic, payloads, signatures or templates will be closed unmodified).

## Welcome

- Corrections: typos, unclear wording, wrong facts in the docs.
- Translation improvements for the Persian documentation (`docs/fa/`).
- Questions or suggestions about the documentation, via an [issue](../../issues/new/choose).

## How to propose a change

1. Open an issue describing what is wrong or missing, or fork the repository and open a pull request for a documentation fix.
2. Keep one topic per pull request.
3. Do not include real scan results, customer data, credentials, or the identity of any third-party target.
4. Do not describe or paste implementation details (internal function names, pattern lists, payload lists, thresholds that are not already in the docs).

By submitting a contribution you agree that it may be used under the terms in [LICENSE](LICENSE).

## Automated check

Every pull request runs `scripts/check_public_repo.py`. It fails if a change adds source code, large code blocks, secrets, fonts, archives or other files that do not belong in a documentation repository. Run it locally before you push:

```bash
python3 scripts/check_public_repo.py
```

## Security issues

Do not open a public issue. See [SECURITY.md](SECURITY.md).
