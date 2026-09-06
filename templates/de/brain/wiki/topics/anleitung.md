---
type: topic
status: active
updated: 2026-09-06
sources:
  - CLAUDE.md
  - system/schema.md
---

# Anleitung — So benutzt du dein Second Brain

## Session starten: Kontext holen

In Claude Code (beliebiger Ordner, typischerweise dein Projektordner):

```
/get <projektname>
```

In anderen Werkzeugen (Codex, Cursor, Gemini CLI, Aider …) stattdessen
im Klartext: „Lies `<BRAIN>/AGENTS.md` und lade den Kontext für
<projektname>." Der Ablauf ist derselbe.

Die KI lädt nur die kleine Cockpit-Seite des Projekts, fasst Stand,
Entscheidungen und offene Punkte zusammen und fragt, woran gearbeitet
werden soll. Kein manuelles Kontext-Einfüttern mehr.

## Arbeiten: wie immer

Nichts Neues zu lernen — normal mit der KI im Projekt arbeiten.

## Stand sichern: bei Meilensteinen, nicht erst bei Token-Not

```
/handoff
```

(oder: „Lies `<BRAIN>/AGENTS.md` und mach einen Handoff für
<projektname>.") Die KI verdichtet den Session-Stand, zeigt die Änderung
zur Freigabe (Write-Gate) und erledigt dann: Cockpit schreiben, Index
regenerieren, Log-Zeile, Git-Commit. Bei einem neuen Projekt legt der
Handoff die Cockpit-Seite an — so kommen Projekte ins Brain.

## Wissen reingeben

Dateien (Notizen, Chat-Exporte, Dokumente) nach `inbox/` legen und in
einer Session sagen: „Verdichte das ins Brain." Die KI schlägt eine
Wiki-Seite vor, du gibst frei, das Original wandert als Beleg nach
`raw/`.

## Wissen rausholen

Einfach fragen — in einer Session im Brain-Ordner oder nach dem Laden
des Kontexts. Die KI folgt der Suchleiter (Router → gezielt eine Seite),
lädt nie alles.

## Was du nie anfasst

- `raw/` — eingefrorene Belege (der Lint schlägt bei Änderungen an)
- `system/generated/` — wird von Skripten erzeugt

## Gesundheitscheck bei Bedarf

```
cd <BRAIN>
python3-64.exe system/scripts/brain_lint.py
```

Läuft auch als Teil der Session-Abschluss-Checkliste.

## Regeln im Detail

Verfassung: `CLAUDE.md` · Seitentypen und Schema: `system/schema.md` ·
Abläufe im Wortlaut: `AGENTS.md`.
