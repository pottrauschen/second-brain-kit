---
type: topic
status: active
updated: 2026-09-06
sources:
  - CLAUDE.md
---

# Projekt-Doku-Standard

Verbindlich für alle Coding-Projekte. Ziel: keine willkürlichen
md-Dateien — jede Datei hat festen Platz und Zweck. Session-Wissen
gehört ins Brain, nie als Datei ins Repo.

## Struktur (feste Kategorien)

```
<projekt>/
├─ README.md              # Pflicht: Was ist das, wie starten
├─ CLAUDE.md              # Pflicht: Arbeitsregeln + Doc-Map
└─ docs/                  # ALLE weiteren md-Dateien — freie Namen
   ├─ architektur.md      #   (Kategorien-Präfixe empfohlen, nicht
   ├─ spec-<feature>.md   #   Pflicht: spec-, anleitung-, referenz-;
   └─ server.md           #   docs/server.md ist genauso okay)
```

Konventionsdateien (CHANGELOG.md, CONTRIBUTING.md, LICENSE.md,
AGENTS.md) sind erlaubt, wenn das Projekt sie braucht — auch sie stehen
in der Doc-Map. **README.md in Unterordnern** (z. B. Code-README eines
Submoduls) ist Konvention und erlaubt. Andere Kategorien nur nach
bewusster Entscheidung (dann hier ergänzen).

## Regeln

1. **Doc-Map-Pflicht:** Jede md-Datei steht in der CLAUDE.md des
   Projekts — eine Zeile: Pfad + Zweck. Was nicht gelistet ist, gilt
   als verwaist und wird beim nächsten Handoff zur Klärung vorgelegt.
2. **Namen:** kebab-case. **Nie** Versionsnummern oder Datumsstempel im
   Namen — Historie macht Git. Kategorien-Präfixe (`spec-`,
   `anleitung-`, `referenz-`) sind Empfehlung, keine Pflicht: Ort hart,
   Namen weich.
3. **Kein Session-Wissen im Repo:** Stand, Entscheidungen, offene
   Punkte, Stolperfallen → Brain via Handoff. Dateien wie `NOTES.md`,
   `CONTEXT_v3.md`, `TODO_final.md` entstehen nicht mehr.
4. **Außerhalb von README, CLAUDE.md, docs/ und Konventionsdateien
   liegen keine md-Dateien.**

## Durchsetzung

- **Deterministisch:** `system/scripts/brain_doku_check.py <projektordner>`
  prüft Ort, Namen und Doc-Map maschinell — der Befund ist verbindlich.
  Eine weiche Prüfung durch das Modell übersieht erfahrungsgemäß
  Dateien im Projektroot.
- Die KI führt den Check bei jedem **Handoff** aus und legt jeden
  Verstoß als Aufräum-Tabelle vor (einsortieren / umbenennen / ins
  Brain verdichten / löschen / begründete Ausnahme). Umsetzung nur mit
  Freigabe (Write-Gate).
- **Begründete Ausnahmen** stehen in `.doku-check-ignore` im
  Projektroot (je Zeile ein Ordner-Präfix oder Glob, `#` = Kommentar
  mit Begründung + Freigabe-Datum). Der Check nimmt diese Pfade aus
  und weist die Zahl im Report aus. Gedacht für Werkstatt-Ordner, die
  laut Projekt-Spec md-Dateien führen (z. B. `skripte/` als
  Pipeline-Input, `work/` als Arbeitsmaterial) — nicht als Schlupfloch
  für unsortierte Doku.
- **Rollout bestehender Projekte:** beim jeweils nächsten Handoff pro
  Projekt — kein Big-Bang.
- Beim **Onboarding** (Kontext laden für ein unbekanntes Projekt) werden
  code-gekoppelte Dateien direkt in den Standard einsortiert.
