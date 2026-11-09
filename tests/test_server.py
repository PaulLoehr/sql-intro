from pathlib import Path

from sqlkurs.server import App


def test_schema_lists_tables(tmp_path):
    app = App(Path(__file__).parent.parent / "exercises", tmp_path)
    tables = {t["table"] for t in app.schema("kvv")}
    assert {"lines", "stops", "line_stops", "trips", "stop_events"} <= tables
    assert {c["name"] for t in app.schema("flat") for c in t["columns"]} >= {"delay_min", "boarded"}
