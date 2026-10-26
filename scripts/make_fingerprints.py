#!/usr/bin/env python3
"""Build a private "fingerprint" file from your PRIVATE source code.

The fingerprint file holds one short hash per distinctive source line (not the
lines themselves). `check_public_repo.py` uses it to detect when code copied
from your private repository ends up in this public one, even if it was pasted
into a Markdown file or renamed.

    python3 scripts/make_fingerprints.py /path/to/private/repo -o ~/.salisecure/fingerprints.txt

Keep the output OUTSIDE this repository (the .gitignore of this repository
would not stage it anyway). Re-run it whenever the private code changes.
"""
import argparse
import hashlib
import os
import sys

MIN_LEN = 30                      # ignore short / generic lines
HEADER = "# salisecure-fingerprints v1"
SOURCE_EXT = {".py", ".js", ".ts", ".php", ".go", ".rs", ".java", ".c", ".cpp", ".h",
              ".sh", ".sql", ".json", ".yml", ".yaml", ".html", ".css", ".txt", ".md"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache"}


def normalize_line(line):
    """Whitespace-insensitive form of a line, or None if it is not distinctive."""
    norm = " ".join(line.split())
    if len(norm) < MIN_LEN:
        return None
    if not any(ch.isalnum() for ch in norm):
        return None
    if set(norm) <= set("=-#*_/~+. "):          # separator lines
        return None
    return norm


def line_hash(norm):
    return hashlib.sha256(norm.encode("utf-8", "replace")).hexdigest()[:16]


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if os.path.splitext(name)[1].lower() in SOURCE_EXT:
                    yield os.path.join(root, name)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="private source files or directories")
    ap.add_argument("-o", "--output", required=True, help="fingerprint file to write")
    args = ap.parse_args(argv)

    hashes = set()
    files = 0
    for path in iter_files(args.paths):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    norm = normalize_line(line)
                    if norm:
                        hashes.add(line_hash(norm))
        except OSError as exc:
            print(f"skip {path}: {exc}", file=sys.stderr)
            continue
        files += 1

    out = os.path.abspath(os.path.expanduser(args.output))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(HEADER + "\n")
        fh.write("\n".join(sorted(hashes)) + "\n")
    try:
        os.chmod(out, 0o600)
    except OSError:
        pass
    print(f"{len(hashes)} fingerprints from {files} file(s) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
