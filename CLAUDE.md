# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Overview

Teaching repo for an introductory SQL course at HKA (VSM): two 90-minute exercise sheets (sheet 0: querying one table, sheet 1: relating tables), loosely modeled on CS50 SQL lectures 0 and 1. It generates two synthetic SQLite databases about public transport (`flat`, `kvv`), defines exercises with reference solutions (TOML, validated by Pydantic), and serves a stdlib-only web UI where students solve and check them. Checking compares query results, not SQL text. Students run it on macOS and Windows, so setup must stay simple (uv, with venv + pip as fallback; Python >= 3.11; no `sqlite3` CLI needed). Course text is German; code is English. The UI follows the dm colour guidelines (Indigo `#49439B`, Mint `#55C1AF`, text `#3E3E48`, traffic-light colours only for status, font DM Office with Arial fallback, no decorative lines or stripes).

## Development Commands

### Setup

```bash
uv sync --group test
```

### Run

```bash
uv run sqlkurs                 # build data/ if missing, start web UI, open browser
uv run sqlkurs --port 8001 --no-browser
uv run sqlkurs build           # (re)create data/flat.db and data/kvv.db
uv run sqlkurs list            # list sheets and exercises
```

Alternative without uv: `python -m venv .venv`, activate, `pip install -e .`, `sqlkurs`.

### Testing

```bash
uv run pytest --cov
uv run pytest tests/test_engine.py -k 1.3
```

Every exercise solution is tested against its own check; add a solution to a TOML file and the tests pick it up.

## Structure

- `exercises/uebung-N.toml`: one sheet per file (`number`, `title`, `db`, `goal`, then `[[exercise]]` with `id`, `section`, `title`, `task`, `hint`, `solution`, `ordered`, `bonus`). Models in `src/sqlkurs/models.py`.
- `ablauf/uebung-N.md`: German session plans for the lecturer (minute plan, demo queries).
- `src/sqlkurs/data.py`: seeded data generation, schemas (`flat`: table `delays`; `kvv`: normalized).
- `src/sqlkurs/engine.py`: sandboxed execution (ATTACH/PRAGMA denied) and result comparison.
- `src/sqlkurs/server.py`, `static/index.html`: JSON API (`/api/sheets`, `/api/schema/<db>`, `/api/run`, `/api/check`, `/api/solution/<id>`, `/api/reset`) and the single-file UI.
- `data/`: generated databases (gitignored), opened by students in VS Code with the SQLite Viewer extension.
