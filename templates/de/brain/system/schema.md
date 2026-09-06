# Schema — Seitentypen, Frontmatter, Regeln

## Ordnersemantik

| Ordner | Bedeutung | Wer schreibt |
|---|---|---|
| `raw/` | Unveränderliche Belege (archivierte Session-Artefakte, Quelldokumente) | nur Import-Workflow, dann eingefroren |
| `inbox/` | Eingangskorb — wartet auf Verarbeitung | Owner legt ab, Ingest räumt |
| `wiki/` | Abgeleitetes, gepflegtes Wissen — einziger Pflegeort | KI (mit Write-Gate) |
| `maps/` | Retrieval-Router (kleine Wegweiser-Seiten) | KI (mit Write-Gate) |
| `system/` | Regeln, Skripte, Generiertes | Skripte; Regeln nur auf Auftrag |

## Frontmatter (Pflicht für alle Seiten unter `wiki/`)

```yaml
---
type: project-cockpit | decision | topic | source | note
project: mein-projekt     # Pflicht bei project-cockpit, sonst optional
status: active | done | stale
updated: 2026-01-31       # bei jeder inhaltlichen Änderung setzen
sources: []               # Belege: raw/<pfad> oder repo:<absoluter pfad>
---
```

## Seitentypen

- **project-cockpit** (`wiki/projects/<name>/cockpit.md`): Einstiegsseite
  eines Projekts. Abschnitte: Stand (3–6 Sätze) · Entscheidungen (mit
  Warum) · Offene Punkte / Nächste Schritte · Stolperfallen ·
  Live-Quellen. Ziel: unter ~150 Zeilen — Details in eigene Seiten
  (`decisions.md`, `gotchas.md`) auslagern, wenn es wächst.
- **decision**: eine wichtige Entscheidung mit Kontext, Alternativen,
  Begründung, Datum.
- **topic** (`wiki/topics/`): projektübergreifendes Technik-Wissen.
- **source** (`wiki/sources/`): Verdichtung genau einer Quelle aus `raw/`.
- **note**: alles andere Kleine.

## Live-Quellen-Regel

Dateien, die zu einem Code-Repo gehören und dort aktiv gepflegt werden
(README, Projekt-CLAUDE.md, aktive Specs), werden **nie kopiert**.
Referenz als `repo:<absoluter pfad zur datei>` in `sources:` bzw. im
Abschnitt „Live-Quellen". Wer Details braucht, liest dort — das Brain
hält nur Verdichtung + Pfad. Dynamische Fakten im Wiki immer mit
Stand-Datum.

## Wegwerf-Regel

Raw-Pflicht gilt für Quellen, aus denen faktische Aussagen ins Wiki
übernommen wurden. Reine Wegwerf-Notizen (Kontext-Dumps, erledigte
Zwischenpläne ohne übernommene Fakten) dürfen nach dem Ingest gelöscht
werden — die Entscheidung steht im Log.

## Widersprüche

Widerspruch gefunden → beide Aussagen bleiben stehen, Block direkt an
der Stelle:

```
> ⚠️ KONFLIKT (2026-01-31): Aussage A (Quelle X) vs. Aussage B (Quelle Y).
> Entscheidung offen — Owner.
```

Aufgelöst wird durch Reparatur der **Quelle** bzw. Entscheid des Owners,
dann Wiki nachziehen und Konfliktblock entfernen (Log-Eintrag).

## Log-Format (`log.md`, append-only)

```
## [YYYY-MM-DD] <op> | <betreff>
Ein bis drei Zeilen: was, warum, betroffene Seiten.
```

Ops: `init` · `handoff` · `ingest` · `lint` · `konflikt` · `entscheidung`
— grep-bar mit `grep "^## \[" log.md`.
