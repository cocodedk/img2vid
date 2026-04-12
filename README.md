# img2vid

Command-line and Flask tooling for converting ordered image folders into MP4 slideshows with soundtrack support.

## Website

- [English](https://cocodedk.github.io/img2vid/)
- [فارسی (Persian)](https://cocodedk.github.io/img2vid/fa/)

## Download

[**Download img2vid**](https://github.com/cocodedk/img2vid/releases/latest/download/img2vid.zip)

## Prerequisites

- [uv](https://github.com/astral-sh/uv) 0.2.0 or newer
- Python 3.12 (managed via `uv`)

## Environment Setup

```bash
uv python install 3.12
uv venv
source .venv/bin/activate
uv sync
```

## CLI Usage

```bash
uv run img2vid \
  --input-dir ./assets/images \
  --audio ./assets/soundtrack.mp3 \
  --frame-duration-ms 3000 \
  --transition-ms 500 \
  --start-text "Project Unity" \
  --end-text "Thanks for watching" \
  --output-name project-unity \
  --text-duration-ms 2000
```

## Flask Service

```bash
uv run python -m flask --app img2vid.flask_app:create_app run --debug
```

Send a POST request to `http://localhost:5000/render` with JSON parameters matching the CLI flags.

## Architecture

```
src/img2vid/
├── cli.py          ← CLI entry point
├── converter.py    ← Video conversion logic
├── flask_app.py    ← Flask web service
└── helpers/        ← Shared utilities
```

| Component | Technology |
|-----------|-----------|
| Video conversion | moviepy 2.1 |
| CLI | Click |
| Web UI | Flask 3.0 |
| Language | Python 3.12 |

## Author

**Babak Bandpey** — [cocode.dk](https://cocode.dk) | [LinkedIn](https://linkedin.com/in/babakbandpey) | [GitHub](https://github.com/cocodedk)

## License

Apache-2.0 | © 2026 [Cocode](https://cocode.dk) | Created by [Babak Bandpey](https://linkedin.com/in/babakbandpey)
