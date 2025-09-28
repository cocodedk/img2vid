"""Audio utilities for merging soundtracks onto video clips."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from moviepy.audio.fx import AudioFadeIn, AudioFadeOut, AudioLoop
from moviepy.audio.io.AudioFileClip import AudioFileClip

from .config import ConversionError


def attach_audio(
    video_clip,
    audio_path: Path,
    transition_ms: int,
) -> Tuple[object, Tuple[object, ...]]:
    """Attach audio to ``video_clip`` and return the clip plus resources to close."""

    transition_duration = transition_ms / 1000.0
    audio_clip = AudioFileClip(str(audio_path))
    audio_duration = audio_clip.duration or 0.0
    video_duration = video_clip.duration or 0.0
    if audio_duration <= 0.0:
        audio_clip.close()
        raise ConversionError("Audio file duration must be greater than zero")

    min_required_audio = max(transition_duration * 2, 0.1)
    if audio_duration < min_required_audio:
        audio_clip.close()
        raise ConversionError(
            "Audio file is too short to accommodate fade in/out transitions"
        )

    if audio_duration < video_duration:
        working_audio = audio_clip.with_effects([AudioLoop(duration=video_duration)])
    else:
        working_audio = audio_clip.subclipped(0, video_duration)

    fade_duration = transition_duration if transition_duration > 0 else min(
        0.5, video_duration / 10
    )
    fade_duration = min(fade_duration, max(video_duration / 4, 0.0))
    if fade_duration > 0:
        working_audio = working_audio.with_effects(
            [AudioFadeIn(fade_duration), AudioFadeOut(fade_duration)]
        )

    video_clip = video_clip.with_audio(working_audio)

    closeables: Tuple[object, ...]
    if working_audio is audio_clip or not hasattr(working_audio, "close"):
        closeables = (audio_clip,)
    else:
        closeables = (audio_clip, working_audio)

    return video_clip, closeables
