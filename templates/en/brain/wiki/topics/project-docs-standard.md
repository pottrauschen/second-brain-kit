---
type: topic
status: active
updated: 2026-09-06
sources:
  - CLAUDE.md
---

# Project docs standard

Binding for all coding projects. Goal: no arbitrary md files — every
file has a fixed place and purpose. Session knowledge belongs in the
brain, never as a file in the repo.

## Structure (fixed categories)

```
<project>/
├─ README.md              # required: what is this, how to start
├─ CLAUDE.md              # required: working rules + doc map
└─ docs/                  # ALL other md files — free names
   ├─ architecture.md     #   (category prefixes recommended, not
   ├─ spec-<feature>.md   #   required: spec-, guide-, reference-;
   └─ server.md           #   docs/server.md is just as fine)
```

Convention files (CHANGELOG.md, CONTRIBUTING.md, LICENSE.md, AGENTS.md)
are allowed when the project needs them — they too appear in the doc
map. **README.md in subfolders** (e.g. the code README of a submodule) is
convention and allowed. Other categories only after a deliberate decision
(then add them here).

## Rules

1. **Doc-map obligation:** every md file is listed in the project's
   CLAUDE.md — one line: path + purpose. What is not listed counts as
   orphaned and is brought up for clarification at the next handoff.
2. **Names:** kebab-case. **Never** version numbers or date stamps in
   names — Git keeps the history. Category prefixes (`spec-`, `guide-`,
   `reference-`) are a recommendation, not a requirement: place is
   strict, names are loose.
3. **No session knowledge in the repo:** state, decisions, open points,
   pitfalls → brain via handoff. Files like `NOTES.md`, `CONTEXT_v3.md`,
   `TODO_final.md` no longer come into being.
4. **No md files outside README, CLAUDE.md, docs/ and convention files.**

## Enforcement

- **Deterministic:** `system/scripts/brain_doku_check.py <project folder>`
  checks place, names and doc map mechanically — the finding is binding.
  A soft check by the model tends to miss files in the project root.
- The AI runs the check at every **handoff** and presents every violation
  as a clean-up table (file / rename / condense into the brain / delete /
  justified exception). Changes only with approval (write gate).
- **Justified exceptions** live in `.doku-check-ignore` in the project
  root (one folder prefix or glob per line, `#` = comment with reasoning
  + approval date). The check excludes those paths and reports their
  number. Meant for workshop folders that hold md files by design (e.g.
  `scripts/` as pipeline input, `work/` as working material) — not as a
  loophole for unsorted docs.
- **Rollout for existing projects:** at each project's next handoff — no
  big bang.
- During **onboarding** (getting the context for an unknown project),
  code-coupled files are sorted straight into the standard.
