# CLAUDE.md — img2vid

## Project Overview

img2vid is a Python CLI and Flask tool for converting ordered image folders into MP4 slideshow videos with crossfade effects and optional audio soundtrack support.

- **Language / Runtime**: Python 3.12
- **Framework**: Flask 3.0 (web), Click (CLI via pyproject.toml entry point)
- **Architecture**: Layered — CLI → converter core → helpers
- **Package / Namespace**: `img2vid`
- **Package manager**: uv

---

## Required Skills — ALWAYS Invoke These

| Situation | Skill |
|-----------|-------|
| Before any new feature or screen | `superpowers:brainstorming` |
| Planning multi-step changes | `superpowers:writing-plans` |
| Writing or fixing core logic | `superpowers:test-driven-development` |
| First sign of a bug or failure | `superpowers:systematic-debugging` |
| Before completing a feature branch | `superpowers:requesting-code-review` |
| Before claiming any task done | `superpowers:verification-before-completion` |
| Working on UI / frontend | `frontend-design:frontend-design` |
| After implementing — reviewing quality | `simplify` |

---

## Architecture

```
img-2-vid/
├── src/img2vid/       ← Core package
│   ├── cli.py         ← CLI entry point (Click)
│   ├── converter.py   ← Video conversion logic
│   ├── flask_app.py   ← Flask web interface
│   └── helpers/       ← Shared utilities
├── pyproject.toml     ← Project config + dependencies
├── version.txt        ← Semantic version
└── scripts/           ← Dev tooling
```

### Layer Rules
- `helpers/` must not import from `cli.py` or `flask_app.py`
- `converter.py` must not import from `cli.py` or `flask_app.py`

---

## Coding Conventions

- [ ] All functions typed with Python type hints
- [ ] Functions pure where possible
- [ ] No hardcoded strings — use constants or config
- [ ] `ruff` enforced on every commit

---

## Engineering Principles

### File Size
- **200-line maximum per file**

### DRY · SOLID · KISS · YAGNI
- Extract shared logic into named utilities
- Single Responsibility: one class/function does one thing
- Don't add features not yet needed

### TDD
- Write the failing test first, make it pass, then refactor

### Commit hygiene
- Follow Conventional Commits: `feat:` / `fix:` / `chore:`

---

## Build Commands

```bash
uv sync                                  # Install dependencies
uv run ruff check .                      # Lint
uv run pytest --tb=short                 # Run tests
uv run ruff check . && uv run pytest     # Smoke check
uv run img2vid --help                    # CLI
```

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file |
| `version.txt` | Semantic version (MAJOR.MINOR.PATCH) |
| `.github/workflows/` | CI, release, Pages automation |
| `.githooks/` | Pre-commit and commit-msg hooks |
| `scripts/install-hooks.sh` | One-time hook installer |

---

## Starting a New Session

1. Read this file
2. Run `uv run ruff check . && uv run pytest --tb=short`
3. Invoke `superpowers:brainstorming` before touching any feature
