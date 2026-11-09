# SQL-Einführung (HKA VSM)

Eine interaktive Einführung in SQL und Datenbanken, aufgebaut wie die ersten beiden Lectures von [CS50 SQL](https://cs50.harvard.edu/sql/) (Lecture 0 „Querying“, Lecture 1 „Relating“). Statt Buchpreisen und U-Bahn aus dem Original gibt es ÖPNV-Daten mit Verspätungen, passend zum Studiengang. Die Daten sind erfunden und werden bei jedem Start identisch erzeugt.

Im Browser stehen Aufgaben, ein SQL-Feld und ein „Prüfen“-Knopf, der das Ergebnis mit der Musterlösung vergleicht. Man kann das Ganze auf dem Beamer vorführen und Studierende bei sich selbst laufen lassen.

## Schnellstart

Voraussetzungen: [uv](https://docs.astral.sh/uv/) (installiert Python 3.13 selbst). Für die Konsole zusätzlich `sqlite3` (auf macOS vorhanden).

```bash
uv sync
uv run sqlkurs serve
```

Dann `http://127.0.0.1:8000` öffnen. Links eine Aufgabe wählen, Abfrage eintippen, mit Strg+Enter ausführen, mit „Prüfen“ kontrollieren. Erledigte Aufgaben bekommen einen Haken (im Browser gespeichert).

## Zurechtfinden

| Ordner | Inhalt |
|---|---|
| `lessons/` | Ablaufpläne mit Live-Demo-Abfragen je Lecture (Deutsch) |
| `exercises/` | Aufgaben mit Musterlösung als TOML |
| `src/sqlkurs/` | Code: Datenerzeugung, Prüfung, Webserver |
| `tests/` | Tests, u. a. „jede Musterlösung besteht ihre eigene Prüfung“ |
| `data/` | erzeugte Datenbanken (nicht im Git) |

## So funktioniert es

- **Lecture 0** nutzt `flat`: eine einzige Tabelle `delays` (Linie, Haltestelle, Verspätung, Einsteiger, Wetter).
- **Lecture 1** nutzt `kvv`: dieselben Daten, auf `lines`, `stops`, `line_stops`, `trips` und `stop_events` verteilt. So erlebt man, warum man Tabellen aufteilt und wieder verbindet.
- Eingaben laufen auf einer Arbeitskopie; „Datenbank zurücksetzen“ stellt den Ausgangszustand her. `ATTACH` und `PRAGMA` sind gesperrt. Der Server lauscht nur auf `127.0.0.1`.

Wochenplan und Demo-Abfragen: [Lecture 0](lessons/00-querying.md), [Lecture 1](lessons/01-relating.md).

## Selbst weitermachen

**Aufgabe ergänzen:** In `exercises/0-querying.toml` oder `1-relating.toml` einen `[[exercise]]`-Block anhängen (`id`, `lesson`, `title`, `db`, `task`, `hint`, `solution`, optional `ordered = true`, wenn die Reihenfolge zählt). Dann `uv run pytest`: der Test prüft, dass die Lösung Zeilen liefert und besteht.

**Daten ändern:** In `src/sqlkurs/data.py` Linien, Haltestellen oder Wahrscheinlichkeiten anpassen, dann `uv run sqlkurs build` (Seed fest, Ergebnis reproduzierbar). Aufgaben danach mit `uv run pytest` prüfen.

**Weitere CS50-Lectures:** Writing (INSERT/UPDATE/DELETE), Viewing, Optimizing sind bewusst nicht enthalten. Ein Aufgabentyp für Änderungen müsste in `engine.check` ergänzt werden (Änderung auf Kopie ausführen, dann eine Prüfabfrage vergleichen).

## Konfiguration

| Option | Bedeutung | Standard |
|---|---|---|
| `serve --port` | Port des Webservers | 8000 |
| `shell <db>` | `flat` oder `kvv` in `sqlite3` öffnen | – |

Es gibt keine Umgebungsvariablen und keine Zugangsdaten.

## Tests und Qualität

```bash
uv run pytest --cov
```

## Weiterführendes

[CLAUDE.md](CLAUDE.md) für die Arbeit mit Claude Code. Konzept und Aufgabenidee nach CS50 SQL (Harvard, CC BY-NC-SA 4.0); Aufgaben und Daten hier sind eigene Arbeiten und keine Kopien des Originals.
