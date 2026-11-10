from pathlib import Path

import pytest

from sqlkurs import engine
from sqlkurs.data import build_all
from sqlkurs.models import load_sheets

SHEETS = load_sheets(Path(__file__).parent.parent / "exercises")
CASES = [(sheet, exercise) for sheet in SHEETS for exercise in sheet.exercises]
IDS = [exercise.id for _, exercise in CASES]


@pytest.fixture(scope="module")
def dbs(tmp_path_factory):
    return build_all(tmp_path_factory.mktemp("dbs"))


def test_every_sheet_has_enough_exercises():
    assert len(SHEETS) == 2
    for sheet in SHEETS:
        assert len(sheet.exercises) >= 15, sheet.title


@pytest.mark.parametrize(("sheet", "exercise"), CASES, ids=IDS)
def test_solution_passes_own_check(sheet, exercise, dbs, tmp_path):
    result = engine.check(exercise, exercise.solution, dbs[sheet.db], tmp_path)
    assert result.ok, result.message


@pytest.mark.parametrize(("sheet", "exercise"), CASES, ids=IDS)
def test_solution_returns_rows(sheet, exercise, dbs):
    conn = engine.connect(dbs[sheet.db])
    try:
        assert engine.run(conn, exercise.solution).rows
    finally:
        conn.close()


def test_wrong_answer_fails(dbs, tmp_path):
    sheet, exercise = CASES[0]
    result = engine.check(exercise, "SELECT 1;", dbs[sheet.db], tmp_path)
    assert not result.ok


def test_sql_error_is_reported(dbs, tmp_path):
    sheet, exercise = CASES[0]
    result = engine.check(exercise, "SELEKT 1", dbs[sheet.db], tmp_path)
    assert not result.ok and result.message


def test_attach_is_blocked(dbs, tmp_path):
    conn = engine.connect(dbs["flat"])
    result = engine.run(conn, f"ATTACH DATABASE '{tmp_path}/evil.db' AS evil;")
    conn.close()
    assert result.error
    assert not (tmp_path / "evil.db").exists()


def test_build_is_deterministic(tmp_path):
    a = build_all(tmp_path / "a")["kvv"].read_bytes()
    b = build_all(tmp_path / "b")["kvv"].read_bytes()
    assert a == b
