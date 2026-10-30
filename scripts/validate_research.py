#!/usr/bin/env python3
"""Validate the specdocz research catalog and its index integrity.

Standard-library only. Checks structure and links; not scholarly truth or runtime claims.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_catalog(text: str) -> list[dict[str, str]]:
    require(re.search(r"(?m)^schema_version:\s*1\s*$", text) is not None,
            "research/catalog.yaml requires schema_version: 1")
    entries = []
    for block in re.split(r"(?m)^  - id:\s*", text)[1:]:
        lines = block.splitlines()
        study_id = lines[0].strip()
        entry = {"id": study_id}
        for key in ("path", "index", "status", "normative"):
            match = re.search(rf"(?m)^    {key}:\s*(\S.*?)\s*$", block)
            require(match is not None, f"{study_id}: catalog missing {key}")
            entry[key] = match.group(1).strip("'\"")
        entries.append(entry)
    require(bool(entries), "research/catalog.yaml has no registered studies")
    require(len({x["id"] for x in entries}) == len(entries),
            "research/catalog.yaml has duplicate study IDs")
    return entries


def check_relative_links(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    count = 0
    for target in re.findall(r"\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)", content):
        if target.startswith(("https://", "http://", "mailto:", "#", "data:")):
            continue
        target_path = unquote(target.split("#", 1)[0])
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        require(resolved.is_relative_to(ROOT), f"{path.relative_to(ROOT)}: link escapes repository: {target}")
        require(resolved.exists(), f"{path.relative_to(ROOT)}: broken link: {target}")
        count += 1
    return count


def check_study(entry: dict[str, str]) -> None:
    study_id = entry["id"]
    require(re.fullmatch(r"RESEARCH-[A-Z0-9]+-\d{3}", study_id) is not None,
            f"invalid research study ID: {study_id}")
    require(entry["normative"] == "false", f"{study_id}: research must be non-normative")
    for key in ("path", "index"):
        rel = Path(entry[key])
        require(not rel.is_absolute() and ".." not in rel.parts,
                f"{study_id}: unsafe {key}: {entry[key]}")
        f = (RESEARCH / rel).resolve()
        require(f.is_relative_to(RESEARCH) and f.is_file(),
                f"{study_id}: missing {key}: {entry[key]}")
    study = (RESEARCH / entry["path"]).read_text(encoding="utf-8")
    require(study.startswith("---\n") and "\n---\n" in study[4:],
            f"{study_id}: missing document front matter")
    front = study.split("---", 2)[1]
    for key in ("title", "document_type", "version", "research_cutoff", "status"):
        require(re.search(rf"(?m)^{key}:\s*\S+", front) is not None,
                f"{study_id}: front matter missing {key}")
    require(not re.search(r"(?m)^normative:\s*true\s*$", front),
            f"{study_id}: a research document cannot declare itself normative")

    # The first imported study retains its historical front matter and complete
    # original source register. The detached source listing is a checked extract.
    if study_id == "RESEARCH-ZPL-001":
        source_file = (RESEARCH / "zero-player-level-design/sources.md").read_text(encoding="utf-8")
        annotations = re.findall(r"(?m)^- \*\*\[S\d{2}\].*$", study)
        copied = re.findall(r"(?m)^- \*\*\[S\d{2}\].*$", source_file)
        require(len(annotations) == 21, "RESEARCH-ZPL-001: expected 21 annotated sources")
        require(annotations == copied, "RESEARCH-ZPL-001: source index diverged from canonical study")
        source_ids = [re.search(r"\[S\d{2}\]", line).group(0) for line in annotations]
        require(len(set(source_ids)) == len(source_ids), "RESEARCH-ZPL-001: duplicate source ID")
        patterns = set(re.findall(r"\bZP-P\d{2}\b", study))
        pattern_index = (RESEARCH / "zero-player-level-design/patterns.md").read_text(encoding="utf-8")
        require(len(patterns) == 11, "RESEARCH-ZPL-001: expected 11 patterns")
        require(patterns == set(re.findall(r"\bZP-P\d{2}\b", pattern_index)),
                "RESEARCH-ZPL-001: pattern index diverged from canonical study")


def main() -> int:
    try:
        catalog = (RESEARCH / "catalog.yaml").read_text(encoding="utf-8")
        studies = parse_catalog(catalog)
        for entry in studies:
            check_study(entry)
        markdown = [ROOT / "README.md", *RESEARCH.rglob("*.md")]
        for path in markdown:
            require(path.is_file(), f"missing markdown document: {path}")
        checked = sum(check_relative_links(path) for path in markdown)
        print(f"Research validation PASSED: {len(studies)} studies; "
              f"{len(markdown)} markdown documents; {checked} local links checked.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Research validation FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
