"""CLI entry points: `uebung0` / `uebung1` start one sheet in the browser; `sqlkurs` builds and lists."""

import argparse
import sys
from pathlib import Path

from .data import DATABASES, build_all
from .models import load_sheets


def _project_root() -> Path:
    """Repo root: found relative to the package (editable install), else the working directory."""
    candidate = Path(__file__).resolve().parents[2]
    return candidate if (candidate / "exercises").is_dir() else Path.cwd()


ROOT = _project_root()
EXERCISES_DIR = ROOT / "exercises"
DB_DIR = ROOT / "data"


def _serve_sheet(number: int, argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(prog=f"uebung{number}", description=f"Übung {number} im Browser starten")
    parser.add_argument("--port", type=int, default=8000, help="Port der Oberfläche (8000)")
    parser.add_argument("--no-browser", action="store_true", help="Browser nicht automatisch öffnen")
    args = parser.parse_args(argv)

    from .server import serve

    if not all((DB_DIR / f"{name}.db").exists() for name in DATABASES):
        build_all(DB_DIR)  # so data/*.db can be opened in VS Code right away
    serve(EXERCISES_DIR, sheet=number, port=args.port, open_browser=not args.no_browser)
    return 0


def uebung0(argv: list[str] | None = None) -> int:
    return _serve_sheet(0, argv)


def uebung1(argv: list[str] | None = None) -> int:
    return _serve_sheet(1, argv)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sqlkurs",
        description="Interaktive SQL-Einführung. Übungen starten mit `uebung0` bzw. `uebung1`.",
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build", help="Datenbanken in data/ neu erzeugen")
    sub.add_parser("list", help="Aufgaben auflisten")
    args = parser.parse_args(argv)

    if args.command == "build":
        for name, path in build_all(DB_DIR).items():
            print(f"{name}: {path}")
    elif args.command == "list":
        for sheet in load_sheets(EXERCISES_DIR):
            print(f"Übung {sheet.number}: {sheet.title} [{sheet.db}]  ->  uebung{sheet.number}")
            for e in sheet.exercises:
                print(f"  {e.id:5} {e.section}: {e.title}")
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
