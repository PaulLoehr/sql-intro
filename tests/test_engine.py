from pathlib import Path

import pytest

from sqlkurs import engine
from sqlkurs.data import build_all
from sqlkurs.models import load_exercises

EXERCISES = load_exercises(Path(__file__).parent.parent / "exercises")


@pytest.fixture(scope="module")
def dbs(tmp_path_factory):
    return build_all(tmp_path_factory.mktemp("dbs"))


def test_exercise_ids_unique():
    ids = [e.id for e in EXERCISES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("exercise", EXERCISES, ids=lambda e: e.id)
def test_solution_passes_own_check(exercise, dbs, tmp_path):
    result = engine.check(exercise, exercise.solution, dbs[exercise.db], tmp_path)
    assert result.ok, result.message


@pytest.mark.parametrize("exercise", EXERCISES, ids=lambda e: e.id)
def test_solution_returns_rows(exercise, dbs, tmp_path):
    conn = engine.connect(dbs[exercise.db])
    assert engine.run(conn, exercise.solution).rows


def test_wrong_answer_fails(dbs, tmp_path):
    exercise = next(e for e in EXERCISES if e.id == "0.5")
    assert not engine.check(exercise, "SELECT COUNT(*) FROM delays;", dbs["flat"], tmp_path).ok


def test_sql_error_is_reported(dbs, tmp_path):
    exercise = EXERCISES[0]
    result = engine.check(exercise, "SELEKT 1", dbs["flat"], tmp_path)
    assert not result.ok and result.message


def test_attach_is_blocked(dbs, tmp_path):
    conn = engine.connect(dbs["flat"])
    result = engine.run(conn, f"ATTACH DATABASE '{tmp_path}/evil.db' AS evil;")
    assert result.error
    assert not (tmp_path / "evil.db").exists()


def test_build_is_deterministic(tmp_path):
    a = build_all(tmp_path / "a")["kvv"].read_bytes()
    b = build_all(tmp_path / "b")["kvv"].read_bytes()
    assert a == b
