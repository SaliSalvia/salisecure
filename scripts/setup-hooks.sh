#!/bin/sh
# One-time setup after cloning: enable the leak-protection hooks.
#   sh scripts/setup-hooks.sh
set -e
root="$(git rev-parse --show-toplevel)"
cd "$root"
chmod +x .githooks/pre-commit .githooks/pre-push scripts/check_public_repo.py scripts/make_fingerprints.py
git config core.hooksPath .githooks
echo "Hooks enabled (core.hooksPath = .githooks)."

fp="$HOME/.salisecure/fingerprints.txt"
if [ -f "$fp" ]; then
  echo "Private fingerprints found: $fp"
else
  echo
  echo "Recommended: create private fingerprints of your source code so copied code is detected:"
  echo "  python3 scripts/make_fingerprints.py /path/to/PRIVATE/repo -o $fp"
fi
python3 scripts/check_public_repo.py
