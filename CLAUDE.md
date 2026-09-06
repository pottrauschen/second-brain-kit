# CLAUDE.md — second-brain-kit

Baukasten für die Bootstrap-Datei des Second Brain: eine Markdown-Datei,
mit der eine beliebige KI ein Second Brain im Gespräch anlegt. Quelle
der Wahrheit sind die Vorlagen unter `templates/`; `second-brain-bootstrap.md`
wird daraus mit `python build_bootstrap.py` erzeugt und nie von Hand
bearbeitet. Projektkontext im Second Brain: `/hole second-brain-kit`.

## Doc-Map

| Datei | Inhalt |
|---|---|
| `README.md` | Zweck, Benutzung, Aufbau, Herkunft der Vorlagen |
| `second-brain-bootstrap.md` | Erzeugtes Ergebnis (Teil A Anleitung, Teil B Dateien) |
| `templates/bootstrap-kopf.md` | Teil A: Gesprächsleitfaden A.1, Anlegen A.2, Werkzeug A.3, Abnahme A.4 |
| `templates/brain/CLAUDE.md` | Verfassung des Brains |
| `templates/brain/system/schema.md` | Seitentypen, Frontmatter, Regeln |
| `templates/brain/wiki/topics/anleitung.md` | Benutzungsanleitung |
| `templates/brain/wiki/topics/projekt-doku-standard.md` | Doku-Standard für Projekte |
| `templates/brain/maps/index.md`, `log.md`, `.gitattributes` | Router, Log-Kopf, Git-Attribute |
| `templates/brain/AGENTS-kopf.md` | Einleitung der AGENTS.md; die Abläufe hängt das Bau-Skript an |
| `templates/ablaeufe/hole.md`, `handoff.md` | Die zwei Abläufe mit `$ARGUMENTS` (Claude Code) bzw. `<projekt>` (AGENTS.md) |
| `templates/claude/CLAUDE-abschnitt.md` | Abschnitt für die globale CLAUDE.md von Claude Code |

## Arbeitsregeln

- **Nur Vorlagen ändern, dann bauen.** Nie in `second-brain-bootstrap.md`
  editieren; nach jeder Vorlagenänderung `python build_bootstrap.py`
  laufen lassen und das Ergebnis mitcommitten.
- **Platzhalter:** `<BRAIN>` und `<PYTHON>` in Prosa und Befehlen; in den
  Vorlagen darf `python3-64.exe` stehen, das Bau-Skript ersetzt es.
  Keine absoluten Pfade eines konkreten Rechners, keine Personennamen,
  keine Bezüge auf andere Brain-Instanzen oder Leser.
- **Skripte unverändert aus dem Live-Brain** (`S:\SecondBrain\system\scripts\`)
  übernehmen; bei Änderungen dort zuerst, dann hierher kopieren. Die
  Skripte dürfen keine vier aufeinanderfolgenden Backticks enthalten
  (Rahmen der Bootstrap-Datei), das Bau-Skript bricht sonst ab.
- **Dialog vor Schreiben:** Teil A verlangt von der KI, jeden Punkt mit
  dem Owner zu klären und nichts Bestehendes zu überschreiben. Diese
  Haltung bei Änderungen an `bootstrap-kopf.md` beibehalten.
- **Sprache:** Deutsch; Übersetzung überlässt Teil A der KI auf Wunsch
  des Owners.

## Befehle

```
python build_bootstrap.py
```

## Probelauf

Die Bootstrap-Datei in einem leeren Testordner einer KI geben und den
Dialog durchspielen; Abnahme ist ein grüner `brain_lint.py` im neuen
Brain und ein erstes Cockpit nach Onboarding.
