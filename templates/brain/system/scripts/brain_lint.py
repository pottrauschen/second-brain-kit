#!/usr/bin/env python3
"""Integritätsprüfung des Brains. Exit 0 = grün, 1 = Fehler.

Prüft: Frontmatter (wiki/), interne Links, Katalog-Abdeckung,
Unveränderlichkeit von raw/ (Hash-Register, neue Dateien werden
automatisch registriert — das ist der einzige Schreibvorgang)."""

import hashlib
import re
import sys
from pathlib import Path

BRAIN = Path(__file__).resolve().parents[2]
CATALOG = BRAIN / "system" / "generated" / "catalog.md"
HASHES = BRAIN / "system" / "generated" / "raw-hashes.txt"

VALID_TYPES = {"project-cockpit", "decision", "topic", "source", "note"}
VALID_STATUS = {"active", "done", "stale"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK = re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)\s]+)\)")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_index import parse_frontmatter  # noqa: E402

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def all_md(*dirs):
    for d in dirs:
        base = BRAIN / d
        if base.is_dir():
            yield from sorted(base.rglob("*.md"))


def check_frontmatter():
    for p in all_md("wiki"):
        rel = p.relative_to(BRAIN).as_posix()
        fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
        if fm is None:
            err(f"{rel}: Frontmatter fehlt oder ist nicht geschlossen")
            continue
        t = fm.get("type")
        if t not in VALID_TYPES:
            err(f"{rel}: type '{t}' ungültig (erlaubt: {sorted(VALID_TYPES)})")
        s = fm.get("status")
        if s not in VALID_STATUS:
            err(f"{rel}: status '{s}' ungültig (erlaubt: {sorted(VALID_STATUS)})")
        u = fm.get("updated", "")
        if not isinstance(u, str) or not DATE.match(u):
            err(f"{rel}: updated '{u}' ist kein Datum (YYYY-MM-DD)")
        if t == "project-cockpit" and not fm.get("project"):
            err(f"{rel}: project-cockpit ohne project-Feld")


def check_links():
    # Auflösbare Ziele: alle md unter wiki/, maps/ + Root-Dateien
    pages = list(all_md("wiki", "maps")) + [
        p for p in (BRAIN / n for n in ("cockpit.md", "log.md", "CLAUDE.md")) if p.exists()
    ]
    by_stem = {p.stem for p in pages}
    rel_paths = {p.relative_to(BRAIN).as_posix() for p in pages}

    for p in pages:
        rel = p.relative_to(BRAIN).as_posix()
        text = p.read_text(encoding="utf-8")
        for m in WIKILINK.finditer(text):
            target = m.group(1).strip()
            ok = (
                target in by_stem
                or target.rsplit("/", 1)[-1] in by_stem
                or f"{target}.md" in rel_paths
                or target in rel_paths
            )
            if not ok:
                err(f"{rel}: Wikilink [[{target}]] nicht auflösbar")
        for m in MDLINK.finditer(text):
            target = m.group(1).strip()
            if re.match(r"^(https?:|mailto:|repo:|#)", target):
                continue
            cand = (p.parent / target, BRAIN / target)
            if not any(c.exists() for c in cand):
                err(f"{rel}: Link ({target}) zeigt ins Leere")


def check_catalog():
    if not CATALOG.exists():
        warn("catalog.md fehlt — brain_index.py noch nie gelaufen?")
        return
    listed = set(re.findall(r"^\| (\S+\.md) \|", CATALOG.read_text(encoding="utf-8"), re.M))
    actual = {p.relative_to(BRAIN).as_posix() for p in all_md("wiki", "maps")}
    for missing in sorted(actual - listed):
        err(f"Katalog: {missing} fehlt — brain_index.py laufen lassen")
    for stale in sorted(listed - actual):
        err(f"Katalog: {stale} existiert nicht mehr — brain_index.py laufen lassen")


def check_raw():
    known = {}
    if HASHES.exists():
        for line in HASHES.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                path, digest = line.split("\t", 1)
                known[path] = digest
    current = {}
    raw = BRAIN / "raw"
    if raw.is_dir():
        for p in sorted(raw.rglob("*")):
            if p.is_file():
                rel = p.relative_to(BRAIN).as_posix()
                current[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    for rel, digest in current.items():
        if rel in known and known[rel] != digest:
            err(f"raw/ VERLETZT: {rel} wurde verändert (raw ist unveränderlich)")
        elif rel not in known:
            warn(f"raw/ neu registriert: {rel}")
    for rel in known:
        if rel not in current:
            err(f"raw/ VERLETZT: {rel} wurde gelöscht (raw ist unveränderlich)")
    merged = {**known, **{k: v for k, v in current.items() if k not in known}}
    HASHES.parent.mkdir(parents=True, exist_ok=True)
    out = "".join(f"{k}\t{v}\n" for k, v in sorted(merged.items()))
    if not HASHES.exists() or HASHES.read_text(encoding="utf-8") != out:
        HASHES.write_text(out, encoding="utf-8", newline="\n")


def main() -> int:
    check_frontmatter()
    check_links()
    check_catalog()
    check_raw()
    for w in warnings:
        print(f"WARNUNG  {w}")
    for e in errors:
        print(f"FEHLER   {e}")
    print(f"\nLint: {len(errors)} Fehler, {len(warnings)} Warnungen")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
