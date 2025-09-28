"""Minimal Flask application exposing the conversion service."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request

from .converter import (
    DEFAULT_TEXT_DURATION_MS,
    ConversionConfig,
    ConversionError,
    render_video,
)

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.post("/render")
    def render_endpoint():
        payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
        try:
            config = ConversionConfig(
                input_dir=Path(payload["input_dir"]),
                output_video=Path(payload["output_video"]),
                audio_path=Path(payload["audio"]) if payload.get("audio") else None,
                frame_duration_ms=int(payload.get("frame_duration_ms", 3000)),
                transition_ms=int(payload.get("transition_ms", 500)),
                frame_rate=int(payload.get("frame_rate", 30)),
                start_text=payload.get("start_text"),
                end_text=payload.get("end_text"),
                text_duration_ms=int(
                    payload.get("text_duration_ms", DEFAULT_TEXT_DURATION_MS)
                ),
                text_font=payload.get("text_font"),
                text_font_size=int(payload.get("text_font_size", 54)),
                text_color=payload.get("text_color", "white"),
                text_bg_color=payload.get("text_bg_color", "#000000"),
            )
            output_path = render_video(config)
        except KeyError as exc:
            missing_key = str(exc).strip("'")
            logger.warning("Missing required field in request: %s", missing_key)
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Missing required field: {missing_key}",
                    }
                ),
                400,
            )
        except ConversionError as exc:
            logger.warning("Conversion error: %s", exc)
            return (
                jsonify({"status": "error", "message": str(exc)}),
                400,
            )
        except Exception as exc:  # pragma: no cover - safety net
            logger.exception("Unexpected failure during rendering")
            return (
                jsonify({"status": "error", "message": str(exc)}),
                500,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "output_video": str(output_path),
                }
            ),
            200,
        )

    return app


if __name__ == "__main__":  # pragma: no cover - manual launch helper
    logging.basicConfig(level=logging.INFO)
    application = create_app()
    application.run(host="0.0.0.0", port=5000)
