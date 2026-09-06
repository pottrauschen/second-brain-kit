#!/usr/bin/env python3
"""Setzt die Bootstrap-Dateien aus templates/ zusammen, eine je Sprache.

Aufruf aus dem Kit-Ordner:  python build_bootstrap.py

Je Sprache (templates/de, templates/en): Teil A aus bootstrap-kopf.md,
Teil B aus brain/ (Dateien des Brains), ablaeufe/ (die zwei Ablaeufe,
einmal als AGENTS.md, einmal als Claude-Code-Befehle) und claude/
(Abschnitt fuer die globale CLAUDE.md). Die drei Skripte kommen fuer
beide Sprachen aus templates/scripts/; sie lesen ihre Sprache zur
Laufzeit aus <BRAIN>/system/lang, das hier je Sprache erzeugt wird.
python3-64.exe wird ueberall durch <PYTHON> ersetzt; <BRAIN> steht schon
in den Vorlagen. Die KI ersetzt beide beim Anlegen.
"""

import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
T = ROOT / "templates"
FENCE = "````"  # vier Backticks: die Vorlagen enthalten selbst dreifache

SCRIPTS = ["brain_index.py", "brain_lint.py", "brain_doku_check.py"]

LANGS = {
    "de": {
        "out": "second-brain-bootstrap.de.md",
        "topics": ["wiki/topics/anleitung.md", "wiki/topics/projekt-doku-standard.md"],
        "file": "Datei",
        "path": "Pfad",
        "part_b": "## Teil B: Dateien\n\nReihenfolge und Pfade. `<BRAIN>` und `<PYTHON>` beim Schreiben ersetzen.\n\n| Datei | Zweck |\n|---|---|\n",
        "claude_only": "Nur Claude Code",
        "append": "anhängen",
        "purposes": {
            "CLAUDE.md": "Verfassung: Invarianten, Suchleiter, Schreibtransaktion",
            ".gitattributes": "keine Zeilenenden-Konvertierung (Hashes in raw/)",
            "log.md": "append-only Log",
            "maps/index.md": "Router: Projekte, Themen, System",
            "system/schema.md": "Seitentypen, Frontmatter, Regeln",
            "system/lang": "Sprache der Skript-Ausgaben",
            "wiki/topics/anleitung.md": "Benutzung in fünf Minuten",
            "wiki/topics/projekt-doku-standard.md": "wohin md-Dateien in Projekten gehören",
            "system/scripts/brain_index.py": "erzeugt system/generated/catalog.md",
            "system/scripts/brain_lint.py": "Integrität: Frontmatter, Links, Katalog, raw-Hashes",
            "system/scripts/brain_doku_check.py": "prüft ein Projekt-Repo gegen den Doku-Standard",
            "AGENTS.md": "die zwei Abläufe im Wortlaut, für alle Werkzeuge",
        },
        "manifest_claude": "| `~/.claude/CLAUDE.md` (anhängen) | nur Claude Code: Wegweiser |\n| `~/.claude/commands/get.md`, `handoff.md` | nur Claude Code: Slash-Befehle |\n\n",
        "agents_h1": "## Ablauf 1: Kontext laden",
        "agents_h2": "## Ablauf 2: Stand sichern (Handoff)",
        "section_title": "Abschnitt für ~/.claude/CLAUDE.md (anhängen)",
        "footer": "---\n\nEnde der Bootstrap-Datei. Erzeugt aus dem Second-Brain-Kit am {d}.\n",
    },
    "en": {
        "out": "second-brain-bootstrap.en.md",
        "topics": ["wiki/topics/guide.md", "wiki/topics/project-docs-standard.md"],
        "file": "File",
        "path": "Path",
        "part_b": "## Part B: Files\n\nOrder and paths. Replace `<BRAIN>` and `<PYTHON>` when writing.\n\n| File | Purpose |\n|---|---|\n",
        "claude_only": "Claude Code only",
        "append": "append",
        "purposes": {
            "CLAUDE.md": "constitution: invariants, search ladder, write transaction",
            ".gitattributes": "no line-ending conversion (hashes in raw/)",
            "log.md": "append-only log",
            "maps/index.md": "router: projects, topics, system",
            "system/schema.md": "page types, front matter, rules",
            "system/lang": "language of the script output",
            "wiki/topics/guide.md": "usage in five minutes",
            "wiki/topics/project-docs-standard.md": "where md files belong in projects",
            "system/scripts/brain_index.py": "generates system/generated/catalog.md",
            "system/scripts/brain_lint.py": "integrity: front matter, links, catalog, raw hashes",
            "system/scripts/brain_doku_check.py": "checks a project repo against the docs standard",
            "AGENTS.md": "the two routines verbatim, for all tools",
        },
        "manifest_claude": "| `~/.claude/CLAUDE.md` (append) | Claude Code only: signpost |\n| `~/.claude/commands/get.md`, `handoff.md` | Claude Code only: slash commands |\n\n",
        "agents_h1": "## Routine 1: get context",
        "agents_h2": "## Routine 2: save the state (handoff)",
        "section_title": "Section for ~/.claude/CLAUDE.md (append)",
        "footer": "---\n\nEnd of the bootstrap file. Generated from the Second Brain Kit on {d}.\n",
    },
}


def read(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("python3-64.exe", "<PYTHON>")
    if FENCE in text:
        sys.exit("FEHLER: %s enthaelt vier Backticks, kollidiert mit dem Rahmen" % path)
    return text


def block(title, path_label, text, lang_hint, L):
    return "### %s\n\n%s: `%s`\n\n%s%s\n%s\n%s\n\n" % (
        title, L["path"], path_label, FENCE, lang_hint, text.rstrip("\n"), FENCE)


def build(code: str) -> None:
    L = LANGS[code]
    base = T / code
    brain_files = [("CLAUDE.md", "markdown"), (".gitattributes", "text"), ("log.md", "markdown"),
                   ("maps/index.md", "markdown"), ("system/schema.md", "markdown"),
                   ("system/lang", "text")] + [(t, "markdown") for t in L["topics"]] + \
                  [("system/scripts/" + s, "python") for s in SCRIPTS]

    parts = [read(base / "bootstrap-kopf.md").rstrip("\n") + "\n\n", L["part_b"]]
    for rel, _ in brain_files:
        parts.append("| `<BRAIN>/%s` | %s |\n" % (rel, L["purposes"][rel]))
    parts.append("| `<BRAIN>/AGENTS.md` | %s |\n" % L["purposes"]["AGENTS.md"])
    parts.append(L["manifest_claude"])

    for rel, hint in brain_files:
        if rel == "system/lang":
            text = code + "\n"
        elif rel.startswith("system/scripts/"):
            text = read(T / "scripts" / rel.split("/")[-1])
        else:
            text = read(base / "brain" / rel)
        parts.append(block("%s: <BRAIN>/%s" % (L["file"], rel), "<BRAIN>/" + rel, text, hint, L))

    get = read(base / "ablaeufe" / "get.md")
    handoff = read(base / "ablaeufe" / "handoff.md")
    agents = (read(base / "brain" / "AGENTS-kopf.md").rstrip("\n")
              + "\n\n" + L["agents_h1"] + "\n\n" + get.replace("$ARGUMENTS", "<project>" if code == "en" else "<projekt>").rstrip("\n")
              + "\n\n" + L["agents_h2"] + "\n\n" + handoff.replace("$ARGUMENTS", "<project>" if code == "en" else "<projekt>"))
    parts.append(block("%s: <BRAIN>/AGENTS.md" % L["file"], "<BRAIN>/AGENTS.md", agents, "markdown", L))

    parts.append(block("%s: %s" % (L["claude_only"], L["section_title"]), "~/.claude/CLAUDE.md",
                       read(base / "claude" / "CLAUDE-abschnitt.md"), "markdown", L))
    parts.append(block("%s: ~/.claude/commands/get.md" % L["claude_only"], "~/.claude/commands/get.md", get, "markdown", L))
    parts.append(block("%s: ~/.claude/commands/handoff.md" % L["claude_only"], "~/.claude/commands/handoff.md", handoff, "markdown", L))
    parts.append(L["footer"].format(d=datetime.date.today().isoformat()))

    text = "".join(parts)
    out = ROOT / L["out"]
    out.write_text(text, encoding="utf-8", newline="\n")
    print("geschrieben:", out.name, len(text.splitlines()), "Zeilen")


def main():
    for code in LANGS:
        build(code)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
