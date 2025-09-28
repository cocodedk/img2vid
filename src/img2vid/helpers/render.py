"""High-level rendering orchestration for image-to-video conversion."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

from moviepy import concatenate_videoclips

from .audio import attach_audio
from .config import ConversionConfig
from .images import build_video_clip, list_image_files
from .overlays import create_text_overlay_clip

logger = logging.getLogger(__name__)


def render_video(config: ConversionConfig) -> Path:
    """Render a video based on the provided config and return the output path."""

    config.validate()
    image_files = list_image_files(config.input_dir)
    total_images = len(image_files)
    logger.info("Found %d image(s) to process", total_images)

    video_clip = build_video_clip(
        image_files=image_files,
        frame_duration_ms=config.frame_duration_ms,
        transition_ms=config.transition_ms,
        frame_rate=config.frame_rate,
    )

    transition_seconds = config.transition_ms / 1000.0
    text_duration_seconds = config.text_duration_ms / 1000.0

    frame_size = video_clip.size

    start_clip = create_text_overlay_clip(
        text=config.start_text,
        frame_size=frame_size,
        duration_seconds=text_duration_seconds,
        transition_seconds=transition_seconds,
        font_path=config.text_font,
        font_size=config.text_font_size,
        text_color=config.text_color,
        bg_color=config.text_bg_color,
    )
    if start_clip is not None:
        video_clip = concatenate_videoclips(
            [start_clip, video_clip],
            method="compose",
            padding=-transition_seconds if transition_seconds > 0 else 0,
        ).with_fps(config.frame_rate)

    end_clip = create_text_overlay_clip(
        text=config.end_text,
        frame_size=frame_size,
        duration_seconds=text_duration_seconds,
        transition_seconds=transition_seconds,
        font_path=config.text_font,
        font_size=config.text_font_size,
        text_color=config.text_color,
        bg_color=config.text_bg_color,
    )
    if end_clip is not None:
        video_clip = concatenate_videoclips(
            [video_clip, end_clip],
            method="compose",
            padding=0,
        ).with_fps(config.frame_rate)

    audio_resources: Sequence[object] = ()
    if config.audio_path:
        logger.info("Attaching audio track: %s", config.audio_path.name)
        video_clip, audio_resources = attach_audio(
            video_clip=video_clip,
            audio_path=config.audio_path,
            transition_ms=config.transition_ms,
        )

    output_path = config.output_video
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Writing video to %s", output_path)
    final_duration = 0.0
    try:
        video_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac" if config.audio_path else None,
            fps=config.frame_rate,
            preset="medium",
            logger=None,
        )
        final_duration = video_clip.duration or 0.0
    finally:
        video_clip.close()
        for resource in audio_resources:
            close_method = getattr(resource, "close", None)
            if callable(close_method):
                close_method()

    logger.info("Render complete. Total duration: %.2f seconds", final_duration)
    return output_path
