# Contributing to img2vid

## Local Setup

1. Install [uv](https://github.com/astral-sh/uv) 0.2.0+.
2. Clone the repository:
   ```bash
   git clone https://github.com/cocodedk/img2vid.git
   cd img2vid
   uv sync
   ```

## Install Git Hooks

```bash
./scripts/install-hooks.sh
```

## Local Git Setup

```bash
git config pull.rebase true
git config core.autocrlf input
git config push.autoSetupRemote true
git config init.defaultBranch main
```

## Build and Test Commands

```bash
uv run ruff check .          # Lint
uv run pytest --tb=short     # Run tests
uv run img2vid --help        # CLI entry point
```

## Coding Style

- Follow PEP 8 via `ruff`.
- Keep files under 200 lines.
- Use type hints everywhere.

## Branch Naming

| Prefix | Use |
|---|---|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance |
| `docs/` | Documentation |
| `refactor/` | Code restructuring |
| `ci/` | CI/CD changes |

## PR Checklist

- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest` passes.
- [ ] Manual test completed.
- [ ] Updated docs if behavior changed.
