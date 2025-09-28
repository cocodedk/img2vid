# Title & Credits Overlay Plan

## Goal
Add optional opening title and closing credits text overlays to the rendered video while ensuring the soundtrack spans the entire runtime without interruption.

## Workstreams
- **Rendering pipeline**: extend helper modules to support structured overlay segments around the slideshow.
- **CLI/API surface**: introduce `--start-text`, `--end-text`, and optional styling knobs.
- **Validation & UX**: guard against overly long overlays and provide clear logging feedback.

## Implementation Steps
1. **Config enhancements**
   - Extend `ConversionConfig` with optional `start_text`, `end_text`, `text_duration_ms`, and typography options (font path, size, color, background).
   - Add validation to ensure text durations are positive and shorter than total runtime budget.
2. **Overlay generation**
   - Create helper to build MoviePy clips for text cards using `TextClip` (fallback to ImageClip if fonts missing) with fade in/out matching transition settings.
   - Prepend title clip and append credits clip to slideshow via `concatenate_videoclips`, adjusting padding so crossfades remain smooth.
3. **Audio continuity**
   - Update audio helper to stretch/loop soundtrack to full duration after overlays are inserted; keep fade in/out aligned with earliest/ latest visuals.
   - Provide graceful degradation when audio duration is shorter than total runtime even after overlays (loop as needed).
4. **Interface wiring**
   - Surface new options in CLI flags and Flask payload schema, keeping defaults disabled for backward compatibility.
   - Update README examples to demonstrate usage and mention font requirements.
5. **Testing & demo assets**
   - Add unit tests (where feasible) around overlay creation and config validation.
   - Prepare sample command in docs referencing `files/` assets for quick smoke checks.

## Open Questions
- Preferred default font and background styling?
- Should overlay durations reuse `frame_duration_ms` or have independent control?
- Need per-language localization considerations now or later?

## Risks & Mitigations
- **Font availability**: allow font path override and fall back to default system font.
- **Runtime**: extra clips increase render time; document expected overhead.
- **Alignment bugs**: ensure overlay durations counted in total video length before audio sync to avoid drift.
