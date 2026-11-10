# SQL-Einführung (HKA VSM)

Zwei Übungen à 90 Minuten, in denen ihr SQL an Daten ausprobiert: Verspätungen im ÖPNV einer fiktiven Stadt. Im Browser seht ihr die Aufgabe, tippt eure Abfrage, und ein Knopf „Prüfen“ sagt sofort, ob das Ergebnis stimmt. Nichts davon kann etwas kaputt machen: Die Daten sind erfunden und lassen sich jederzeit zurücksetzen.

| | Datenbank | Thema |
|---|---|---|
| Übung 0 | `flat.db` | Abfragen auf einer Tabelle: filtern, sortieren, zählen, gruppieren |
| Übung 1 | `kvv.db` | Mehrere Tabellen: Schlüssel, Subqueries, JOIN |

## Schnellstart

Ihr braucht zwei Dinge: **uv** (startet das Projekt und installiert Python bei Bedarf selbst) und dieses Repo.

### 1. uv installieren (einmalig, ca. 1 Minute)

Terminal öffnen (macOS: Programm „Terminal“, Windows: „PowerShell“) und **einen** Befehl einfügen.

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Danach das Terminal **schließen und neu öffnen**. Prüfen mit `uv --version`.

Habt ihr schon Python mit `pip`, geht auch: `pip install uv`.

### 2. Projekt holen und starten

```bash
git clone <URL-dieses-Repos> hka-sql-intro
cd hka-sql-intro
uv run uebung0
```

Für die zweite Übung entsprechend `uv run uebung1`. Beim ersten Start lädt uv alles Nötige (ein paar Sekunden). Dann öffnet sich der Browser mit den Aufgaben. Beenden mit Strg+C im Terminal. Ohne `git`: Repo als ZIP herunterladen, entpacken und im entpackten Ordner `uv run uebung0` ausführen.

Ist Port 8000 schon belegt: `uv run uebung0 --port 8001`.

### Ohne uv: klassisch mit venv

Funktioniert mit Python 3.11 oder neuer:

```bash
python -m venv .venv
```

Aktivieren: macOS/Linux `source .venv/bin/activate`, Windows `.venv\Scripts\activate`. Danach:

```bash
pip install -e .
uebung0
```

## Die ersten 5 Minuten: Datenbank ansehen

Beim ersten Start entsteht der Ordner `data/` mit `flat.db` und `kvv.db`. So schaut ihr hinein, bevor ihr Abfragen schreibt:

1. Repo-Ordner in VS Code öffnen.
2. Erweiterung **SQLite Viewer** installieren (Extensions-Symbol, „SQLite Viewer“ suchen).
3. `data/flat.db` anklicken. Links stehen die Tabellen, rechts die Zeilen.

Was ihr im SQLite Viewer seht, ist genau das, was eure Abfragen im Browser durchsuchen.

## So arbeitet ihr im Browser

- Links seht ihr die Abschnitte der Übung als Perlenschnur, jeder Abschnitt bringt eine neue Sache. Die Aufgaben des Abschnitts, in dem ihr gerade seid, sind aufgeklappt. Erledigtes ist lila, die aktuelle Aufgabe grün.
- **Ausführen** (oder Strg+Enter / Cmd+Enter) zeigt das Ergebnis eurer Abfrage, **Prüfen** vergleicht es mit der Musterlösung. Es zählt das Ergebnis, nicht wie ihr es formuliert.
- **Tipp** hilft, ohne die Lösung zu verraten. **Lösung zeigen** gibt es erst nach einem Prüfen-Versuch.
- Erledigte Aufgaben merkt sich der Browser. **Datenbank zurücksetzen** stellt den Anfangszustand wieder her.

## Zurechtfinden

| Ordner | Inhalt |
|---|---|
| `exercises/` | Aufgaben mit Musterlösung (`uebung-0.toml`, `uebung-1.toml`) |
| `ablauf/` | Ablaufpläne für die Dozentenseite mit Minutenplan und Demo-Abfragen |
| `data/` | erzeugte Datenbanken, in VS Code ansehbar (nicht im Git) |
| `src/sqlkurs/` | Code: Datenerzeugung, Prüfung, Webserver, Oberfläche |
| `tests/` | Tests, u. a. „jede Musterlösung besteht ihre eigene Prüfung“ |

## So funktioniert es

- **Übung 0** nutzt `flat`: eine Tabelle `delays` (Linie, Haltestelle, Verspätung, Einsteiger, Wetter).
- **Übung 1** nutzt `kvv`: dieselben Daten, verteilt auf `lines`, `stops`, `line_stops`, `trips` und `stop_events`. So erlebt man, warum man Tabellen aufteilt und wieder verbindet.
- Eingaben laufen auf einer Arbeitskopie. `ATTACH` und `PRAGMA` sind gesperrt. Der Server lauscht nur auf `127.0.0.1`, ist also von außen nicht erreichbar.
- Die Daten werden mit festem Startwert erzeugt: bei allen Studierenden identisch.

## Selbst weitermachen

**Aufgabe ergänzen:** In `exercises/uebung-0.toml` oder `uebung-1.toml` einen `[[exercise]]`-Block anhängen (`id`, `section`, `title`, `task`, `hint`, `solution`, optional `ordered = true` wenn die Reihenfolge zählt). Dann `uv run pytest`: der Test prüft, dass die Lösung Zeilen liefert und besteht.

**Daten ändern:** In `src/sqlkurs/data.py` Linien, Haltestellen oder Wahrscheinlichkeiten anpassen, dann `uv run sqlkurs build`. Aufgaben danach mit `uv run pytest` prüfen.

**Weitere Themen** (INSERT/UPDATE/DELETE): Ein Aufgabentyp für Änderungen müsste in `engine.check` ergänzt werden (Änderung auf Kopie ausführen, dann eine Prüfabfrage vergleichen).

## Befehle

| Befehl | Wirkung |
|---|---|
| `uv run uebung0` | Übung 0 starten, Browser öffnet sich |
| `uv run uebung1` | Übung 1 starten, Browser öffnet sich |
| `uv run uebung0 --port 8001` | anderen Port nutzen |
| `uv run uebung0 --no-browser` | Browser nicht automatisch öffnen |
| `uv run sqlkurs build` | Datenbanken in `data/` neu erzeugen |
| `uv run sqlkurs list` | Aufgaben auflisten |

Es gibt keine Umgebungsvariablen und keine Zugangsdaten.

## Tests

```bash
uv run --group test pytest --cov
```

## Weiterführendes

[CLAUDE.md](CLAUDE.md) für die Arbeit mit Claude Code. Konzept und Aufgabenidee nach CS50 SQL (Harvard, CC BY-NC-SA 4.0); Aufgaben und Daten hier sind eigene Arbeiten und keine Kopien des Originals.
