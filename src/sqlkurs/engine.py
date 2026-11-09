"""Run student SQL safely against a working copy and check results."""

import shutil
import sqlite3
from collections import Counter
from pathlib import Path

from .models import CheckResult, Exercise, QueryResult

MAX_ROWS = 200
_DENIED = {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH}


def _authorizer(action: int, arg1, arg2, db_name, source):
    """Block ATTACH/DETACH and PRAGMAs so queries cannot touch other files."""
    if action in _DENIED or action == sqlite3.SQLITE_PRAGMA:
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")  # before the authorizer blocks PRAGMA
    conn.set_authorizer(_authorizer)
    return conn


def run(conn: sqlite3.Connection, sql: str, limit: int = MAX_ROWS) -> QueryResult:
    """Run a script; return the rows of the last statement that produces rows."""
    try:
        statements = _split(sql)
        result = QueryResult()
        for statement in statements:
            cur = conn.execute(statement)
            if cur.description:
                result = QueryResult(columns=[d[0] for d in cur.description])
                fetched = cur.fetchmany(limit + 1)
                result.truncated = len(fetched) > limit
                result.rows = [list(r) for r in fetched[:limit]]
            else:
                result = QueryResult(rowcount=cur.rowcount)
        conn.commit()
        return result
    except (sqlite3.Error, ValueError) as exc:
        conn.rollback()
        return QueryResult(error=str(exc))


def _split(sql: str) -> list[str]:
    """Split a script into complete statements (sqlite3.complete_statement aware)."""
    statements: list[str] = []
    buffer = ""
    for line in sql.splitlines(keepends=True):
        buffer += line
        if sqlite3.complete_statement(buffer):
            statements.append(buffer.strip())
            buffer = ""
    if buffer.strip() and not _only_comments(buffer):
        statements.append(buffer.strip())
    return statements


def _only_comments(text: str) -> bool:
    return all(not line.strip() or line.strip().startswith("--") for line in text.splitlines())


def _compare(expected: QueryResult, actual: QueryResult, ordered: bool) -> str:
    """Return an empty string when equal, otherwise a student-friendly message."""
    if len(actual.columns) != len(expected.columns):
        return (
            f"Erwartet {len(expected.columns)} Spalte(n), "
            f"deine Abfrage liefert {len(actual.columns)}."
        )
    exp = [tuple(r) for r in expected.rows]
    act = [tuple(r) for r in actual.rows]
    if len(exp) != len(act):
        return f"Erwartet {len(exp)} Zeile(n), du hast {len(act)}."
    if ordered:
        if exp != act:
            return "Die Zeilen stimmen nicht oder stehen in falscher Reihenfolge."
    elif Counter(exp) != Counter(act):
        return "Anzahl passt, aber der Inhalt der Zeilen weicht ab."
    return ""


def fresh_copy(source: Path, target: Path) -> Path:
    shutil.copyfile(source, target)
    return target


def check(exercise: Exercise, sql: str, db_path: Path, scratch: Path) -> CheckResult:
    """Run `sql` on a fresh copy of the exercise database and compare with the solution."""
    expected_db = fresh_copy(db_path, scratch / "expected.db")
    actual_db = fresh_copy(db_path, scratch / "actual.db")
    expected_conn, actual_conn = connect(expected_db), connect(actual_db)
    try:
        expected = run(expected_conn, exercise.solution, limit=10_000)
        actual = run(actual_conn, sql, limit=10_000)
        if actual.error:
            return CheckResult(ok=False, message=actual.error, result=actual)
        problem = _compare(expected, actual, exercise.ordered)
        if problem:
            return CheckResult(ok=False, message=problem, result=actual)
        return CheckResult(ok=True, message="Richtig!", result=actual)
    finally:
        expected_conn.close()
        actual_conn.close()
