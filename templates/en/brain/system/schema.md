# Schema — page types, front matter, rules

## Folder semantics

| Folder | Meaning | Who writes |
|---|---|---|
| `raw/` | Immutable evidence (archived session artefacts, source documents) | import workflow only, then frozen |
| `inbox/` | Intake — waiting to be processed | owner drops files, ingest clears them |
| `wiki/` | Derived, maintained knowledge — the only place that is curated | AI (with write gate) |
| `maps/` | Retrieval routers (small signpost pages) | AI (with write gate) |
| `system/` | Rules, scripts, generated files | scripts; rules only on request |

## Front matter (required for every page under `wiki/`)

```yaml
---
type: project-cockpit | decision | topic | source | note
project: my-project       # required for project-cockpit, otherwise optional
status: active | done | stale
updated: 2026-01-31       # set on every substantive change
sources: []               # evidence: raw/<path> or repo:<absolute path>
---
```

## Page types

- **project-cockpit** (`wiki/projects/<name>/cockpit.md`): entry page of a
  project. Sections: State (3–6 sentences) · Decisions (with their why) ·
  Open points / next steps · Pitfalls · Live sources. Target: under ~150
  lines — move details to their own pages (`decisions.md`, `gotchas.md`)
  when it grows.
- **decision**: one important decision with context, alternatives,
  reasoning, date.
- **topic** (`wiki/topics/`): technical knowledge across projects.
- **source** (`wiki/sources/`): condensation of exactly one source from
  `raw/`.
- **note**: everything else that is small.

## Live-source rule

Files that belong to a code repo and are actively maintained there
(README, project CLAUDE.md, active specs) are **never copied**. Reference
them as `repo:<absolute path to the file>` in `sources:` or in the
section "Live sources". Whoever needs details reads there — the brain
keeps only the condensation plus the path. Dynamic facts in the wiki
always carry an as-of date.

## Throwaway rule

The raw obligation applies to sources from which factual statements were
taken into the wiki. Pure throwaway notes (context dumps, finished
interim plans without adopted facts) may be deleted after ingest — the
decision is recorded in the log.

## Contradictions

Contradiction found → both statements stay, block right at the spot:

```
> ⚠️ CONFLICT (2026-01-31): statement A (source X) vs. statement B (source Y).
> Decision open — owner.
```

Resolved by repairing the **source** or by the owner's decision, then
update the wiki and remove the conflict block (log entry).

## Log format (`log.md`, append-only)

```
## [YYYY-MM-DD] <op> | <subject>
One to three lines: what, why, pages affected.
```

Ops: `init` · `handoff` · `ingest` · `lint` · `conflict` · `decision`
— greppable with `grep "^## \[" log.md`.
