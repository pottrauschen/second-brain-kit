# Second Brain — Wegweiser

Das Second Brain (Projekt-Kontext-System) liegt unter `<BRAIN>`.
Zwei Befehle:

- `/hole <projekt>` — Kontext laden; bei unbekanntem Projekt bietet der
  Befehl das Onboarding an
- `/handoff` — Session-Stand ins Brain sichern

Beginnt der Owner Projektarbeit ohne geladenen Kontext, weise **einmal**
kurz auf `/hole` hin (kein Zwang, kein Banner). Bei Meilensteinen
`/handoff` anbieten. Anleitung: `<BRAIN>/wiki/topics/anleitung.md`

Neue md-Dateien in Projekten folgen dem Doku-Standard: README und
CLAUDE.md (mit Doc-Map) im Root, **alles andere unter `docs/`**
(kebab-case, freie Namen); kein Session-Wissen als Datei — dafür
`/handoff`. Details: `<BRAIN>/wiki/topics/projekt-doku-standard.md`

Das Auto-Memory des Assistenten ist **kein** Ort für Projektwissen oder
Arbeitsregeln des Owners — beides gehört ins Brain (Cockpit,
`decisions.md`, `gotchas.md`). Sagt der Owner „merk dir das", ist die
Bitte zugleich die Write-Gate-Freigabe.
