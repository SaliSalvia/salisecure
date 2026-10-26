#!/usr/bin/env python3
"""Guard for the public SaliSecure documentation repository.

Fails (exit 1) when something that does not belong in a documentation-only
repository is about to be committed, pushed or published: source code, large
code blocks, archives, fonts, secrets, or text copied from your private code.

Modes
    (default)     check every file in the working tree that git tracks or could track
    --staged      check what is staged for commit (used by .githooks/pre-commit)
    --pre-push    check every commit about to be pushed; reads git's pre-push
                  lines from stdin (used by .githooks/pre-push)
    --history     check every blob in the whole history (used by CI)

Private detectors (optional, never stored in this repository)
    fingerprints  hashes of your private source lines, made with
                  scripts/make_fingerprints.py.
                  Path: --fingerprints, $SALISECURE_FINGERPRINTS or
                  ~/.salisecure/fingerprints.txt
    patterns      one regular expression per line (client domains, internal
                  names ...). Path: --patterns, $SALISECURE_PATTERNS or
                  ~/.salisecure/forbidden_patterns.txt
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True      # never leave __pycache__ behind in the repository
sys.path.insert(0, HERE)
from make_fingerprints import HEADER, line_hash, normalize_line  # noqa: E402

# ---------------------------------------------------------------- allow-lists
ALLOWED_PY = {"scripts/check_public_repo.py", "scripts/make_fingerprints.py"}
ALLOWED_SH = {"scripts/setup-hooks.sh"}
ALLOWED_NOEXT = {"LICENSE", ".gitignore", ".gitattributes", ".githooks/pre-commit", ".githooks/pre-push"}
TEXT_EXT = {".md", ".yml", ".yaml"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
MAX_BYTES = {"text": 400_000, "script": 40_000, "image": 4_000_000, "pdf": 12_000_000}

PY_STRUCT = re.compile(r"^\s*(?:async\s+def\s+\w+|def\s+\w+\s*\(|class\s+\w+\s*[(:]|from\s+[\w.]+\s+import\s+\S|import\s+[\w.]+(?:\s*,\s*[\w.]+)*\s*$)")
PY_SHEBANG = re.compile(r"^#!.*\bpython")
FENCE = re.compile(r"^\s*(```|~~~)\s*([\w+-]*)")
BIG_B64 = re.compile(r"^[A-Za-z0-9+/=]{2000,}$")
SECRETS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("API key assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|passwd|password)\b\s*[:=]\s*['\"][A-Za-z0-9_\-/+=]{20,}['\"]")),
]


# ------------------------------------------------------------------- helpers
def git(*args, input_bytes=None, check=True):
    res = subprocess.run(["git", *args], input=input_bytes, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if check and res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {res.stderr.decode(errors='replace').strip()}")
    return res.stdout


def repo_root():
    try:
        return git("rev-parse", "--show-toplevel").decode().strip()
    except Exception:
        return os.path.dirname(HERE)


def read_lines_file(path):
    try:
        with open(os.path.expanduser(path), "r", encoding="utf-8", errors="replace") as fh:
            return [ln.rstrip("\n") for ln in fh]
    except OSError:
        return None


class Detectors:
    def __init__(self, fp_path, pat_path, fp_threshold):
        self.threshold = fp_threshold
        self.fingerprints = None
        self.patterns = []
        fp_path = fp_path or os.environ.get("SALISECURE_FINGERPRINTS") or "~/.salisecure/fingerprints.txt"
        lines = read_lines_file(fp_path)
        if lines and lines[0].strip() == HEADER:
            self.fingerprints = {ln.strip() for ln in lines[1:] if ln.strip()}
            self.fp_source = os.path.expanduser(fp_path)
        pat_path = pat_path or os.environ.get("SALISECURE_PATTERNS") or "~/.salisecure/forbidden_patterns.txt"
        for ln in read_lines_file(pat_path) or []:
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                try:
                    self.patterns.append(re.compile(ln))
                except re.error as exc:
                    print(f"warning: ignoring bad pattern {ln!r}: {exc}", file=sys.stderr)

    def describe(self):
        fp = f"{len(self.fingerprints)} fingerprints" if self.fingerprints is not None else "no fingerprints"
        return f"{fp}, {len(self.patterns)} private pattern(s)"


def pdf_text(data):
    """Text layer + metadata of a PDF ('' when no extractor is installed).

    Content streams are usually compressed, so scanning raw bytes would miss
    text. Uses pypdf if available, otherwise the `pdftotext` command."""
    try:
        import io
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        parts = [str(v) for v in (reader.metadata or {}).values()]
        parts += [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(parts)
    except ImportError:
        pass
    except Exception as exc:                      # damaged / encrypted PDF
        return f"[unreadable pdf: {exc}]"
    try:
        res = subprocess.run(["pdftotext", "-q", "-", "-"], input=data, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, timeout=60)
        return res.stdout.decode("utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        print("warning: neither pypdf nor pdftotext is available; PDF text layers were not scanned",
              file=sys.stderr)
        return ""


def classify(path):
    """Return (kind, problem). kind in text/script/image/pdf; problem set if not allowed."""
    p = path.replace("\\", "/")
    ext = os.path.splitext(p)[1].lower()
    if p in ALLOWED_PY or p in ALLOWED_SH:
        return "script", None
    if p in ALLOWED_NOEXT:
        return "text", None
    if ext in TEXT_EXT:
        return "text", None
    if ext in IMAGE_EXT:
        return "image", None
    if ext == ".pdf":
        return "pdf", None
    if ext in (".py", ".sh"):
        return None, "source/script file is not allowed in the public repository"
    if ext == "":
        return None, "file without extension is not allowed"
    return None, f"file type '{ext}' is not allowed in a documentation-only repository"


# --------------------------------------------------------------------- rules
def check_blob(path, data, det):
    """Return a list of violation strings for one file."""
    out = []
    kind, problem = classify(path)
    if problem:
        return [problem]
    if len(data) > MAX_BYTES[kind]:
        out.append(f"file too large ({len(data):,} bytes, limit {MAX_BYTES[kind]:,})")

    if kind in ("image",):
        text = data.decode("latin-1") if path.lower().endswith(".svg") else ""
    elif kind == "pdf":
        text = data.decode("latin-1") + "\n" + pdf_text(data)   # raw metadata + extracted text layer
    else:
        text = data.decode("utf-8", errors="replace")

    for rx in det.patterns:
        m = rx.search(text)
        if m:
            out.append(f"matches a private forbidden pattern ({rx.pattern!r})")
    if kind in ("image", "pdf"):
        return out

    lines = text.splitlines()
    for label, rx in SECRETS:
        for n, ln in enumerate(lines, 1):
            if rx.search(ln):
                out.append(f"line {n}: looks like a {label}")
                break

    if kind == "text":
        py_hits = [n for n, ln in enumerate(lines, 1) if PY_STRUCT.match(ln)]
        if len(py_hits) >= 6:
            out.append(f"looks like source code ({len(py_hits)} def/class/import lines, first at line {py_hits[0]})")
        for n, ln in enumerate(lines, 1):
            if PY_SHEBANG.match(ln):
                out.append(f"line {n}: python shebang in a non-script file")
                break
        for n, ln in enumerate(lines, 1):
            if BIG_B64.match(ln.strip()):
                out.append(f"line {n}: huge base64-like blob")
                break
        if path.lower().endswith(".md"):
            out += markdown_blocks(lines)

    if det.fingerprints is not None and kind in ("text", "script"):
        hits = [n for n, ln in enumerate(lines, 1)
                if (norm := normalize_line(ln)) and line_hash(norm) in det.fingerprints]
        if len(hits) >= det.threshold:
            out.append(f"{len(hits)} lines match your private source code (first at line {hits[0]})")
    return out


def markdown_blocks(lines):
    out, fence, lang, start = [], None, "", 0
    for n, ln in enumerate(lines, 1):
        m = FENCE.match(ln)
        if m and fence is None:
            fence, lang, start = m.group(1), m.group(2).lower(), n
        elif m and fence == m.group(1):
            size = n - start - 1
            if lang in ("python", "py", "python3") and size > 12:
                out.append(f"line {start}: {size}-line python code block (limit 12)")
            elif size > 60:
                out.append(f"line {start}: {size}-line code block (limit 60)")
            fence = None
    return out


# ---------------------------------------------------------------- file sources
def worktree_files(root):
    try:
        names = git("-C", root, "ls-files", "-co", "--exclude-standard", "-z").decode().split("\0")
    except Exception:
        names = []
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x != ".git"]
            names += [os.path.relpath(os.path.join(d, f), root) for f in files]
    for name in sorted(filter(None, set(names))):
        full = os.path.join(root, name)
        if os.path.isfile(full):
            with open(full, "rb") as fh:
                yield name, fh.read()


def staged_files(root):
    names = git("-C", root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").decode().split("\0")
    for name in filter(None, names):
        yield name, git("-C", root, "show", f":{name}")


def pushed_files(root, stdin_lines):
    seen = set()
    zero = "0" * 40
    for line in stdin_lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        _, local_sha, _, remote_sha = parts[:4]
        if local_sha == zero:
            continue
        rng = [local_sha, "--not", "--remotes"] if remote_sha == zero else [f"{remote_sha}..{local_sha}"]
        for commit in git("-C", root, "rev-list", *rng).decode().split():
            diff = git("-C", root, "diff-tree", "-r", "-m", "--root", "--no-commit-id",
                       "--diff-filter=ACMR", commit).decode()
            for row in diff.splitlines():
                meta, _, name = row.partition("\t")
                sha = meta.split()[3]
                if (sha, name) in seen:
                    continue
                seen.add((sha, name))
                yield name, git("-C", root, "cat-file", "blob", sha)


def history_files(root):
    listing = git("-C", root, "rev-list", "--objects", "--all").decode()
    pairs = [ln.split(" ", 1) for ln in listing.splitlines() if " " in ln]
    if not pairs:
        return
    stdin = "".join(f"{sha}\n" for sha, _ in pairs).encode()
    types = git("-C", root, "cat-file", "--batch-check=%(objecttype) %(objectname)", input_bytes=stdin).decode().splitlines()
    seen = set()
    for (sha, name), t in zip(pairs, types):
        if not t.startswith("blob") or (sha, name) in seen:
            continue
        seen.add((sha, name))
        yield name, git("-C", root, "cat-file", "blob", sha)


# ---------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--pre-push", action="store_true")
    mode.add_argument("--history", action="store_true")
    ap.add_argument("--fingerprints")
    ap.add_argument("--patterns")
    ap.add_argument("--fp-threshold", type=int, default=3, help="matching lines needed to fail (default 3)")
    ap.add_argument("--root", help="repository root (default: auto-detect)")
    args = ap.parse_args(argv)

    root = args.root or repo_root()
    det = Detectors(args.fingerprints, args.patterns, args.fp_threshold)
    if args.staged:
        source, label = staged_files(root), "staged files"
    elif args.pre_push:
        source, label = pushed_files(root, sys.stdin.read().splitlines()), "commits being pushed"
    elif args.history:
        source, label = history_files(root), "full history"
    else:
        source, label = worktree_files(root), "working tree"

    bad, count = {}, 0
    for name, data in source:
        count += 1
        problems = check_blob(name.replace("\\", "/"), data, det)
        if problems:
            bad.setdefault(name, []).extend(p for p in problems if p not in bad.get(name, []))

    if det.fingerprints is None and not args.history and sys.stderr.isatty():
        print("note: no private fingerprints found; run scripts/make_fingerprints.py for stronger protection",
              file=sys.stderr)
    if bad:
        print(f"BLOCKED: {len(bad)} file(s) do not belong in the public repository ({label}):\n", file=sys.stderr)
        for name, problems in sorted(bad.items()):
            for p in problems:
                print(f"  {name}: {p}", file=sys.stderr)
        print("\nThis repository is documentation only. Nothing was pushed or committed.", file=sys.stderr)
        return 1
    print(f"OK: {count} file(s) checked ({label}); {det.describe()}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
