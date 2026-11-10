"""CLI entry point: start the web UI (default), build the databases, list exercises."""

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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sqlkurs", description="Interaktive SQL-Einführung")
    sub = parser.add_subparsers(dest="command")
    serve_p = sub.add_parser("serve", help="Browser-Oberfläche starten (Standard)")
    sub.add_parser("build", help="Datenbanken in data/ neu erzeugen")
    sub.add_parser("list", help="Aufgaben auflisten")
    for p in (parser, serve_p):
        p.add_argument("--port", type=int, default=8000, help="Port der Oberfläche (8000)")
        p.add_argument("--no-browser", action="store_true", help="Browser nicht automatisch öffnen")
    args = parser.parse_args(argv)

    if args.command == "build":
        for name, path in build_all(DB_DIR).items():
            print(f"{name}: {path}")
    elif args.command == "list":
        for sheet in load_sheets(EXERCISES_DIR):
            print(f"Übung {sheet.number}: {sheet.title} [{sheet.db}]")
            for e in sheet.exercises:
                print(f"  {e.id:5} {e.section}: {e.title}{' (Zusatz)' if e.bonus else ''}")
    else:  # default: serve
        from .server import serve

        if not all((DB_DIR / f"{name}.db").exists() for name in DATABASES):
            build_all(DB_DIR)  # so data/*.db can be opened in VS Code right away
        serve(EXERCISES_DIR, port=args.port, open_browser=not args.no_browser)
    return 0


if __name__ == "__main__":
    sys.exit(main())
