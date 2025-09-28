"""Image collection and video clip assembly helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Sequence

from moviepy import ImageClip, concatenate_videoclips
from moviepy.video.fx import CrossFadeIn

from .config import DEFAULT_FRAME_RATE, ConversionError, SUPPORTED_IMAGE_EXTENSIONS

logger = logging.getLogger(__name__)


def list_image_files(input_dir: Path) -> List[Path]:
    """Return sorted image files supported by the converter."""

    image_files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )

    if not image_files:
        raise ConversionError(
            f"No supported images found in {input_dir}. Supported extensions: {sorted(SUPPORTED_IMAGE_EXTENSIONS)}"
        )

    return image_files


def build_video_clip(
    image_files: Sequence[Path],
    frame_duration_ms: int,
    transition_ms: int,
    frame_rate: int = DEFAULT_FRAME_RATE,
):
    """Create a MoviePy video clip from the provided image paths."""

    frame_duration = frame_duration_ms / 1000.0
    transition_duration = transition_ms / 1000.0

    clips = []
    total = len(image_files)
    for index, image_path in enumerate(image_files):
        logger.info("Adding image %s (%d/%d)", image_path.name, index + 1, total)
        clip = ImageClip(str(image_path), duration=frame_duration)
        if transition_duration > 0 and index != 0:
            clip = clip.with_effects([CrossFadeIn(transition_duration)])
        clips.append(clip)

    padding = -transition_duration if transition_duration > 0 else 0
    video_clip = concatenate_videoclips(
        clips,
        method="compose",
        padding=padding,
    )
    return video_clip.with_fps(frame_rate)
