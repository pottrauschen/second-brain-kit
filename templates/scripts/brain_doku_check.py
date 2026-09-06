#!/usr/bin/env python3
"""Deterministischer Doku-Standard-Check für Projektordner.

Aufruf: python3-64.exe brain_doku_check.py <projektordner>
Exit 0 = konform, 1 = Verstöße. Der Befund ist verbindlich —
der Handoff legt ihn als Aufräum-Tabelle vor, das LLM interpretiert
ihn nicht weg. Standard: wiki/topics/projekt-doku-standard.md
Sprache der Ausgaben: system/lang ("de" oder "en"), Standard deutsch."""

import fnmatch
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_index import lang  # noqa: E402

EXCLUDE_DIRS = {".git", ".dart_tool", ".idea", ".vscode", "node_modules",
                "__pycache__", ".venv", "venv", "build", "dist", "target"}
CONVENTION = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE.md",
              "CLAUDE.md", "AGENTS.md"}
# Namen in docs/: kebab-case Pflicht; Kategorien-Präfixe nur Empfehlung
KEBAB = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")
BAD_NAME = re.compile(r"(_?[vV]\d|\d{4}-\d{2}|_final|_neu|_alt|_backup|"
                      r"[A-Z]{2,})")
MD_REF = re.compile(r"[\w./\\-]+\.md")

MSG = {
    "de": {
        "usage": "Aufruf: brain_doku_check.py <projektordner>",
        "no_dir": "Kein Ordner: {root}",
        "claude_missing": "CLAUDE.md fehlt (Pflicht: Arbeitsregeln + Doc-Map)",
        "readme_missing": "README.md fehlt (Pflicht)",
        "place": "ORT      {rel} — gehört nach docs/ (oder ist kein erlaubter Root-/Konventionsname)",
        "name": "NAME     {rel} — kebab-case Pflicht, keine Versionsnummern/Datumsstempel/GROSSBUCHSTABEN",
        "docmap": "DOC-MAP  {rel} — nicht in der Doc-Map der CLAUDE.md gelistet (Waise)",
        "docmap_dangling": "DOC-MAP  Eintrag '{ref}' zeigt auf fehlende Datei",
        "head": "Doku-Standard-Check: {root}",
        "checked": "{n} md-Dateien geprüft{note}\n",
        "note": ", {k} per .doku-check-ignore ausgenommen",
        "violation": "VERSTOSS {v}",
        "warn": "WARNUNG  {w}",
        "summary": "\n{v} Verstöße, {w} Warnungen",
    },
    "en": {
        "usage": "Usage: brain_doku_check.py <project folder>",
        "no_dir": "Not a folder: {root}",
        "claude_missing": "CLAUDE.md missing (required: working rules + doc map)",
        "readme_missing": "README.md missing (required)",
        "place": "PLACE    {rel} — belongs in docs/ (or is not an allowed root/convention name)",
        "name": "NAME     {rel} — kebab-case required, no version numbers/date stamps/UPPERCASE",
        "docmap": "DOC-MAP  {rel} — not listed in the doc map of CLAUDE.md (orphan)",
        "docmap_dangling": "DOC-MAP  entry '{ref}' points to a missing file",
        "head": "Docs standard check: {root}",
        "checked": "{n} md files checked{note}\n",
        "note": ", {k} excluded via .doku-check-ignore",
        "violation": "VIOLATION {v}",
        "warn": "WARNING  {w}",
        "summary": "\n{v} violations, {w} warnings",
    },
}


def t(key: str, **kw) -> str:
    return MSG[lang()][key].format(**kw)


def find_md(root: Path):
    for p in sorted(root.rglob("*.md")):
        if any(part in EXCLUDE_DIRS for part in p.relative_to(root).parts):
            continue
        yield p


def main() -> int:
    if len(sys.argv) != 2:
        print(t("usage"))
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(t("no_dir", root=root))
        return 2

    # Optionale Werkstatt-Ausnahmen: .doku-check-ignore im Projektroot,
    # je Zeile ein Ordner-Präfix oder Glob (relativ zum Root), # = Kommentar.
    # Begründung gehört als Kommentar in die Datei; sie ist Teil des Repos.
    ignored_pats = []
    ignore_file = root / ".doku-check-ignore"
    if ignore_file.exists():
        for line in ignore_file.read_text(encoding="utf-8",
                                          errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                ignored_pats.append(line.rstrip("/"))

    def is_ignored(rel: str) -> bool:
        return any(rel == pat or rel.startswith(pat + "/")
                   or fnmatch.fnmatch(rel, pat) for pat in ignored_pats)

    violations, warnings_ = [], []
    all_files = list(find_md(root))
    files = [p for p in all_files
             if not is_ignored(p.relative_to(root).as_posix())]
    skipped = len(all_files) - len(files)

    claude_md = root / "CLAUDE.md"
    doc_map_text = claude_md.read_text(encoding="utf-8", errors="replace") \
        if claude_md.exists() else ""
    if not claude_md.exists():
        violations.append(t("claude_missing"))
    if not (root / "README.md").exists():
        violations.append(t("readme_missing"))

    listed = set()
    for m in MD_REF.finditer(doc_map_text):
        ref = m.group(0).replace("\\", "/").lstrip("./")
        listed.add(ref)
        listed.add(ref.rsplit("/", 1)[-1])

    for p in files:
        rel = p.relative_to(root).as_posix()
        name = p.name
        parts = rel.split("/")

        # --- Ort ---
        ok_ort = (
            (len(parts) == 1 and name in CONVENTION)
            or (len(parts) >= 2 and parts[0] == "docs" and len(parts) == 2)
            or (len(parts) >= 2 and name == "README.md")
        )
        if not ok_ort:
            violations.append(t("place", rel=rel))
            continue  # Namens-Check für falsch liegende Dateien sinnlos

        # --- Namen (nur docs/) ---
        if parts[0] == "docs" and len(parts) == 2:
            if not KEBAB.match(name) or BAD_NAME.search(name):
                violations.append(t("name", rel=rel))

        # --- Doc-Map ---
        if name != "CLAUDE.md" and doc_map_text:
            if rel not in listed and name not in listed:
                violations.append(t("docmap", rel=rel))

    # Doc-Map-Einträge, deren Datei fehlt (auch ignorierte zählen als existent)
    existing = {p.relative_to(root).as_posix() for p in all_files} | \
               {p.name for p in all_files}
    for ref in sorted(listed):
        if "/" in ref and ref not in existing and not (root / ref).exists():
            warnings_.append(t("docmap_dangling", ref=ref))

    print(t("head", root=root))
    note = t("note", k=skipped) if skipped else ""
    print(t("checked", n=len(files), note=note))
    for v in violations:
        print(t("violation", v=v))
    for w in warnings_:
        print(t("warn", w=w))
    print(t("summary", v=len(violations), w=len(warnings_)))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
