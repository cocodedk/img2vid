"""Context helpers for controlling MoviePy temporary directories."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from moviepy import config as moviepy_config


@contextmanager
def temporary_directory(root: Path) -> Iterator[Path]:
    """Temporarily point MoviePy to ``root`` for staging files."""

    root.mkdir(parents=True, exist_ok=True)
    previous_default = getattr(moviepy_config, "DEFAULT_TEMP_DIR", None)
    moviepy_config.DEFAULT_TEMP_DIR = str(root)
    try:
        yield root
    finally:
        moviepy_config.DEFAULT_TEMP_DIR = previous_default
