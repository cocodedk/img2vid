"""Text overlay generation helpers for title and credit cards."""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.fx import FadeIn, FadeOut


def _fallback_text_clip(
    text: str,
    frame_size: Tuple[int, int],
    duration: float,
    font_path: Optional[str],
    font_size: int,
    text_color: str,
    bg_color: str,
):
    """Generate a text clip using PIL when MoviePy's TextClip is unavailable."""

    width, height = frame_size
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    text_lines = text.splitlines() or [text]
    line_metrics = []
    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        line_metrics.append((line, line_width, line_height))

    max_line_height = max((m[2] for m in line_metrics), default=font_size)
    total_text_height = sum((m[2] for m in line_metrics)) + max(0, len(line_metrics) - 1) * 8

    current_y = (height - total_text_height) / 2
    for line, line_width, line_height in line_metrics:
        position = ((width - line_width) / 2, current_y)
        draw.text(position, line, font=font, fill=text_color, align="center")
        current_y += line_height + 8

    return ImageClip(np.array(image)).with_duration(duration)


def create_text_overlay_clip(
    *,
    text: Optional[str],
    frame_size: Tuple[int, int],
    duration_seconds: float,
    transition_seconds: float,
    font_path: Optional[str],
    font_size: int,
    text_color: str,
    bg_color: str,
):
    """Create a MoviePy clip containing the provided text with fades."""

    if not text or not text.strip():
        return None

    safe_duration = max(duration_seconds, 0.1)

    try:
        clip = TextClip(
            text=text,
            font=font_path,
            font_size=font_size,
            color=text_color,
            bg_color=bg_color,
            size=frame_size,
            method="caption",
            text_align="center",
            horizontal_align="center",
            vertical_align="center",
            duration=safe_duration,
        )
    except Exception:
        clip = _fallback_text_clip(
            text=text,
            frame_size=frame_size,
            duration=safe_duration,
            font_path=font_path,
            font_size=font_size,
            text_color=text_color,
            bg_color=bg_color,
        )

    fade_duration = min(max(transition_seconds, 0.0), safe_duration / 2)
    if fade_duration > 0:
        clip = clip.with_effects([FadeIn(fade_duration), FadeOut(fade_duration)])

    return clip
