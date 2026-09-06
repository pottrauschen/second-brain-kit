# Second Brain — signpost

The Second Brain (project-context system) lives at `<BRAIN>`.
Two commands:

- `/get <project>` — get the context; for an unknown project the command
  offers the onboarding
- `/handoff` — save the session state into the brain

If the owner starts project work without loaded context, point to `/get`
**once**, briefly (no pressure, no banner). Offer `/handoff` at
milestones. Guide: `<BRAIN>/wiki/topics/guide.md`

New md files in projects follow the docs standard: README and CLAUDE.md
(with doc map) in the root, **everything else under `docs/`**
(kebab-case, free names); no session knowledge as a file — use
`/handoff` for that. Details: `<BRAIN>/wiki/topics/project-docs-standard.md`

The assistant's auto-memory is **not** the place for project knowledge or
the owner's working rules — both belong in the brain (cockpit,
`decisions.md`, `gotchas.md`). When the owner says "remember this", that
request is also the write-gate approval.
