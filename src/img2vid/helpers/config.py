"""Configuration models and constants for image-to-video conversions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
DEFAULT_FRAME_RATE = 30
DEFAULT_TEXT_DURATION_MS = 2000


class ConversionError(Exception):
    """Raised when rendering fails due to invalid input or processing errors."""


@dataclass(slots=True)
class ConversionConfig:
    """User-configurable settings for a conversion run."""

    input_dir: Path
    output_video: Path
    audio_path: Optional[Path] = None
    frame_duration_ms: int = 3000
    transition_ms: int = 500
    frame_rate: int = DEFAULT_FRAME_RATE
    start_text: Optional[str] = None
    end_text: Optional[str] = None
    text_duration_ms: int = DEFAULT_TEXT_DURATION_MS
    text_font: Optional[str] = None
    text_font_size: int = 54
    text_color: str = "white"
    text_bg_color: str = "#000000"

    def validate(self) -> None:
        if not self.input_dir.is_dir():
            raise ConversionError(f"Input directory not found: {self.input_dir}")

        if self.audio_path is not None and not self.audio_path.is_file():
            raise ConversionError(f"Audio file not found: {self.audio_path}")

        if self.frame_duration_ms <= 0:
            raise ConversionError("Frame duration must be greater than 0 ms")

        if self.transition_ms < 0:
            raise ConversionError("Transition duration cannot be negative")

        if self.transition_ms > self.frame_duration_ms:
            raise ConversionError(
                "Transition duration cannot exceed frame duration"
            )

        if self.frame_rate <= 0:
            raise ConversionError("Frame rate must be a positive integer")

        has_title = bool(self.start_text and self.start_text.strip())
        has_credits = bool(self.end_text and self.end_text.strip())
        if (has_title or has_credits) and self.text_duration_ms <= 0:
            raise ConversionError("Text duration must be greater than 0 ms")

        if self.text_font_size <= 0:
            raise ConversionError("Text font size must be greater than 0")
