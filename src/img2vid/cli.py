"""Command-line interface for the image-to-video renderer."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable, Optional

from .converter import (
    DEFAULT_FRAME_RATE,
    DEFAULT_TEXT_DURATION_MS,
    ConversionConfig,
    ConversionError,
    render_video,
    resolve_output_path,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="img2vid",
        description=(
            "Convert an ordered folder of images into an MP4 slideshow with optional audio"
        ),
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing the source images",
    )
    parser.add_argument(
        "--output-video",
        type=Path,
        help="Explicit target path for the generated video",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="Root folder where versioned outputs are stored (default: build)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        help="Base filename (without extension) for the generated video",
    )
    parser.add_argument(
        "--audio",
        type=Path,
        help="Optional soundtrack to merge with the slideshow",
    )
    parser.add_argument(
        "--frame-duration-ms",
        type=int,
        default=3000,
        help="Duration each image remains on screen (milliseconds)",
    )
    parser.add_argument(
        "--transition-ms",
        type=int,
        default=500,
        help="Cross-fade duration between images (milliseconds)",
    )
    parser.add_argument(
        "--frame-rate",
        type=int,
        default=DEFAULT_FRAME_RATE,
        help="Frames per second for the final video (default: %(default)s)",
    )
    parser.add_argument(
        "--start-text",
        type=str,
        help="Optional opening title text overlay",
    )
    parser.add_argument(
        "--end-text",
        type=str,
        help="Optional closing credits text overlay",
    )
    parser.add_argument(
        "--text-duration-ms",
        type=int,
        default=DEFAULT_TEXT_DURATION_MS,
        help="Duration for title/credits overlays (milliseconds)",
    )
    parser.add_argument(
        "--text-font",
        type=str,
        help="Path to a TTF/OTF font for overlay text",
    )
    parser.add_argument(
        "--text-font-size",
        type=int,
        default=54,
        help="Font size for overlay text",
    )
    parser.add_argument(
        "--text-color",
        type=str,
        default="white",
        help="Text color (name or hex) for overlays",
    )
    parser.add_argument(
        "--text-bg-color",
        type=str,
        default="#000000",
        help="Background color (name or hex) for overlays",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity",
    )
    return parser


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(levelname)s %(message)s",
    )


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    _configure_logging(args.log_level)
    logging.info("Starting conversion run")

    output_video = resolve_output_path(
        input_dir=args.input_dir,
        explicit_output=args.output_video,
        output_root=args.output_dir,
        output_basename=args.output_name,
    )

    config = ConversionConfig(
        input_dir=args.input_dir,
        output_video=output_video,
        audio_path=args.audio,
        frame_duration_ms=args.frame_duration_ms,
        transition_ms=args.transition_ms,
        frame_rate=args.frame_rate,
        start_text=args.start_text,
        end_text=args.end_text,
        text_duration_ms=args.text_duration_ms,
        text_font=args.text_font,
        text_font_size=args.text_font_size,
        text_color=args.text_color,
        text_bg_color=args.text_bg_color,
    )

    try:
        output_path = render_video(config)
    except ConversionError as exc:
        logging.error("Conversion failed: %s", exc)
        return 1
    except Exception:
        logging.exception("Unexpected error while rendering video")
        return 1

    logging.info("Saved video to %s", output_path)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
