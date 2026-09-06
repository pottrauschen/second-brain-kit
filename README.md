# second-brain-kit

Verpackt das Second Brain (Projekt-Kontext-System für die Arbeit mit
KI-Assistenten) in **eine Markdown-Datei je Sprache**, die man jeder KI
mit Dateizugriff geben kann:

- `second-brain-bootstrap.de.md` (deutsch)
- `second-brain-bootstrap.en.md` (englisch)

Die KI führt ein kurzes Gespräch (Ordner, Werkzeug, Python, Git, Sprache,
erstes Projekt) und legt das Brain dann lokal an, samt Skripten,
Verfassung und den zwei Abläufen „Kontext laden" (`/get`) und „Handoff".

Kein Plugin, kein MCP, keine Installation: Datei weitergeben, fertig.
Claude Code bekommt die Slash-Befehle `/get` und `/handoff`; alle anderen
Werkzeuge arbeiten über `AGENTS.md` im Brain-Ordner.

## Benutzen

Die passende Datei an die KI geben und sagen: „Lies diese Datei und
richte mir das Second Brain ein." Der Rest ist Dialog.

## Bauen

Die Bootstrap-Dateien werden nicht von Hand gepflegt, sondern aus den
Vorlagen zusammengesetzt:

```
python build_bootstrap.py
```

```
second-brain-kit/
├── build_bootstrap.py              setzt beide Dateien zusammen (stdlib, kein pip)
├── second-brain-bootstrap.de.md    Ergebnis deutsch
├── second-brain-bootstrap.en.md    Ergebnis englisch
└── templates/
    ├── scripts/                    die drei Skripte, gemeinsam für beide Sprachen
    ├── de/                         deutsche Vorlagen
    │   ├── bootstrap-kopf.md       Teil A: Gesprächsleitfaden und Schritte für die KI
    │   ├── brain/                  Teil B: Verfassung, Schema, Router, Log, Themen-Seiten, AGENTS-Kopf
    │   ├── ablaeufe/               get.md, handoff.md (einmal als AGENTS.md, einmal als Befehle)
    │   └── claude/                 Abschnitt für die globale CLAUDE.md von Claude Code
    └── en/                         dieselbe Struktur auf Englisch (Themen: guide.md, project-docs-standard.md)
```

Platzhalter in den Vorlagen: `<BRAIN>` (absoluter Pfad des Brains) und
`<PYTHON>` (Python-Aufruf); `python3-64.exe` in den Quellen wird beim
Bauen zu `<PYTHON>`. Die Skripte lesen ihre Sprache zur Laufzeit aus
`<BRAIN>/system/lang` (`de` oder `en`, ohne Datei deutsch); das Bau-Skript
erzeugt diese Datei je Sprache.

Die Vorlagen sind gegenüber dem privaten Brain generalisiert: „Owner"
statt Personenname, keine Bezüge auf andere Instanzen oder Rechner.

## Herkunft

Die Skripte sind die des Live-Brains, ergänzt um den Sprachschalter;
Verfassung, Schema und Themen-Seiten sind die Live-Fassungen ohne private
Bezüge, die englischen Vorlagen sind Übersetzungen davon. Änderungen an
den Regeln gehören zuerst ins Live-Brain und dann in beide Sprachordner,
nicht umgekehrt.
