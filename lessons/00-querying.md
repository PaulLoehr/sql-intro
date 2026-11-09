# Lecture 0: Querying

Orientierung: [CS50 SQL, Lecture 0 „Querying“](https://cs50.harvard.edu/sql/). Dort ist es eine Liste von Buchpreis-Kandidaten, hier eine Tabelle mit Verspätungsdaten aus dem ÖPNV (passt zu VSM). Alle Daten sind erfunden.

**Ziel:** Studierende können Fragen an eine einzelne Tabelle stellen.
**Datenbank:** `flat` (Tabelle `delays`, 1 Zeile = 1 Halt eines Fahrzeugs). Aufgaben 0.1 bis 0.8 in der Browser-Oberfläche.

## Ablauf (ca. 45 Minuten)

| Min | Was | Wie |
|---|---|---|
| 0–10 | Was ist eine Datenbank, was ist SQL? Tabelle = Excel-Blatt, aber mit Regeln | Folie, dann `uv run sqlkurs shell flat`, `.schema` zeigen |
| 10–20 | `SELECT`, `DISTINCT`, `WHERE`, `LIKE`, `ORDER BY`, `LIMIT` | Live-Demo, dann Aufgaben 0.1 bis 0.4 |
| 20–35 | Aggregate: `COUNT`, `SUM`, `AVG`, `GROUP BY`, `HAVING` | Live-Demo, dann Aufgaben 0.5 bis 0.7 |
| 35–45 | Daten erzählen etwas: Gilt „bei Schnee mehr Verspätung“? | Aufgabe 0.8 gemeinsam, Diskussion |

## Live-Demo (zum Mittippen)

```sql
SELECT * FROM delays LIMIT 5;
SELECT DISTINCT line FROM delays;
SELECT stop, delay_min FROM delays WHERE line = 'S1' AND delay_min > 8;
SELECT COUNT(*) FROM delays;
SELECT line, AVG(delay_min) FROM delays GROUP BY line;
```

## Stolpersteine

- Zeichenketten in einfachen Anführungszeichen, `=` statt `==`.
- `WHERE` filtert Zeilen vor dem Gruppieren, `HAVING` Gruppen danach.
- `AVG` über Ganzzahlen liefert Kommazahlen, `ROUND` zum Lesen nutzen.
- Fehlende Werte sind `NULL`, nicht 0 (kommt in Lecture 1 vor).

## Bezug zum Kurs

Lösungen sind in `exercises/0-querying.toml` (Feld `solution`) und über den Button „Lösung zeigen“ abrufbar. Die Prüfung vergleicht Ergebnisse, nicht den SQL-Text: jede richtige Formulierung zählt.
