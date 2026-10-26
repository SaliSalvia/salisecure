# Security policy

## Reporting a vulnerability in SaliSecure

If you believe you have found a security problem in SaliSecure itself (the service on [salisec.ir](https://salisec.ir), the reports it produces, or the way it handles data), please report it **privately**.

1. Use GitHub's **private vulnerability reporting**: go to the *Security* tab of this repository and choose *Report a vulnerability*.
2. If that is not available to you, use the contact page on [salisec.ir](https://salisec.ir) and mark the message *Security*.

Please **do not** open a public issue or pull request for a vulnerability.

Include, when you can: what you found, where, steps to reproduce, and the impact you expect. Do not access, modify or retain data that is not yours, and do not run denial-of-service tests.

### What to expect

- We acknowledge your report as soon as we can.
- We investigate, fix, and tell you when it is resolved.
- We credit you if you wish, once a fix is released.

Good-faith research that follows this policy will not be pursued.

## Reporting unexpected scan traffic

If your logs show requests with a `User-Agent` starting with `SaliSecure/` and nobody in your organization requested an assessment, please tell us through the same channels, with the time range and your domain. See [docs/safety-and-authorization.md](docs/safety-and-authorization.md).

## Out of scope

- Findings in a third-party site that you scanned with SaliSecure (report those to that site's owner).
- Missing security headers or similar hardening on this documentation repository.
- Social engineering or physical attacks.

## Supported versions

Fixes are made to the current 5.5.x release line.

## This repository

This repository contains documentation only and holds no source code, credentials or customer data. If you notice any of those here, please report it privately as described above.
