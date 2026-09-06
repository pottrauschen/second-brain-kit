Save the current session state into the Second Brain under
`<BRAIN>`. Respect the rules of the brain (`<BRAIN>/CLAUDE.md`).

1. **Determine the project:** `$ARGUMENTS`; if empty, the name of the
   current working folder in kebab-case. Ask if unclear.
2. **Read the existing cockpit** (if any):
   `<BRAIN>/wiki/projects/<project>/cockpit.md`.
3. **Update or create the cockpit** — condensed, no content copies from
   repo files, no code blocks except one-liners:
   - Front matter: `type: project-cockpit`, `project`, `status: active`,
     `updated: <today>`, `sources:` (live sources as `repo:<path>`)
   - Sections: **State** (3–6 sentences) · **Decisions** (with their why)
     · **Open points / next steps** · **Pitfalls** · **Live sources**
     (paths of the important repo files)
   - Replace what is outdated instead of appending; mark contradictions
     with the existing content as a `⚠️ CONFLICT` block, never overwrite
     silently.
   - Target: under ~150 lines. If it grows beyond that, move details to
     `decisions.md` / `gotchas.md` in the same folder.
4. **Check the docs standard — mandatory, deterministic:**
   ```
   python3-64.exe <BRAIN>/system/scripts/brain_doku_check.py <project folder>
   ```
   The finding is **binding** — it is not explained away. Every
   VIOLATION goes into a clean-up table with a proposal (file / rename /
   condense into the brain / delete / justified exception, which the
   owner decides). Exit 0 = one line "Docs standard: compliant" in the
   handoff report, with the number of files checked. When moving files:
   update the doc map, cross-references and the brain's live sources; with
   uncommitted work, commit the working state first, the move as its own
   commit. Change nothing without approval.
   (Details of the standard: `<BRAIN>/wiki/topics/project-docs-standard.md`)
5. **Write gate:** show the change briefly and wait for approval — unless
   the owner has already granted it for this session as a whole.
6. **After writing:**
   - `python3-64.exe <BRAIN>/system/scripts/brain_index.py`
   - Append a log line to `<BRAIN>/log.md`:
     `## [YYYY-MM-DD] handoff | <project>` + 1–3 lines of content
   - `git -C <BRAIN> add -A`
   - `git -C <BRAIN> commit -m "handoff: <project>"`

Note for you: handoffs belong at milestones, not at the token limit —
offer them proactively when something substantial has been decided.
