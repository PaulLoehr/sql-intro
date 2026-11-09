"""Tiny local web UI (stdlib only) to present and solve the exercises."""

import json
import shutil
import sqlite3
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path

from pydantic import BaseModel, ValidationError

from . import engine
from .data import build_all
from .models import Exercise, load_exercises


class RunRequest(BaseModel):
    db: str
    sql: str


class CheckRequest(BaseModel):
    id: str
    sql: str


class ResetRequest(BaseModel):
    db: str = ""


class App:
    """Holds the pristine databases, the working copies and the exercises."""

    def __init__(self, exercises_dir: Path, work_dir: Path) -> None:
        self.exercises = load_exercises(exercises_dir)
        self.pristine = build_all(work_dir / "pristine")
        self.working = {name: work_dir / f"{name}.db" for name in self.pristine}
        self.scratch = work_dir / "scratch"
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.reset()

    def reset(self, db: str = "") -> None:
        for name, source in self.pristine.items():
            if not db or db == name:
                shutil.copyfile(source, self.working[name])

    def exercise(self, exercise_id: str) -> Exercise | None:
        return next((e for e in self.exercises if e.id == exercise_id), None)

    def schema(self, db: str) -> list[dict]:
        # Trusted internal read (no authorizer): pragma_table_info is blocked for students.
        conn = sqlite3.connect(f"file:{self.working[db]}?mode=ro", uri=True)
        try:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall()
            out = []
            for (table,) in tables:
                cols = conn.execute(f'SELECT name, type FROM pragma_table_info("{table}")').fetchall()
                out.append({"table": table, "columns": [{"name": n, "type": t} for n, t in cols]})
            return out
        finally:
            conn.close()


def make_handler(app: App) -> type[BaseHTTPRequestHandler]:
    index_html = resources.files("sqlkurs").joinpath("static/index.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, payload: object, status: int = 200) -> None:
            if isinstance(payload, BaseModel):
                body = payload.model_dump_json().encode()
            else:
                body = json.dumps(payload).encode()
            self._send(status, body, "application/json; charset=utf-8")

        def _body(self) -> dict:
            # Only accept JSON posts from our own page (blocks cross-site form posts).
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                raise ValueError("expected application/json")
            length = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(length) or b"{}")

        def do_GET(self) -> None:
            if self.path == "/":
                self._send(200, index_html, "text/html; charset=utf-8")
            elif self.path == "/api/exercises":
                self._json(
                    [e.model_dump(mode="json", exclude={"solution"}) for e in app.exercises]
                )
            elif self.path.startswith("/api/schema/"):
                db = self.path.rsplit("/", 1)[1]
                if db in app.working:
                    self._json(app.schema(db))
                else:
                    self._json({"error": "unknown db"}, 404)
            elif self.path.startswith("/api/solution/"):
                exercise = app.exercise(self.path.rsplit("/", 1)[1])
                if exercise:
                    self._json({"solution": exercise.solution.strip()})
                else:
                    self._json({"error": "unknown exercise"}, 404)
            else:
                self._json({"error": "not found"}, 404)

        def do_POST(self) -> None:
            try:
                data = self._body()
                if self.path == "/api/run":
                    req = RunRequest(**data)
                    if req.db not in app.working:
                        return self._json({"error": "unknown db"}, 404)
                    conn = engine.connect(app.working[req.db])
                    try:
                        self._json(engine.run(conn, req.sql))
                    finally:
                        conn.close()
                elif self.path == "/api/check":
                    req = CheckRequest(**data)
                    exercise = app.exercise(req.id)
                    if exercise is None:
                        return self._json({"error": "unknown exercise"}, 404)
                    self._json(
                        engine.check(exercise, req.sql, app.pristine[exercise.db], app.scratch)
                    )
                elif self.path == "/api/reset":
                    app.reset(ResetRequest(**data).db)
                    self._json({"ok": True})
                else:
                    self._json({"error": "not found"}, 404)
            except (ValueError, ValidationError) as exc:
                self._json({"error": str(exc)}, 400)

        def log_message(self, format: str, *args: object) -> None:  # keep the console quiet
            pass

    return Handler


def serve(exercises_dir: Path, host: str = "127.0.0.1", port: int = 8000) -> None:
    with tempfile.TemporaryDirectory(prefix="sqlkurs-") as tmp:
        app = App(exercises_dir, Path(tmp))
        server = ThreadingHTTPServer((host, port), make_handler(app))
        print(f"sqlkurs läuft auf http://{host}:{port}  (Strg+C zum Beenden)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nBeendet.")
        finally:
            server.server_close()
