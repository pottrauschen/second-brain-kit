#!/usr/bin/env python3
"""Katalog-Generator: liest Frontmatter aller Wiki-/Maps-Seiten und
schreibt system/generated/catalog.md. Deterministisch und idempotent —
niemals von Hand editieren, immer neu generieren."""

import re
import sys
from pathlib import Path

BRAIN = Path(__file__).resolve().parents[2]
SCAN_DIRS = ["wiki", "maps"]
CATALOG = BRAIN / "system" / "generated" / "catalog.md"

FM_KEY = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
FM_LIST_ITEM = re.compile(r"^\s+-\s+(.*)$")


def parse_frontmatter(text: str):
    """Flaches YAML-Subset: 'key: value', Inline-Listen [a, b] und
    Strichlisten. Gibt (dict | None, body) zurück."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    fm, key = {}, None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fm, "\n".join(lines[i + 1:])
        m = FM_KEY.match(line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
            elif val == "":
                fm[key] = []
            else:
                fm[key] = val
            continue
        li = FM_LIST_ITEM.match(line)
        if li and key is not None and isinstance(fm.get(key), list):
            fm[key].append(li.group(1).strip())
    return None, text  # kein schließendes ---


def first_description(body: str) -> str:
    """Erste Überschrift oder erste Textzeile als Kurzbeschreibung."""
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        s = re.sub(r"^#+\s*", "", s)
        s = s.replace("|", "\\|")
        return s[:100]
    return ""


def main() -> int:
    rows = []
    for d in SCAN_DIRS:
        base = BRAIN / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            rel = p.relative_to(BRAIN).as_posix()
            fm, body = parse_frontmatter(p.read_text(encoding="utf-8"))
            fm = fm or {}
            rows.append(
                "| {} | {} | {} | {} | {} | {} |".format(
                    rel,
                    fm.get("type", "-"),
                    fm.get("project", "-"),
                    fm.get("status", "-"),
                    fm.get("updated", "-"),
                    first_description(body),
                )
            )
    out = "\n".join(
        [
            "# Katalog (generiert von brain_index.py — nie von Hand editieren)",
            "",
            "| Pfad | Typ | Projekt | Status | Aktualisiert | Kurzbeschreibung |",
            "|---|---|---|---|---|---|",
            *rows,
            "",
        ]
    )
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    old = CATALOG.read_text(encoding="utf-8") if CATALOG.exists() else None
    if old != out:
        CATALOG.write_text(out, encoding="utf-8", newline="\n")
        print(f"catalog.md aktualisiert ({len(rows)} Seiten)")
    else:
        print(f"catalog.md unverändert ({len(rows)} Seiten)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
