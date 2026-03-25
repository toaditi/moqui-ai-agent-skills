#!/usr/bin/env python3
"""Copy selected skills from this repo into an agent skills directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def discover_skills(repo_root: Path) -> dict[str, Path]:
    skills: dict[str, Path] = {}
    for path in sorted(repo_root.iterdir()):
        if path.is_dir() and (path / "SKILL.md").exists():
            skills[path.name] = path
    return skills


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync selected skill folders from this repo into a target skills directory."
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Specific skill folder names to sync. Defaults to all discovered skills.",
    )
    parser.add_argument(
        "--dest",
        default=str(Path.home() / ".codex" / "skills"),
        help="Destination skills directory. Defaults to ~/.codex/skills",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available skills and exit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing anything.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    available = discover_skills(repo_root)

    if args.list:
        for skill_name in available:
            print(skill_name)
        return 0

    selected_names = args.skills or list(available.keys())
    missing = [name for name in selected_names if name not in available]
    if missing:
        print(f"Unknown skill(s): {', '.join(missing)}", file=sys.stderr)
        print("Use --list to see available skills.", file=sys.stderr)
        return 1

    destination = Path(args.dest).expanduser().resolve()
    if not args.dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    for skill_name in selected_names:
        source = available[skill_name]
        target = destination / skill_name
        print(f"{source} -> {target}")
        if args.dry_run:
            continue
        shutil.copytree(source, target, dirs_exist_ok=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
