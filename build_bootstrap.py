#!/usr/bin/env python3
"""Setzt second-brain-bootstrap.md aus templates/ zusammen.

Aufruf aus dem Kit-Ordner:  python build_bootstrap.py

Teil A kommt aus templates/bootstrap-kopf.md, Teil B aus den Vorlagen
unter templates/brain/ (Dateien des Brains), templates/ablaeufe/ (die
zwei Ablaeufe, einmal als AGENTS.md, einmal als Claude-Code-Befehle) und
templates/claude/ (Abschnitt fuer die globale CLAUDE.md). In allen
Vorlagen wird python3-64.exe durch den Platzhalter <PYTHON> ersetzt;
<BRAIN> steht schon in den Vorlagen. Die KI ersetzt beide beim Anlegen.
"""

import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
T = ROOT / "templates"
OUT = ROOT / "second-brain-bootstrap.md"
FENCE = "````"  # vier Backticks: die Vorlagen enthalten selbst dreifache

BRAIN_FILES = [
    ("CLAUDE.md", "markdown"),
    (".gitattributes", "text"),
    ("log.md", "markdown"),
    ("maps/index.md", "markdown"),
    ("system/schema.md", "markdown"),
    ("wiki/topics/anleitung.md", "markdown"),
    ("wiki/topics/projekt-doku-standard.md", "markdown"),
    ("system/scripts/brain_index.py", "python"),
    ("system/scripts/brain_lint.py", "python"),
    ("system/scripts/brain_doku_check.py", "python"),
]


def read(rel):
    text = (T / rel).read_text(encoding="utf-8")
    text = text.replace("python3-64.exe", "<PYTHON>")
    if FENCE in text:
        sys.exit("FEHLER: %s enthaelt vier Backticks, kollidiert mit dem Rahmen" % rel)
    return text


def block(title, path_label, text, lang):
    return "### %s\n\nPfad: `%s`\n\n%s%s\n%s\n%s\n\n" % (
        title, path_label, FENCE, lang, text.rstrip("\n"), FENCE)


def main():
    parts = []
    parts.append(read("bootstrap-kopf.md").rstrip("\n") + "\n\n")

    manifest = ["## Teil B: Dateien\n\n",
                "Reihenfolge und Pfade. `<BRAIN>` und `<PYTHON>` beim Schreiben ersetzen.\n\n",
                "| Datei | Zweck |\n|---|---|\n"]
    purposes = {
        "CLAUDE.md": "Verfassung: Invarianten, Suchleiter, Schreibtransaktion",
        ".gitattributes": "keine Zeilenenden-Konvertierung (Hashes in raw/)",
        "log.md": "append-only Log",
        "maps/index.md": "Router: Projekte, Themen, System",
        "system/schema.md": "Seitentypen, Frontmatter, Regeln",
        "wiki/topics/anleitung.md": "Benutzung in fuenf Minuten",
        "wiki/topics/projekt-doku-standard.md": "wohin md-Dateien in Projekten gehoeren",
        "system/scripts/brain_index.py": "erzeugt system/generated/catalog.md",
        "system/scripts/brain_lint.py": "Integritaet: Frontmatter, Links, Katalog, raw-Hashes",
        "system/scripts/brain_doku_check.py": "prueft ein Projekt-Repo gegen den Doku-Standard",
    }
    for rel, _ in BRAIN_FILES:
        manifest.append("| `<BRAIN>/%s` | %s |\n" % (rel, purposes[rel]))
    manifest.append("| `<BRAIN>/AGENTS.md` | die zwei Ablaeufe im Wortlaut, fuer alle Werkzeuge |\n")
    manifest.append("| `~/.claude/CLAUDE.md` (anhaengen) | nur Claude Code: Wegweiser |\n")
    manifest.append("| `~/.claude/commands/hole.md`, `handoff.md` | nur Claude Code: Slash-Befehle |\n\n")
    parts.append("".join(manifest))

    for rel, lang in BRAIN_FILES:
        parts.append(block("Datei: <BRAIN>/" + rel, "<BRAIN>/" + rel, read("brain/" + rel), lang))

    hole = read("ablaeufe/hole.md")
    handoff = read("ablaeufe/handoff.md")
    agents = (read("brain/AGENTS-kopf.md").rstrip("\n")
              + "\n\n## Ablauf 1: Kontext laden\n\n" + hole.replace("$ARGUMENTS", "<projekt>").rstrip("\n")
              + "\n\n## Ablauf 2: Stand sichern (Handoff)\n\n" + handoff.replace("$ARGUMENTS", "<projekt>"))
    parts.append(block("Datei: <BRAIN>/AGENTS.md", "<BRAIN>/AGENTS.md", agents, "markdown"))

    parts.append(block("Nur Claude Code: Abschnitt fuer ~/.claude/CLAUDE.md (anhaengen)",
                       "~/.claude/CLAUDE.md", read("claude/CLAUDE-abschnitt.md"), "markdown"))
    parts.append(block("Nur Claude Code: ~/.claude/commands/hole.md",
                       "~/.claude/commands/hole.md", hole, "markdown"))
    parts.append(block("Nur Claude Code: ~/.claude/commands/handoff.md",
                       "~/.claude/commands/handoff.md", handoff, "markdown"))

    parts.append("---\n\nEnde der Bootstrap-Datei. Erzeugt aus dem Second-Brain-Kit am %s.\n"
                 % datetime.date.today().isoformat())

    text = "".join(parts)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("geschrieben:", OUT.name, len(text.splitlines()), "Zeilen")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
