# CLAUDE.md — second-brain-kit

Baukasten für die Bootstrap-Dateien des Second Brain: je Sprache eine
Markdown-Datei, mit der eine beliebige KI ein Second Brain im Gespräch
anlegt. Quelle der Wahrheit sind die Vorlagen unter `templates/`; die
Dateien `second-brain-bootstrap.de.md` und `second-brain-bootstrap.en.md`
werden daraus mit `python build_bootstrap.py` erzeugt und nie von Hand
bearbeitet. Projektkontext im Second Brain: `/hole second-brain-kit`.

## Doc-Map

| Datei | Inhalt |
|---|---|
| `README.md` | Zweck, Benutzung, Aufbau, Herkunft der Vorlagen |
| `second-brain-bootstrap.de.md`, `second-brain-bootstrap.en.md` | Erzeugte Ergebnisse (Teil A Anleitung, Teil B Dateien) |
| `templates/de/bootstrap-kopf.md`, `templates/en/bootstrap-kopf.md` | Teil A: Gespräch A.1, Anlegen A.2, Werkzeug A.3, Abnahme A.4, Regeln A.5 |
| `templates/de/brain/CLAUDE.md`, `templates/en/brain/CLAUDE.md` | Verfassung des Brains |
| `templates/de/brain/system/schema.md`, `templates/en/brain/system/schema.md` | Seitentypen, Frontmatter, Regeln |
| `templates/de/brain/wiki/topics/anleitung.md`, `templates/en/brain/wiki/topics/guide.md` | Benutzungsanleitung |
| `templates/de/brain/wiki/topics/projekt-doku-standard.md`, `templates/en/brain/wiki/topics/project-docs-standard.md` | Doku-Standard für Projekte |
| `templates/de/brain/maps/index.md`, `templates/en/brain/maps/index.md`, dazu je `log.md` und `.gitattributes` | Router, Log-Kopf, Git-Attribute |
| `templates/de/brain/AGENTS-kopf.md`, `templates/en/brain/AGENTS-kopf.md` | Einleitung der AGENTS.md; die Abläufe hängt das Bau-Skript an |
| `templates/de/ablaeufe/get.md`, `templates/de/ablaeufe/handoff.md`, `templates/en/ablaeufe/get.md`, `templates/en/ablaeufe/handoff.md` | Die zwei Abläufe mit `$ARGUMENTS` (Claude Code) bzw. `<projekt>`/`<project>` (AGENTS.md) |
| `templates/de/claude/CLAUDE-abschnitt.md`, `templates/en/claude/CLAUDE-abschnitt.md` | Abschnitt für die globale CLAUDE.md von Claude Code |
| `templates/scripts/*.py` | brain_index, brain_lint, brain_doku_check; zweisprachig über `system/lang` |

## Arbeitsregeln

- **Nur Vorlagen ändern, dann bauen.** Nie in den erzeugten Dateien
  editieren; nach jeder Vorlagenänderung `python build_bootstrap.py`
  laufen lassen und beide Ergebnisse mitcommitten.
- **Beide Sprachen zusammen pflegen.** Eine inhaltliche Änderung in
  `templates/de` bekommt ihr Gegenstück in `templates/en` im selben
  Commit. Der Befehl heißt in beiden Sprachen `/get` und `/handoff`.
- **Platzhalter:** `<BRAIN>` und `<PYTHON>` in Prosa und Befehlen; in den
  Vorlagen darf `python3-64.exe` stehen, das Bau-Skript ersetzt es.
  Keine absoluten Pfade eines konkreten Rechners, keine Personennamen,
  keine Bezüge auf andere Brain-Instanzen oder Leser.
- **Skripte** liegen einmal unter `templates/scripts/` und sind identisch
  mit denen des Live-Brains des Autors (Pfad in `CLAUDE.local.md`);
  Änderungen dort zuerst, dann hierher kopieren. Meldungen stehen im `MSG`-Wörterbuch
  je Sprache; die deutschen Texte bleiben wörtlich wie im Live-Brain. Die
  Skripte dürfen keine vier aufeinanderfolgenden Backticks enthalten
  (Rahmen der Bootstrap-Datei), das Bau-Skript bricht sonst ab.
- **Dialog vor Schreiben:** Teil A verlangt von der KI, jeden Punkt mit
  dem Owner zu klären und nichts Bestehendes zu überschreiben. Diese
  Haltung bei Änderungen an `bootstrap-kopf.md` beibehalten.

## Befehle

```
python build_bootstrap.py
```

## Probelauf

Eine Bootstrap-Datei in einem leeren Testordner einer KI geben und den
Dialog durchspielen; Abnahme ist ein grüner `brain_lint.py` im neuen
Brain (deutsch „0 Fehler", englisch „0 errors") und ein erstes Cockpit
nach Onboarding.
