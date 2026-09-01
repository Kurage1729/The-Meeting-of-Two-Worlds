#!/usr/bin/env python3
"""Build one deterministic GPT-readable file from the canonical TMTW wiki."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "context" / "all-context.md"

EXCLUDED_DIRECTORIES = {
    ".git",
    ".github",
    "_drafts",
    "context",
    "scripts",
}

EXCLUDED_ROOT_FILES = {
    "AI-WORKFLOW-JA.md",
    "README.md",
    "STRUCTURE.md",
}

ROOT_PRIORITY = {
    "index.md": 0,
    "overview.md": 1,
    "timeline.md": 2,
}

DIRECTORY_PRIORITY = {
    "regions": 10,
    "countries": 20,
    "polities": 30,
    "history": 40,
    "culture": 50,
    "people": 60,
    "maps": 70,
}


def is_canonical(path: Path) -> bool:
    relative = path.relative_to(ROOT)

    if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
        return False

    if len(relative.parts) == 1 and relative.name in EXCLUDED_ROOT_FILES:
        return False

    return path.suffix.lower() == ".md"


def sort_key(path: Path) -> tuple[int, int, str]:
    relative = path.relative_to(ROOT)
    relative_text = relative.as_posix()

    if len(relative.parts) == 1:
        return (ROOT_PRIORITY.get(relative.name, 5), 0, relative_text)

    directory = relative.parts[0]
    index_priority = 0 if relative.name == "index.md" else 1
    return (DIRECTORY_PRIORITY.get(directory, 90), index_priority, relative_text)


def collect_sources() -> list[Path]:
    return sorted(
        (path for path in ROOT.rglob("*.md") if is_canonical(path)),
        key=sort_key,
    )


def build_document(sources: list[Path]) -> str:
    source_list = "\n".join(
        f"- `{path.relative_to(ROOT).as_posix()}`" for path in sources
    )

    sections: list[str] = [
        "# TMTW Complete Canonical Context",
        "",
        "> This file is generated automatically. Do not edit it directly.",
        "> Edit the original wiki pages instead.",
        "",
        "## Instructions for AI",
        "",
        "- Treat the material below as the canonical TMTW setting.",
        "- Material in `_drafts/` is deliberately excluded and is not canonical.",
        "- Text explicitly marked `TBD`, `provisional`, `unnamed`, or similar remains undecided.",
        "- If two canonical pages conflict, report the conflict instead of silently choosing one.",
        "- When proposing a change, identify every canonical page that would need updating.",
        "- The user may discuss the setting in Japanese even though the canonical wiki is in English.",
        "",
        "## Included source files",
        "",
        source_list,
        "",
    ]

    for path in sources:
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8").strip()
        sections.extend(
            [
                "---",
                "",
                f"# SOURCE FILE: `{relative}`",
                "",
                content,
                "",
            ]
        )

    return "\n".join(sections).rstrip() + "\n"


def main() -> None:
    sources = collect_sources()

    if not sources:
        raise SystemExit("No canonical Markdown files were found.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_document(sources), encoding="utf-8", newline="\n")
    print(f"Generated {OUTPUT.relative_to(ROOT)} from {len(sources)} files.")


if __name__ == "__main__":
    main()

