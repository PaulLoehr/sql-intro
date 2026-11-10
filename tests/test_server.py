from pathlib import Path

from sqlkurs.server import App

EXERCISES = Path(__file__).parent.parent / "exercises"


def test_schema_lists_tables_and_keys(tmp_path):
    app = App(EXERCISES, tmp_path)
    kvv = {t["table"]: t for t in app.schema("kvv")}
    assert {"lines", "stops", "line_stops", "trips", "stop_events"} <= set(kvv)
    assert any(c["pk"] for c in kvv["stops"]["columns"])
    assert {c["name"] for t in app.schema("flat") for c in t["columns"]} >= {"delay_min", "boarded"}


def test_app_can_serve_a_single_sheet(tmp_path):
    app = App(EXERCISES, tmp_path, sheet=1)
    assert [s.number for s in app.sheets] == [1]
    assert app.find("0.1") is None and app.find("1.1") is not None


def test_unknown_sheet_is_rejected(tmp_path):
    import pytest

    with pytest.raises(ValueError):
        App(EXERCISES, tmp_path, sheet=9)


def test_find_returns_sheet_and_exercise(tmp_path):
    app = App(EXERCISES, tmp_path)
    sheet, exercise = app.find("0.1")
    assert sheet.number == 0 and exercise.id == "0.1"
    assert app.find("nope") is None
