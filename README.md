# second-brain-kit

Verpackt das Second Brain (Projekt-Kontext-System für die Arbeit mit
KI-Assistenten) in **eine Markdown-Datei**, die man jeder KI mit
Dateizugriff geben kann: `second-brain-bootstrap.md`. Die KI führt ein
kurzes Gespräch (Ordner, Werkzeug, Python, Git, Sprache, erstes Projekt)
und legt das Brain dann lokal an, samt Skripten, Verfassung und den zwei
Abläufen „Kontext laden" und „Handoff".

Kein Plugin, kein MCP, keine Installation: Datei weitergeben, fertig.
Claude Code bekommt zusätzlich die Slash-Befehle `/hole` und `/handoff`;
alle anderen Werkzeuge arbeiten über `AGENTS.md` im Brain-Ordner.

## Benutzen

Die Datei `second-brain-bootstrap.md` an die KI geben und sagen:
„Lies diese Datei und richte mir das Second Brain ein." Der Rest ist
Dialog.

## Bauen

Die Bootstrap-Datei wird nicht von Hand gepflegt, sondern aus den
Vorlagen zusammengesetzt:

```
python build_bootstrap.py
```

```
second-brain-kit/
├── build_bootstrap.py          setzt die Datei zusammen (stdlib, kein pip)
├── second-brain-bootstrap.md   Ergebnis, das weitergegeben wird
└── templates/
    ├── bootstrap-kopf.md       Teil A: Gesprächsleitfaden und Schritte für die KI
    ├── brain/                  Teil B: Dateien des Brains (Verfassung, Schema, Router,
    │                           Themen-Seiten, Skripte, AGENTS-Kopf)
    ├── ablaeufe/               hole.md, handoff.md (einmal als AGENTS.md, einmal als Befehle)
    └── claude/                 Abschnitt für die globale CLAUDE.md von Claude Code
```

Platzhalter in den Vorlagen: `<BRAIN>` (absoluter Pfad des Brains) und
`<PYTHON>` (Python-Aufruf); `python3-64.exe` in den Quellen wird beim
Bauen zu `<PYTHON>`. Die Vorlagen sind gegenüber dem privaten Brain
generalisiert: „Owner" statt Personenname, keine Bezüge auf andere
Instanzen oder Rechner.

## Herkunft

Die Skripte sind unverändert aus dem Live-Brain übernommen; Verfassung,
Schema und Themen-Seiten sind die Live-Fassungen ohne private Bezüge.
Änderungen an den Regeln gehören zuerst ins Live-Brain und dann per
Kopie in `templates/`, nicht umgekehrt.
