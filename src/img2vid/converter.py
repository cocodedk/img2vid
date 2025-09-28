"""Facade module exposing conversion helpers for external callers."""

from __future__ import annotations

from .helpers import (
    DEFAULT_FRAME_RATE,
    DEFAULT_TEXT_DURATION_MS,
    SUPPORTED_IMAGE_EXTENSIONS,
    ConversionConfig,
    ConversionError,
    list_image_files,
    resolve_output_path,
    render_video,
)

__all__ = [
    "DEFAULT_FRAME_RATE",
    "DEFAULT_TEXT_DURATION_MS",
    "SUPPORTED_IMAGE_EXTENSIONS",
    "ConversionConfig",
    "ConversionError",
    "list_image_files",
    "resolve_output_path",
    "render_video",
]
