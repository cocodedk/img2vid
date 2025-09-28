# img2vid

Command-line and Flask tooling for converting ordered image folders into MP4 slideshows with soundtrack support.

**Created by [Babak Bandpey](https://cocode.dk) - [cocode.dk](https://cocode.dk)**

## Prerequisites
- [uv](https://github.com/astral-sh/uv) 0.2.0 or newer
- Python 3.12 (managed via `uv`)

## Environment Setup
```bash
# Install Python 3.12 via uv (only required once per machine)
uv python install 3.12

# Create and activate a virtual environment managed by uv
uv venv
source .venv/bin/activate

# Install project dependencies
uv pip install -e .
```

## CLI Usage
```bash
img2vid \
  --input-dir ./assets/images \
  --audio ./assets/soundtrack.mp3 \
  --frame-duration-ms 3000 \
  --transition-ms 500 \
  --start-text "Project Unity" \
  --end-text "Thanks for watching" \
  --output-name project-unity \
  --text-duration-ms 2000
```

### CLI Real Example

```bash
UV_CACHE_DIR=.uv-cache img2vid \
--input-dir ./files/20250928-unity-foundation \
--audio "./files/20250928-unity-foundation/Gibran Alcocer - Idea 9 (Slowed + Reverb).mp3" \
--frame-duration-ms 3000 \
--transition-ms 500 \
--start-text "Unity Foundation - September 2025" \
--end-text "Thank you for all your donations and generocities" \
--text-duration-ms 5000 \
--log-level INFO
```

Logs will display processing progress plus the final runtime. The command exits with a non-zero status when validation fails.

### Overlay Options
- `--start-text` and `--end-text` add title/credits cards that fade in/out using the configured transition duration.
- Customize typographic styling with `--text-font`, `--text-font-size`, `--text-color`, and `--text-bg-color`.
- Use `--text-duration-ms` to control how long each overlay remains on screen (defaults to 2000 ms).

### Output Versioning
- By default, videos are written to `build/<input-folder>/v###/<basename>.mp4`. The first unused version number is selected automatically.
- Override the root directory with `--output-dir` (default `build`) or provide a fully qualified path with `--output-video`.
- Control the filename (without extension) via `--output-name`; when omitted the input folder name is used.

## Flask Service
```bash
# Within the activated uv environment
python -m flask --app img2vid.flask_app:create_app run --debug
```

Send a POST request to `http://localhost:5000/render` with JSON parameters matching the CLI flags to trigger a conversion.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Creator

**Babak Bandpey**
Website: [cocode.dk](https://cocode.dk)
Email: [Contact via cocode.dk](https://cocode.dk)

This project is part of the cocode.dk development portfolio, showcasing practical Python tools for multimedia processing.
