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

## Einrichten je Werkzeug

Voraussetzung ist immer dasselbe: ein KI-Werkzeug, das **Dateien auf
deinem Rechner lesen und schreiben** kann. Dazu Python 3 (beliebige
Version, keine Pakete) und möglichst Git. Die KI prüft beides selbst im
Gespräch und sagt, was fehlt.

Was die Einrichtung anlegt, hängt vom Werkzeug ab:

| Werkzeug | Bekommt | Auslösen |
|---|---|---|
| Claude Code | `/get`, `/handoff` als Slash-Befehle (global in `~/.claude/commands/`) plus Wegweiser in `~/.claude/CLAUDE.md` | `/get <projekt>` · `/handoff` |
| alle anderen | `AGENTS.md` im Brain-Ordner mit beiden Abläufen im Wortlaut | zwei Sätze, siehe unten |

Die zwei Sätze für alle Werkzeuge ohne Slash-Befehle:

```
Lies <BRAIN>/AGENTS.md und lade den Kontext für <projekt>
Lies <BRAIN>/AGENTS.md und mach einen Handoff für <projekt>
```

`<BRAIN>` ist der Pfad des Brain-Ordners, z. B. `~/SecondBrain`.

### Claude Code (CLI, Desktop-App, VS Code, JetBrains)

1. `second-brain-bootstrap.de.md` herunterladen, irgendwohin legen.
2. Claude Code in einem beliebigen Ordner öffnen und schreiben:
   „Lies `<pfad>/second-brain-bootstrap.de.md` und richte mir das Second
   Brain ein."
3. Fragen beantworten (Ordner, Werkzeug: Claude Code, Python, Git,
   Sprache, erstes Projekt). Die KI zeigt vor dem Schreiben eine
   Zusammenfassung und wartet auf dein Ja.
4. Danach in jeder Session: `/get <projekt>` am Anfang, `/handoff` an
   Meilensteinen. Für ein unbekanntes Projekt startet `/get` das
   Onboarding.

Die Slash-Befehle liegen global unter `~/.claude/commands/`, gelten also
in jedem Projektordner. Bestehende Dateien dort werden nie stumm
überschrieben, die KI zeigt sie und fragt.

### Codex (OpenAI)

**ChatGPT im Browser reicht nicht**, es hat keinen Dateizugriff. Du
brauchst die Codex-CLI oder die Codex-App auf dem Rechner.

1. Codex im Zielordner starten und den Satz aus Schritt 2 oben sagen.
   Bei der Frage nach dem Werkzeug „Codex" antworten.
2. Auslösen mit den zwei Sätzen. Codex liest eine `AGENTS.md` im
   Arbeitsordner automatisch; startest du Codex direkt im Brain-Ordner,
   kennt es die Abläufe schon. Für Projektordner bietet die KI an, dort
   einen Zweizeiler mit Verweis auf `<BRAIN>/AGENTS.md` einzutragen.

Codex kann auch schreiben, das Write-Gate gilt genauso: Die KI zeigt die
Cockpit-Änderung, du gibst frei.

### Gemini CLI, Copilot CLI, Cursor, Aider

Gleicher Weg wie bei Codex, mit den zwei Sätzen. Unterschiede beim
automatischen Lesen der Regeldatei:

- **Gemini CLI** liest standardmäßig `GEMINI.md`, nicht `AGENTS.md`. Lass
  die KI beim Einrichten einen Verweis auf `<BRAIN>/AGENTS.md` in deine
  `~/.gemini/GEMINI.md` schreiben, oder nenne den Pfad in jedem Satz.
- **Copilot CLI** liest `copilot-instructions.md` und in aktuellen
  Versionen auch `AGENTS.md`. Im Zweifel: Pfad im Satz nennen.
- **Cursor** liest `.cursorrules` bzw. `.cursor/rules` im Projekt; ein
  Zweizeiler mit Verweis genügt.

Werkzeuge, die keine Regeldatei kennen, funktionieren trotzdem: Der Satz
mit dem Pfad ist die ganze Schnittstelle.

### Zed

Zed bindet Claude Code, Codex und Gemini CLI als externe Agenten ein
(Agent Panel, ACP). Das Brain funktioniert dort mit denselben Dateien,
mit einer Stolperfalle: Zed fängt Nachrichten ab, die mit `/` beginnen,
die Slash-Befehle von Claude Code kommen dort also nicht an. In Zed
deshalb immer die zwei Sätze mit dem Pfad benutzen; die `AGENTS.md`
liegt in jedem Brain, auch wenn nur Claude Code eingerichtet wurde.

### Mehrere Werkzeuge zugleich

Geht, ist der Normalfall. Alle lesen denselben Brain-Ordner. Empfehlung
aus der Praxis: schreiben lassen nur die Werkzeuge, bei denen du das
Write-Gate wirklich siehst (Claude Code, Codex); Agenten, die mit
Vollzugriff laufen, nur lesen lassen. Beim Einrichten „mehrere" angeben,
dann legt die KI Slash-Befehle und `AGENTS.md` an.

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

## Lizenz

MIT, siehe `LICENSE`.
