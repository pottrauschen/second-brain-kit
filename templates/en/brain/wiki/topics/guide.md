---
type: topic
status: active
updated: 2026-09-06
sources:
  - CLAUDE.md
  - system/schema.md
---

# Guide — how to use your Second Brain

## Start a session: get the context

In Claude Code (any folder, typically your project folder):

```
/get <project-name>
```

In other tools (Codex, Cursor, Gemini CLI, Aider …) say it in plain
words instead: "Read `<BRAIN>/AGENTS.md` and get the context for
<project-name>." The routine is the same.

The AI loads only the project's small cockpit page, summarises state,
decisions and open points, and asks what to work on. No more feeding
context by hand.

## Work: as usual

Nothing new to learn — work with the AI in the project as you always do.

## Save the state: at milestones, not when tokens run out

```
/handoff
```

(or: "Read `<BRAIN>/AGENTS.md` and do a handoff for <project-name>.")
The AI condenses the session state, shows the change for approval (write
gate) and then does the rest: write the cockpit, regenerate the index,
log line, Git commit. For a new project the handoff creates the cockpit
page — that is how projects enter the brain.

## Put knowledge in

Drop files (notes, chat exports, documents) into `inbox/` and say in a
session: "Condense this into the brain." The AI proposes a wiki page, you
approve, the original moves to `raw/` as evidence.

## Get knowledge out

Just ask — in a session in the brain folder or after getting the
context. The AI follows the search ladder (router → one targeted page)
and never loads everything.

## What you never touch

- `raw/` — frozen evidence (the lint complains about changes)
- `system/generated/` — produced by scripts

## Health check when needed

```
cd <BRAIN>
python3-64.exe system/scripts/brain_lint.py
```

Also runs as part of the end-of-session checklist.

## Rules in detail

Constitution: `CLAUDE.md` · page types and schema: `system/schema.md` ·
the routines verbatim: `AGENTS.md`.
