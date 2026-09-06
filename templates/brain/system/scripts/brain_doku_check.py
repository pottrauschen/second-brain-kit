#!/usr/bin/env python3
"""Deterministischer Doku-Standard-Check für Projektordner.

Aufruf: python3-64.exe brain_doku_check.py <projektordner>
Exit 0 = konform, 1 = Verstöße. Der Befund ist verbindlich —
/handoff legt ihn als Aufräum-Tabelle vor, das LLM interpretiert
ihn nicht weg. Standard: wiki/topics/projekt-doku-standard.md"""

import fnmatch
import re
import sys
from pathlib import Path

EXCLUDE_DIRS = {".git", ".dart_tool", ".idea", ".vscode", "node_modules",
                "__pycache__", ".venv", "venv", "build", "dist", "target"}
CONVENTION = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE.md",
              "CLAUDE.md"}
# Namen in docs/: kebab-case Pflicht; Kategorien-Präfixe nur Empfehlung
KEBAB = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")
BAD_NAME = re.compile(r"(_?[vV]\d|\d{4}-\d{2}|_final|_neu|_alt|_backup|"
                      r"[A-Z]{2,})")
MD_REF = re.compile(r"[\w./\\-]+\.md")


def find_md(root: Path):
    for p in sorted(root.rglob("*.md")):
        if any(part in EXCLUDE_DIRS for part in p.relative_to(root).parts):
            continue
        yield p


def main() -> int:
    if len(sys.argv) != 2:
        print("Aufruf: brain_doku_check.py <projektordner>")
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Kein Ordner: {root}")
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
        violations.append("CLAUDE.md fehlt (Pflicht: Arbeitsregeln + Doc-Map)")
    if not (root / "README.md").exists():
        violations.append("README.md fehlt (Pflicht)")

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
            violations.append(f"ORT      {rel} — gehört nach docs/ "
                              f"(oder ist kein erlaubter Root-/Konventionsname)")
            continue  # Namens-Check für falsch liegende Dateien sinnlos

        # --- Namen (nur docs/) ---
        if parts[0] == "docs" and len(parts) == 2:
            if not KEBAB.match(name) or BAD_NAME.search(name):
                violations.append(f"NAME     {rel} — kebab-case Pflicht, "
                                  f"keine Versionsnummern/Datumsstempel/"
                                  f"GROSSBUCHSTABEN")

        # --- Doc-Map ---
        if name != "CLAUDE.md" and doc_map_text:
            if rel not in listed and name not in listed:
                violations.append(f"DOC-MAP  {rel} — nicht in der Doc-Map "
                                  f"der CLAUDE.md gelistet (Waise)")

    # Doc-Map-Einträge, deren Datei fehlt (auch ignorierte zählen als existent)
    existing = {p.relative_to(root).as_posix() for p in all_files} | \
               {p.name for p in all_files}
    for ref in sorted(listed):
        if "/" in ref and ref not in existing and not (root / ref).exists():
            warnings_.append(f"DOC-MAP  Eintrag '{ref}' zeigt auf fehlende Datei")

    print(f"Doku-Standard-Check: {root}")
    note = f", {skipped} per .doku-check-ignore ausgenommen" if skipped else ""
    print(f"{len(files)} md-Dateien geprüft{note}\n")
    for v in violations:
        print(f"VERSTOSS {v}")
    for w in warnings_:
        print(f"WARNUNG  {w}")
    print(f"\n{len(violations)} Verstöße, {len(warnings_)} Warnungen")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
