# Maintainers: keeping the source code private

This repository is **documentation only**. The engine lives in a separate **private** repository. This page describes the setup that keeps the two apart.

## Layout

| Repository | Visibility | Contains |
|---|---|---|
| `salisecure-core` | **Private** | Engine source (all versions), fonts, brand assets, tests, build tooling |
| `salisecure` (this one) | Public | Documentation, previews, sample reports, community files |

Never copy a file from the private repository into this one. If you need a diagram, picture or table from the engine, write it again by hand.

## One-time setup (after cloning)

```bash
sh scripts/setup-hooks.sh
python3 scripts/make_fingerprints.py /path/to/salisecure-core -o ~/.salisecure/fingerprints.txt
```

The second command stores **hashes** of your source lines in `~/.salisecure/`, outside this repository. Re-run it when the private code changes materially.

Optional: put one regular expression per line in `~/.salisecure/forbidden_patterns.txt` (client domains, internal project names, API hostnames, anything that must never appear publicly).

## The four layers of protection

1. **Allow-list `.gitignore`.** Everything is ignored except a short list of document, image and sample types. `git add .` cannot stage a `.py`, `.zip` or font by accident.
2. **`pre-commit` hook.** Blocks a commit that contains source code, big code blocks, secrets, archives, fonts, or text that matches your private fingerprints or patterns.
3. **`pre-push` hook.** Re-checks every commit that is about to leave your machine, including commits made with `--no-verify`.
4. **GitHub Actions.** Checks the working tree **and the entire history** on every push and pull request. This also protects against contributors who do not have the hooks.

The hooks and the private fingerprints only exist on your machine; the Actions check works for everyone but has no access to your fingerprints.

Layers 2 and 3 **prevent** a leak. Layer 4 only **detects** one after the push, so while the repository is public treat a failed Actions run as an incident (see below). The safest habit is to keep the repository **private until the first full check passes**, then switch it to public.

## Before you make the repository public (checklist)

- [ ] Repository was created empty and the first commit came from this folder, not from a copy of the private one
- [ ] `python3 scripts/check_public_repo.py` and `python3 scripts/check_public_repo.py --history` both say `OK`
- [ ] Sample PDFs open without a text layer or hidden layers you did not intend (the shipped samples are flattened images)
- [ ] PDF metadata contains no personal name, e-mail, device name or real client domain (`pdfinfo file.pdf`)
- [ ] Settings → Code security: enable **Private vulnerability reporting**
- [ ] Settings → Features: disable **Wikis** and **Projects** if you do not want a second place to moderate
- [ ] Settings → Branches: protect `main` (require the *Public repository guard* check)
- [ ] Remember that public repositories can always be forked; this is harmless here because no source code is in the repository

## If source code was pushed by mistake

Deleting the file in a new commit is **not enough**; the history still contains it and anyone may already have copied it.

1. Make the repository private immediately (Settings → Danger zone).
2. Treat the exposed code as disclosed. Rotate any secret that was in it.
3. Delete the repository and create a new one from a clean folder. Rewriting history with `git filter-repo` also works, but cached copies, forks and pull-request refs on GitHub's servers may survive; contact GitHub Support to purge them.
4. Re-run `python3 scripts/check_public_repo.py --history` on the clean repository before making it public again.

## Protecting the engine itself

A public documentation repository only protects what you do not publish. For the engine:

- Prefer to **run scans on your own server** and deliver only the PDF. Code that never leaves your server cannot leak from a customer.
- If you must distribute the engine, compile it (for example with Nuitka), bind it to a **server-validated license**, watermark each build per customer, and put a **no-redistribution** clause in the contract. Obfuscation alone only slows a determined person down.
- Keep payload sets, signatures and pattern lists in the private repository or on the server, not in documentation.
