# Ablaufplan Übung 0: Abfragen auf einer Tabelle

Dauer: 90 Minuten. Datenbank `flat`, Tabelle `delays`. Aufgaben `0.1` bis `0.24` in der Browser-Oberfläche (`exercises/uebung-0.toml`), davon 4 Zusatzaufgaben (`0.9`, `0.13`, `0.20`, `0.24`) für Schnelle.

## Ziel

Die Studierenden stellen eigenständig Fragen an eine einzelne Tabelle: Spalten wählen, filtern, Text suchen, sortieren, zusammenfassen, gruppieren. Am Ende lesen sie aus Verspätungsdaten Aussagen heraus (Wetter, Hauptverkehrszeit, Verkehrsmittel).

## Voraussetzungen

- Keine SQL-Vorkenntnisse. Excel-Erfahrung (Filter, Pivot) hilft als Brücke.
- Laptop mit Browser (für die Übungsoberfläche) und VS Code mit der Erweiterung „SQLite Viewer“.
- Server der Übungsoberfläche läuft, `data/flat.db` ist gebaut.
- Alle Daten sind erfunden (1328 Zeilen, 2. bis 4. November 2026, 7 Linien, 20 Haltestellen, keine `NULL`-Werte). `IS NULL` kommt daher in dieser Übung nicht vor, das ist Thema von Übung 1.

## Minutenplan

| Min | Abschnitt | Inhalt | Aufgaben |
|---|---|---|---|
| 0-5 | Einstieg | `data/flat.db` in VS Code öffnen (SQLite Viewer), Tabelle `delays` zeigen | - |
| 5-9 | 1 Daten ansehen | Demo: `SELECT`, `*`, `LIMIT`, `DISTINCT`, `AS` | - |
| 9-16 | 1 Daten ansehen | Aufgabenzeit | 0.1 bis 0.3 |
| 16-20 | 2 Filtern | Demo: `WHERE`, `AND`, `OR`, `NOT`, `IN`, `BETWEEN` | - |
| 20-29 | 2 Filtern | Aufgabenzeit | 0.4 bis 0.6 |
| 29-32 | 3 Textsuche | Demo: `LIKE`, `%`, `_` | - |
| 32-39 | 3 Textsuche | Aufgabenzeit | 0.7, 0.8 (Zusatz 0.9) |
| 39-43 | 4 Sortieren | Demo: `ORDER BY`, `DESC`, `LIMIT` | - |
| 43-51 | 4 Sortieren | Aufgabenzeit | 0.10 bis 0.12 (Zusatz 0.13) |
| 51-55 | 5 Aggregieren | Demo: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `ROUND` | - |
| 55-63 | 5 Aggregieren | Aufgabenzeit | 0.14 bis 0.16 |
| 63-68 | 6 Gruppieren | Demo: `GROUP BY`, `HAVING`, `WHERE` gegen `HAVING` | - |
| 68-77 | 6 Gruppieren | Aufgabenzeit | 0.17 bis 0.19 (Zusatz 0.20) |
| 77-80 | 7 Daten erzählen etwas | Demo: Stunde mit `substr` herausschneiden | - |
| 80-86 | 7 Daten erzählen etwas | Aufgabenzeit | 0.21 bis 0.23 (Zusatz 0.24) |
| 86-90 | Abschluss | Ergebnisse besprechen, offene Fragen | - |

Faustregel: Wer im Abschnitt schneller fertig ist, macht die Zusatzaufgabe. Wer hängt, überspringt sie. Wenn die Zeit knapp wird, kürzen Sie die Aufgabenzeit von Abschnitt 3 und lassen `0.8` als Hausaufgabe, die Abschnitte 5 bis 7 haben Vorrang.

## Einstieg (0-5 min)

1. In VS Code `data/flat.db` öffnen (SQLite Viewer), Tabelle `delays` anklicken.
2. Zeigen: 9 Spalten, 1328 Zeilen. Eine Zeile ist ein Halt eines Fahrzeugs an einer Haltestelle.
3. Spalten kurz erklären:
   - `id`: laufende Nummer, eindeutig.
   - `line`, `mode`: Linie (`S1`, `1`, `12`, ...) und Verkehrsmittel (`sbahn`, `tram`, `bus`).
   - `stop`, `zone`: Haltestelle und Tarifzone 1 bis 4.
   - `scheduled`: planmäßige Zeit als Text `2026-11-02 06:43`.
   - `weather`: `sun`, `cloud`, `rain`, `snow`.
   - `delay_min`: Verspätung in Minuten, `boarded`: Einsteiger an diesem Halt.
4. Brücke: Tabelle gleich Excel-Blatt, aber SQL beschreibt, was man will, nicht wie.

## Live-Demo je Abschnitt (zum Mittippen)

Abschnitt 1: Daten ansehen

```sql
SELECT * FROM delays LIMIT 5;
SELECT line, stop, delay_min FROM delays LIMIT 5;
SELECT DISTINCT mode FROM delays;
SELECT DISTINCT zone, mode FROM delays;
SELECT stop AS haltestelle, delay_min AS verspaetung FROM delays LIMIT 5;
```

Abschnitt 2: Filtern

```sql
SELECT stop, delay_min FROM delays WHERE line = 'S2' AND delay_min >= 6;
SELECT stop, mode FROM delays WHERE mode = 'bus' OR mode = 'sbahn' LIMIT 5;
SELECT stop, zone FROM delays WHERE zone IN (1, 2) AND NOT mode = 'tram' LIMIT 5;
SELECT id, boarded FROM delays WHERE boarded BETWEEN 200 AND 250;
```

Abschnitt 3: Textsuche

```sql
SELECT DISTINCT stop FROM delays WHERE stop LIKE '%bahnhof%';
SELECT DISTINCT stop FROM delays WHERE stop LIKE 'Ett%';
SELECT DISTINCT stop FROM delays WHERE stop LIKE '%Tor';
SELECT DISTINCT line FROM delays WHERE line LIKE '_';
```

Abschnitt 4: Sortieren und Begrenzen

```sql
SELECT stop, boarded FROM delays ORDER BY boarded DESC LIMIT 5;
SELECT id, stop, delay_min FROM delays ORDER BY delay_min DESC, id ASC LIMIT 5;
SELECT stop, scheduled FROM delays WHERE line = '1' ORDER BY scheduled LIMIT 5;
```

Abschnitt 5: Aggregieren

```sql
SELECT COUNT(*) FROM delays;
SELECT COUNT(*) FROM delays WHERE mode = 'bus';
SELECT SUM(boarded), AVG(delay_min), MIN(delay_min), MAX(delay_min) FROM delays;
SELECT ROUND(AVG(delay_min), 2) FROM delays;
SELECT COUNT(DISTINCT stop) FROM delays;
```

Abschnitt 6: Gruppieren

```sql
SELECT mode, COUNT(*) FROM delays GROUP BY mode;
SELECT line, ROUND(AVG(delay_min), 2) FROM delays GROUP BY line;
SELECT line, ROUND(AVG(delay_min), 2) AS avg_delay FROM delays
WHERE zone = 1 GROUP BY line HAVING AVG(delay_min) > 3;
```

Abschnitt 7: Daten erzählen etwas

```sql
SELECT scheduled, substr(scheduled, 12, 2) AS stunde FROM delays LIMIT 5;
SELECT strftime('%H', scheduled) AS stunde, COUNT(*) FROM delays GROUP BY stunde;
```

Danach die Aufgaben selbst machen lassen, die Demo löst keine Aufgabe vor.

## Typische Stolpersteine

- Text in einfachen Anführungszeichen (`'S1'`), Zahlen ohne. Doppelte Anführungszeichen führen zu Fehlern oder falschen Ergebnissen.
- `=` statt `==`, Ungleich ist `<>` (oder `!=`).
- `line` ist Text: `'1'` und `1` sind nicht dasselbe, Linien wie `S1` und `12` stehen in Anführungszeichen.
- `LIKE` achtet in SQLite nicht auf Groß- und Kleinschreibung: `'%platz%'` findet auch `Gottesauer Platz`.
- `AND` vor `OR`: bei Mischung Klammern setzen.
- `SELECT DISTINCT` gilt für die ganze Spaltenliste, nicht nur für die erste Spalte.
- `LIMIT` ohne `ORDER BY` liefert beliebige Zeilen. Bei Gleichstand an der Schnittkante entscheidet erst eine zweite Sortierspalte (hier `id`).
- Reihenfolge der Klauseln: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`.
- `WHERE` filtert Zeilen vor dem Gruppieren, `HAVING` Gruppen danach. `WHERE AVG(...) > 3` führt zu einem Fehler.
- Spaltenanzahl muss stimmen: Die Prüfung vergleicht Ergebniszeilen, Spaltennamen sind egal, die Zahl der Spalten nicht.
- Stunde in 0.21 und 0.24: `substr` und `strftime('%H', ...)` liefern Text wie `07`. `CAST(... AS INTEGER)` liefert `7` und passt nicht zur Lösung.
- Runden: `ROUND(AVG(x), 2)` steht in der Klammer, sonst bleibt der Durchschnitt ungerundet.

## Erwartungswerte für die Besprechung

Alle Werte stammen aus der gebauten Datenbank (Seed 42).

| Aufgabe | Erwartung |
|---|---|
| 0.3 | 7 Zeilen (`S1`, `S2`: sbahn; `1`, `2`, `3`: tram; `12`, `73`: bus) |
| 0.4 | 50 Zeilen (Verspätung ab 8 Minuten) |
| 0.5 | 33 Zeilen |
| 0.6 | 52 Zeilen |
| 0.7 | 5 Haltestellen: Gottesauer Platz, Marktplatz, Europaplatz, Kronenplatz, Kaiserplatz |
| 0.8 | 2 Haltestellen: Durlacher Tor, Durlach Turmberg |
| 0.9 (Zusatz) | Linien `12` und `73` |
| 0.10 | Platz 1: `id` 533, `S2`, Grötzingen, 12 Minuten. Plätze 2 bis 4 haben je 10 Minuten (`id` 473, 613, 806), Platz 5: `id` 453 mit 9 |
| 0.11 | `id` 944 (234 Einsteiger), 540 (221), 919 (217) |
| 0.13 (Zusatz) | Plätze 6 bis 10: alle 9 Minuten, `id` 457, 539, 542, 697, 703 |
| 0.14 | 123 Halte bei Schnee |
| 0.15 | 35997 Einsteiger, 3.99 Minuten im Schnitt, Maximum 12 |
| 0.16 | 20 Haltestellen, 7 Linien (`Messe Süd` hat keine Halte in `delays`) |
| 0.17 | `S2` 190 Halte / 19167 Einsteiger, `S1` 160 / 16830, `2` 240 / 14452, `1` 228 / 14513, `3` 160 / 11031, `12` 175 / 5711, `73` 175 / 4705 |
| 0.18 | Zone 1: 4.23, Zone 2: 3.85, Zone 3: 3.8, Zone 4: 6.03 |
| 0.19 | 6 Haltestellen: Pfinztal Berghausen 4.81, Ettlingen Stadt 4.15, Durlacher Tor 3.87, Grötzingen 3.76, Neureut Kirchfeld 3.69, Hauptbahnhof 3.55 |
| 0.20 (Zusatz) | `S1` 76, `S2` 67, `73` 59, `1` 55, `12` 51 |
| 0.21 | Meiste Einsteiger: 08 Uhr (15371), 17 Uhr (14643), 16 Uhr (14332), 07 Uhr (13451). Die Stunden 06, 12 und 20 liegen bei etwa 6000 bis 6900, 09, 13, 18 und 21 sind Randstunden einzelner Fahrten (wenige Zeilen) |
| 0.22 | `sbahn` 350 Halte, 3.99, Maximum 12. `bus` 350, 3.44, 10. `tram` 628, 2.72, 10 |
| 0.23 | `snow` 5.8, `rain` 4.3, `cloud` 2.8, `sun` 2.5 |
| 0.24 (Zusatz) | `Hauptverkehr` 757 Halte mit 3.83, `sonst` 571 Halte mit 2.47 |

### Diskussionsfragen für den Abschluss (86-90 min)

- Wirkt sich Schnee aus? Ja: im Schnitt etwa 3,3 Minuten mehr als bei Sonne (5.8 gegen 2.5). Regen bringt etwa 1,8 Minuten.
- Hauptverkehrszeit: Morgens (07, 08) und nachmittags (16, 17) steigen etwa doppelt so viele Fahrgäste ein, und die Verspätung ist höher.
- Verkehrsmittel: S-Bahn ist am unpünktlichsten, Tram am pünktlichsten. Vorsicht beim Schluss auf Ursache: Das Wetter wechselt stundenweise und verteilt sich nicht gleichmäßig auf die Verkehrsmittel. Eine Korrelation in einer Gruppierung ist noch kein Beweis, das Thema „Störgrößen“ kurz anreißen.
- Überleitung zu Übung 1: In `delays` steht der Linien- und Haltestellenname in jeder Zeile wieder. Wie ginge das ohne Wiederholung? Mehrere Tabellen und `JOIN`.
