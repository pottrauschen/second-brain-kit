Sichere den aktuellen Session-Stand ins Second Brain unter
`<BRAIN>`. Regeln des Brains beachten (`<BRAIN>/CLAUDE.md`).

1. **Projekt bestimmen:** `$ARGUMENTS`, falls leer: Name des aktuellen
   Arbeitsordners in kebab-case. Bei Unklarheit nachfragen.
2. **Bestehendes Cockpit lesen** (falls vorhanden):
   `<BRAIN>/wiki/projects/<projekt>/cockpit.md`.
3. **Cockpit aktualisieren bzw. anlegen** — verdichtet, keine
   Inhaltskopien aus Repo-Dateien, keine Code-Blöcke außer Einzeilern:
   - Frontmatter: `type: project-cockpit`, `project`, `status: active`,
     `updated: <heute>`, `sources:` (Live-Quellen als `repo:<pfad>`)
   - Abschnitte: **Stand** (3–6 Sätze) · **Entscheidungen** (mit Warum)
     · **Offene Punkte / Nächste Schritte** · **Stolperfallen** ·
     **Live-Quellen** (Pfade der wichtigen Repo-Dateien)
   - Überholtes ersetzen statt anhängen; Widersprüche zum Bestand als
     `⚠️ KONFLIKT`-Block markieren, nie still überschreiben.
   - Ziel: unter ~150 Zeilen. Wächst es darüber, Details in
     `decisions.md` / `gotchas.md` im selben Ordner auslagern.
4. **Doku-Standard prüfen — Pflicht, deterministisch:**
   ```
   python3-64.exe <BRAIN>/system/scripts/brain_doku_check.py <projektordner>
   ```
   Der Befund ist **verbindlich** — er wird nicht weginterpretiert.
   Jeder VERSTOSS kommt in eine Aufräum-Tabelle mit Vorschlag
   (einsortieren / umbenennen / ins Brain verdichten / löschen /
   begründete Ausnahme, die der Owner entscheidet). Exit 0 = eine Zeile
   „Doku-Standard: konform" im Handoff-Bericht, mit der geprüften
   Dateizahl. Bei Umzügen: Doc-Map, Querverweise und Brain-Live-Quellen
   mitziehen; bei uncommitteter Arbeit erst den Arbeitsstand committen,
   Umzug als eigener Commit. Nichts ohne Freigabe umsetzen.
   (Standard-Details: `<BRAIN>/wiki/topics/projekt-doku-standard.md`)
5. **Write-Gate:** Änderung kurz zeigen und Freigabe abwarten — außer
   der Owner hat sie in dieser Session bereits pauschal erteilt.
6. **Nach dem Schreiben:**
   - `python3-64.exe <BRAIN>/system/scripts/brain_index.py`
   - Log-Zeile an `<BRAIN>/log.md` anhängen:
     `## [YYYY-MM-DD] handoff | <projekt>` + 1–3 Zeilen Inhalt
   - `git -C <BRAIN> add -A`
   - `git -C <BRAIN> commit -m "handoff: <projekt>"`

Hinweis für dich: Handoffs gehören an Meilensteine, nicht erst an das
Token-Limit — biete sie proaktiv an, wenn Wesentliches entschieden wurde.
