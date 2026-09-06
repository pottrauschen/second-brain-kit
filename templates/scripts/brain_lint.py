#!/usr/bin/env python3
"""Integritätsprüfung des Brains. Exit 0 = grün, 1 = Fehler.

Prüft: Frontmatter (wiki/), interne Links, Katalog-Abdeckung,
Unveränderlichkeit von raw/ (Hash-Register, neue Dateien werden
automatisch registriert — das ist der einzige Schreibvorgang).
Sprache der Ausgaben: system/lang ("de" oder "en"), Standard deutsch."""

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
from brain_index import lang, parse_frontmatter  # noqa: E402

MSG = {
    "de": {
        "fm_missing": "{rel}: Frontmatter fehlt oder ist nicht geschlossen",
        "type_invalid": "{rel}: type '{t}' ungültig (erlaubt: {allowed})",
        "status_invalid": "{rel}: status '{s}' ungültig (erlaubt: {allowed})",
        "updated_invalid": "{rel}: updated '{u}' ist kein Datum (YYYY-MM-DD)",
        "cockpit_project": "{rel}: project-cockpit ohne project-Feld",
        "wikilink": "{rel}: Wikilink [[{target}]] nicht auflösbar",
        "mdlink": "{rel}: Link ({target}) zeigt ins Leere",
        "catalog_none": "catalog.md fehlt — brain_index.py noch nie gelaufen?",
        "catalog_missing": "Katalog: {p} fehlt — brain_index.py laufen lassen",
        "catalog_stale": "Katalog: {p} existiert nicht mehr — brain_index.py laufen lassen",
        "raw_changed": "raw/ VERLETZT: {rel} wurde verändert (raw ist unveränderlich)",
        "raw_new": "raw/ neu registriert: {rel}",
        "raw_deleted": "raw/ VERLETZT: {rel} wurde gelöscht (raw ist unveränderlich)",
        "warn": "WARNUNG  {m}",
        "err": "FEHLER   {m}",
        "summary": "\nLint: {e} Fehler, {w} Warnungen",
    },
    "en": {
        "fm_missing": "{rel}: front matter missing or not closed",
        "type_invalid": "{rel}: type '{t}' invalid (allowed: {allowed})",
        "status_invalid": "{rel}: status '{s}' invalid (allowed: {allowed})",
        "updated_invalid": "{rel}: updated '{u}' is not a date (YYYY-MM-DD)",
        "cockpit_project": "{rel}: project-cockpit without project field",
        "wikilink": "{rel}: wikilink [[{target}]] cannot be resolved",
        "mdlink": "{rel}: link ({target}) points nowhere",
        "catalog_none": "catalog.md missing — has brain_index.py ever run?",
        "catalog_missing": "catalog: {p} missing — run brain_index.py",
        "catalog_stale": "catalog: {p} no longer exists — run brain_index.py",
        "raw_changed": "raw/ VIOLATED: {rel} was modified (raw is immutable)",
        "raw_new": "raw/ newly registered: {rel}",
        "raw_deleted": "raw/ VIOLATED: {rel} was deleted (raw is immutable)",
        "warn": "WARNING  {m}",
        "err": "ERROR    {m}",
        "summary": "\nLint: {e} errors, {w} warnings",
    },
}


def t(key: str, **kw) -> str:
    return MSG[lang()][key].format(**kw)


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
            err(t("fm_missing", rel=rel))
            continue
        ty = fm.get("type")
        if ty not in VALID_TYPES:
            err(t("type_invalid", rel=rel, t=ty, allowed=sorted(VALID_TYPES)))
        s = fm.get("status")
        if s not in VALID_STATUS:
            err(t("status_invalid", rel=rel, s=s, allowed=sorted(VALID_STATUS)))
        u = fm.get("updated", "")
        if not isinstance(u, str) or not DATE.match(u):
            err(t("updated_invalid", rel=rel, u=u))
        if ty == "project-cockpit" and not fm.get("project"):
            err(t("cockpit_project", rel=rel))


def check_links():
    # Auflösbare Ziele: alle md unter wiki/, maps/ + Root-Dateien
    pages = list(all_md("wiki", "maps")) + [
        p for p in (BRAIN / n for n in ("cockpit.md", "log.md", "CLAUDE.md", "AGENTS.md")) if p.exists()
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
                err(t("wikilink", rel=rel, target=target))
        for m in MDLINK.finditer(text):
            target = m.group(1).strip()
            if re.match(r"^(https?:|mailto:|repo:|#)", target):
                continue
            cand = (p.parent / target, BRAIN / target)
            if not any(c.exists() for c in cand):
                err(t("mdlink", rel=rel, target=target))


def check_catalog():
    if not CATALOG.exists():
        warn(t("catalog_none"))
        return
    listed = set(re.findall(r"^\| (\S+\.md) \|", CATALOG.read_text(encoding="utf-8"), re.M))
    actual = {p.relative_to(BRAIN).as_posix() for p in all_md("wiki", "maps")}
    for missing in sorted(actual - listed):
        err(t("catalog_missing", p=missing))
    for stale in sorted(listed - actual):
        err(t("catalog_stale", p=stale))


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
            err(t("raw_changed", rel=rel))
        elif rel not in known:
            warn(t("raw_new", rel=rel))
    for rel in known:
        if rel not in current:
            err(t("raw_deleted", rel=rel))
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
        print(t("warn", m=w))
    for e in errors:
        print(t("err", m=e))
    print(t("summary", e=len(errors), w=len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
