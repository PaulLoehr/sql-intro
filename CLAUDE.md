# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Overview

Teaching repo for an introductory SQL / databases session at HKA (VSM), modeled on the structure of [CS50 SQL](https://cs50.harvard.edu/sql/) lectures 0 and 1 (Querying, Relating). It generates two synthetic SQLite databases about public transport, defines exercises with reference solutions (TOML, validated by Pydantic), and serves a small stdlib-only web UI where exercises can be solved and checked live. Checking compares query results, not SQL text. Course text is German; code is English.

## Development Commands

### Setup

```bash
uv sync --group test
```

### Run

```bash
uv run sqlkurs build         # (re)create data/flat.db and data/kvv.db
uv run sqlkurs list          # list exercises
uv run sqlkurs serve         # web UI on http://127.0.0.1:8000 (--port N)
uv run sqlkurs shell kvv     # sqlite3 console (kvv or flat)
```

Run all commands from the repo root (paths `exercises/` and `data/` are relative to the working directory).

### Testing

```bash
uv run pytest --cov
uv run pytest tests/test_engine.py -k 1.3
```

Every exercise solution is tested against its own check; add a solution to the TOML file and the tests pick it up.

### Structure

- `src/sqlkurs/data.py`: seeded data generation, schemas (`flat`: table `delays`; `kvv`: normalized).
- `src/sqlkurs/engine.py`: sandboxed execution (ATTACH/PRAGMA denied) and result comparison.
- `src/sqlkurs/server.py`, `static/index.html`: web UI and JSON API.
- `exercises/*.toml`: exercises (`id`, `lesson`, `db`, `task`, `hint`, `solution`, `ordered`).
- `lessons/*.md`: lesson plans with demo queries (German).
