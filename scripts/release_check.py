"""Validate the local prerequisites for a DCMI release."""

from __future__ import annotations

import argparse
import importlib.metadata
import re
import subprocess
from pathlib import Path


def current_version() -> str:
    """Return the installed DCMI version."""
    return importlib.metadata.version("dcmi")


def changelog_contains_version(version: str) -> bool:
    """Return whether the changelog contains a section for version."""
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    return (
        re.search(rf"^## \[{re.escape(version)}\](?:\s|$)", changelog, re.MULTILINE)
        is not None
    )


def main() -> int:
    """Validate tag, working tree, and changelog state."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--changelog-only",
        action="store_true",
        help="only validate that the current version has a changelog section",
    )
    args = parser.parse_args()

    version = current_version()
    if not changelog_contains_version(version):
        raise SystemExit(
            f"CHANGELOG.md has no section for installed version {version}."
        )
    if args.changelog_only:
        print(f"CHANGELOG.md contains release {version}.")
        return 0

    tag = subprocess.run(
        ["git", "describe", "--tags", "--exact-match", "--match", "v[0-9]*"],
        check=False,
        capture_output=True,
        text=True,
    )
    if tag.returncode != 0 or tag.stdout.strip() != f"v{version}":
        raise SystemExit(f"Current commit must have tag v{version}.")

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    )
    if status.stdout:
        raise SystemExit("Working tree must be clean.")

    print(f"Release {version} is tagged on the current commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
