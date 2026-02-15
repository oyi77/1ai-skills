#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / ".sisyphus" / "evidence" / "skills"
REQUIRED_FILES = ["baseline.md", "with-skill.md", "notes.md"]


def discover_skill_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("SKILL.md") if path.is_file())


def skill_slug(skill_path: Path, root: Path) -> str:
    rel_dir = skill_path.relative_to(root).parent.as_posix()
    return rel_dir.replace("/", "--")


def missing_evidence_paths(root: Path) -> list[str]:
    missing: list[str] = []
    for skill_path in discover_skill_files(root):
        slug = skill_slug(skill_path, root)
        for filename in REQUIRED_FILES:
            target = EVIDENCE_ROOT / slug / filename
            if not target.exists():
                missing.append(target.relative_to(root).as_posix())
    return sorted(missing)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check required skill evidence files")
    parser.add_argument(
        "--check", action="store_true", help="Verify all evidence files exist"
    )
    args = parser.parse_args()

    if not args.check:
        parser.error("Specify --check")

    missing = missing_evidence_paths(ROOT)
    for path in missing:
        print(path)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
