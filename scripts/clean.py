"""Remove generated DCMI files after an optional confirmation."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def remove_path(path: Path) -> bool:
    """Remove a file, directory, or symbolic link if it exists."""
    if not path.exists() and not path.is_symlink():
        return False
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def remove_matching_files(root: Path, pattern: str) -> int:
    """Remove files below root matching a glob pattern."""
    return sum(
        remove_path(path)
        for path in root.rglob(pattern)
        if path.is_file() and not is_virtual_environment_path(root, path)
    )


def remove_matching_directories(root: Path, directory_name: str) -> int:
    """Remove directories below root with the given name."""
    return sum(
        remove_path(path)
        for path in root.rglob(directory_name)
        if path.is_dir() and not is_virtual_environment_path(root, path)
    )


def is_virtual_environment_path(root: Path, path: Path) -> bool:
    """Return whether path is inside a project virtual environment."""
    relative_parts = path.relative_to(root).parts
    return ".venv" in relative_parts


def clean_generated_files(root: Path) -> int:
    """Remove generated project files and return the number of removed paths."""
    removed = 0
    for relative_path in (
        "logs",
        "build",
        "dist",
        "examples/output",
        "docs/_build",
        "htmlcov",
    ):
        removed += int(remove_path(root / relative_path))

    for path in root.glob("*.egg-info"):
        removed += int(remove_path(path))

    removed += remove_matching_files(root, "*.pyc")
    removed += remove_matching_files(root, "*.spec")
    removed += remove_matching_directories(root, "__pycache__")
    removed += remove_matching_directories(root, "log")
    removed += remove_matching_directories(root, ".pytest_cache")
    removed += remove_matching_directories(root, ".ruff_cache")

    for path in (root / ".coverage",):
        removed += int(remove_path(path))
    removed += sum(int(remove_path(path)) for path in root.glob(".coverage.*"))
    return removed


def main() -> int:
    """Prompt for confirmation and remove generated project files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--yes", action="store_true", help="skip confirmation")
    args = parser.parse_args()

    if not args.yes:
        answer = input(
            "WARNING: This will permanently delete generated files, caches, and logs. "
            "Continue? [y/n] "
        )
        if answer.strip().lower() != "y":
            print("Clean cancelled.")
            return 0

    root = Path(__file__).resolve().parents[1]
    removed = clean_generated_files(root)
    print(f"Project cleaned successfully. Removed {removed} paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
