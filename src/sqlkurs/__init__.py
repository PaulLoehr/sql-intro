"""CLI entry point: build databases, start the web UI, open the sqlite3 shell."""

import argparse
import subprocess
import sys
from pathlib import Path

from .data import DATABASES, build_all
from .models import load_exercises

ROOT = Path.cwd()
EXERCISES_DIR = ROOT / "exercises"
DB_DIR = ROOT / "data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sqlkurs", description="Interaktive SQL-Einführung")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="Datenbanken in data/ neu erzeugen")
    sub.add_parser("list", help="Aufgaben auflisten")
    serve_p = sub.add_parser("serve", help="Browser-Oberfläche starten")
    serve_p.add_argument("--port", type=int, default=8000)
    shell_p = sub.add_parser("shell", help="sqlite3-Konsole auf einer Datenbank öffnen")
    shell_p.add_argument("db", choices=sorted(DATABASES))
    args = parser.parse_args(argv)

    if args.command == "build":
        for name, path in build_all(DB_DIR).items():
            print(f"{name}: {path}")
    elif args.command == "list":
        for e in load_exercises(EXERCISES_DIR):
            print(f"{e.id:5} [{e.db}] {e.title}")
    elif args.command == "serve":
        from .server import serve

        serve(EXERCISES_DIR, port=args.port)
    elif args.command == "shell":
        build_all(DB_DIR)
        return subprocess.call(["sqlite3", "-header", "-column", str(DB_DIR / f"{args.db}.db")])
    return 0


if __name__ == "__main__":
    sys.exit(main())
