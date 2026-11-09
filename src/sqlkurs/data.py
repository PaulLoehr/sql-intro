"""Build the synthetic transit databases used in the course.

All data is invented (loosely inspired by a mid-sized German city) and generated
with a fixed seed, so every build is identical.
"""

import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42

STOPS: list[tuple[str, int, int]] = [
    # name, zone, wheelchair accessible
    ("Hauptbahnhof", 1, 1),
    ("Marktplatz", 1, 1),
    ("Europaplatz", 1, 1),
    ("Kronenplatz", 1, 1),
    ("Durlacher Tor", 1, 1),
    ("Ettlinger Tor", 1, 1),
    ("Mühlburger Tor", 1, 0),
    ("Kaiserplatz", 1, 0),
    ("Entenfang", 2, 1),
    ("Tivoli", 2, 0),
    ("Gottesauer Platz", 2, 1),
    ("Rüppurr Kirche", 2, 0),
    ("Knielingen Nord", 3, 0),
    ("Waldstadt", 3, 1),
    ("Hagsfeld Bahnhof", 3, 1),
    ("Durlach Turmberg", 3, 0),
    ("Grötzingen", 4, 0),
    ("Neureut Kirchfeld", 4, 1),
    ("Ettlingen Stadt", 4, 1),
    ("Pfinztal Berghausen", 4, 0),
    ("Messe Süd", 3, 1),  # planned stop: no line serves it yet
]

# name, mode, operator, ordered stops
LINES: list[tuple[str, str, str, list[str]]] = [
    ("S1", "sbahn", "Regio", ["Ettlingen Stadt", "Hauptbahnhof", "Durlacher Tor", "Hagsfeld Bahnhof", "Pfinztal Berghausen"]),
    ("S2", "sbahn", "Regio", ["Grötzingen", "Durlach Turmberg", "Hauptbahnhof", "Mühlburger Tor", "Knielingen Nord"]),
    ("1", "tram", "Stadtwerke", ["Durlach Turmberg", "Gottesauer Platz", "Durlacher Tor", "Marktplatz", "Europaplatz", "Mühlburger Tor"]),
    ("2", "tram", "Stadtwerke", ["Waldstadt", "Hagsfeld Bahnhof", "Tivoli", "Kronenplatz", "Ettlinger Tor", "Rüppurr Kirche"]),
    ("3", "tram", "Stadtwerke", ["Entenfang", "Hauptbahnhof", "Kronenplatz", "Marktplatz", "Kaiserplatz"]),
    ("12", "bus", "Stadtwerke", ["Neureut Kirchfeld", "Knielingen Nord", "Entenfang", "Europaplatz", "Ettlinger Tor"]),
    ("73", "bus", "Regiobus", ["Waldstadt", "Tivoli", "Gottesauer Platz", "Rüppurr Kirche", "Ettlingen Stadt"]),
]

WEATHER = ["sun", "sun", "sun", "cloud", "cloud", "rain", "rain", "snow"]
DAYS = [datetime(2026, 11, 2), datetime(2026, 11, 3), datetime(2026, 11, 4)]
HOURS = (6, 7, 8, 12, 16, 17, 20)
MODE_BASE_DELAY = {"sbahn": 2.5, "tram": 1.2, "bus": 2.0}


def _delay(rng: random.Random, mode: str, weather: str, hour: int) -> int:
    base = MODE_BASE_DELAY[mode]
    if weather == "rain":
        base += 1.0
    if weather == "snow":
        base += 3.0
    if hour in (7, 8, 16, 17):
        base += 1.5
    return max(0, round(rng.gauss(base, 2.0)))


def _boarded(rng: random.Random, mode: str, zone: int, hour: int) -> int:
    base = {"sbahn": 60, "tram": 35, "bus": 18}[mode]
    if hour in (7, 8, 16, 17):
        base *= 1.8
    if zone == 1:
        base *= 1.4
    return max(0, round(rng.gauss(base, base * 0.3)))


def _generate_events(rng: random.Random) -> list[dict]:
    """One dict per (trip, stop) with all attributes; both databases derive from it."""
    zone_of = {name: zone for name, zone, _ in STOPS}
    events: list[dict] = []
    trip_id = 0
    for day in DAYS:
        weather_by_hour = {h: rng.choice(WEATHER) for h in HOURS}
        for line, mode, _operator, stops in LINES:
            for hour in HOURS:
                weather = weather_by_hour[hour]
                for direction, ordered in (("outbound", stops), ("inbound", stops[::-1])):
                    if rng.random() < 0.15:  # not every run exists
                        continue
                    trip_id += 1
                    t = day.replace(hour=hour, minute=rng.choice([0, 10, 20, 30, 40, 50]))
                    for position, stop in enumerate(ordered, start=1):
                        t += timedelta(minutes=rng.randint(3, 6))
                        events.append(
                            {
                                "trip_id": trip_id,
                                "line": line,
                                "mode": mode,
                                "direction": direction,
                                "position": position,
                                "stop": stop,
                                "zone": zone_of[stop],
                                "scheduled": t.strftime("%Y-%m-%d %H:%M"),
                                "weather": weather,
                                "delay_min": _delay(rng, mode, weather, hour),
                                "boarded": _boarded(rng, mode, zone_of[stop], hour),
                            }
                        )
    return events


FLAT_SCHEMA = """
CREATE TABLE delays (
    id INTEGER PRIMARY KEY,
    line TEXT NOT NULL,
    mode TEXT NOT NULL,
    stop TEXT NOT NULL,
    zone INTEGER NOT NULL,
    scheduled TEXT NOT NULL,
    weather TEXT NOT NULL,
    delay_min INTEGER NOT NULL,
    boarded INTEGER NOT NULL
);
"""

NORMALIZED_SCHEMA = """
CREATE TABLE lines (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    mode TEXT NOT NULL CHECK (mode IN ('tram', 'bus', 'sbahn')),
    operator TEXT NOT NULL
);
CREATE TABLE stops (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    zone INTEGER NOT NULL CHECK (zone BETWEEN 1 AND 4),
    wheelchair INTEGER NOT NULL DEFAULT 0 CHECK (wheelchair IN (0, 1))
);
CREATE TABLE line_stops (
    line_id INTEGER NOT NULL REFERENCES lines (id),
    stop_id INTEGER NOT NULL REFERENCES stops (id),
    position INTEGER NOT NULL,
    PRIMARY KEY (line_id, stop_id)
);
CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    line_id INTEGER NOT NULL REFERENCES lines (id),
    direction TEXT NOT NULL CHECK (direction IN ('outbound', 'inbound')),
    weather TEXT NOT NULL
);
CREATE TABLE stop_events (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER NOT NULL REFERENCES trips (id),
    stop_id INTEGER NOT NULL REFERENCES stops (id),
    scheduled TEXT NOT NULL,
    delay_min INTEGER NOT NULL,
    boarded INTEGER NOT NULL
);
"""


def build_flat(path: Path) -> None:
    events = _generate_events(random.Random(SEED))
    path.unlink(missing_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(FLAT_SCHEMA)
        conn.executemany(
            "INSERT INTO delays (line, mode, stop, zone, scheduled, weather, delay_min, boarded)"
            " VALUES (:line, :mode, :stop, :zone, :scheduled, :weather, :delay_min, :boarded)",
            events,
        )
    conn.close()


def build_normalized(path: Path) -> None:
    events = _generate_events(random.Random(SEED))
    path.unlink(missing_ok=True)
    with sqlite3.connect(path) as conn:
        conn.executescript(NORMALIZED_SCHEMA)
        conn.executemany(
            "INSERT INTO stops (name, zone, wheelchair) VALUES (?, ?, ?)", STOPS
        )
        conn.executemany(
            "INSERT INTO lines (name, mode, operator) VALUES (?, ?, ?)",
            [(n, m, o) for n, m, o, _ in LINES],
        )
        for line_name, _m, _o, stops in LINES:
            for position, stop in enumerate(stops, start=1):
                conn.execute(
                    "INSERT INTO line_stops (line_id, stop_id, position) VALUES"
                    " ((SELECT id FROM lines WHERE name = ?), (SELECT id FROM stops WHERE name = ?), ?)",
                    (line_name, stop, position),
                )
        seen: set[int] = set()
        for e in events:
            if e["trip_id"] not in seen:
                seen.add(e["trip_id"])
                conn.execute(
                    "INSERT INTO trips (id, line_id, direction, weather)"
                    " VALUES (?, (SELECT id FROM lines WHERE name = ?), ?, ?)",
                    (e["trip_id"], e["line"], e["direction"], e["weather"]),
                )
            conn.execute(
                "INSERT INTO stop_events (trip_id, stop_id, scheduled, delay_min, boarded)"
                " VALUES (?, (SELECT id FROM stops WHERE name = ?), ?, ?, ?)",
                (e["trip_id"], e["stop"], e["scheduled"], e["delay_min"], e["boarded"]),
            )
    conn.close()


DATABASES = {"flat": build_flat, "kvv": build_normalized}


def build_all(directory: Path) -> dict[str, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name, builder in DATABASES.items():
        paths[name] = directory / f"{name}.db"
        builder(paths[name])
    return paths
