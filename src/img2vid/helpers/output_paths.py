"""Utilities for computing versioned output locations."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

DEFAULT_OUTPUT_ROOT = Path("build")


def resolve_output_path(
    *,
    input_dir: Path,
    explicit_output: Optional[Path],
    output_root: Optional[Path],
    output_basename: Optional[str],
    extension: str = ".mp4",
) -> Path:
    """Return an output file path honoring versioned folders.

    The layout is ``<root>/<source-folder>/v###/<basename><ext>`` where
    ``v###`` is the first version whose target file does not yet exist.
    """

    if explicit_output is not None:
        return explicit_output

    root = output_root or DEFAULT_OUTPUT_ROOT
    source_name = input_dir.resolve().name
    base_name = (output_basename or source_name).strip() or source_name

    version = 1
    while True:
        candidate_dir = root / source_name / f"v{version:03d}"
        candidate_path = candidate_dir / f"{base_name}{extension}"
        if not candidate_path.exists():
            return candidate_path
        version += 1
