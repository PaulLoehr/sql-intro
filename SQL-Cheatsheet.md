# SQL: Einführung und Cheat-Sheet

Kurze Einführung und Übersicht aller Befehle, die ihr in Übung 0 und Übung 1 braucht. Die Beispiele laufen auf den Übungsdatenbanken, lösen aber keine der Aufgaben.

## Inhalt

1. [Grundidee](#1-grundidee)
2. [Die Datenbanken](#2-die-datenbanken)
3. [Reihenfolge einer Abfrage](#3-reihenfolge-einer-abfrage)
4. [Übung 0: eine Tabelle abfragen](#4-übung-0-eine-tabelle-abfragen)
5. [Übung 1: Tabellen verknüpfen](#5-übung-1-tabellen-verknüpfen)
6. [Funktionen für Text, Zahlen und Zeit](#6-funktionen-für-text-zahlen-und-zeit)
7. [Häufige Fehler](#7-häufige-fehler)
8. [Spickzettel auf einer Seite](#8-spickzettel-auf-einer-seite)

---

## 1. Grundidee

Eine **relationale Datenbank** speichert Daten in **Tabellen**. Jede Tabelle hat **Spalten** (Eigenschaften, z. B. `stop`) und **Zeilen** (einzelne Datensätze).

**SQL** (Structured Query Language) ist die Sprache, mit der ihr der Datenbank sagt, *was* ihr sehen wollt, nicht *wie* sie es berechnen soll. In diesem Kurs lest ihr nur Daten (`SELECT`), ihr verändert nichts.

```sql
SELECT line, stop
FROM delays
WHERE delay_min > 10;
```

Regeln, die immer gelten:

- Jede Abfrage endet mit einem **Semikolon** `;`.
- **Schlüsselwörter** (`SELECT`, `FROM`, …) sind nicht von Groß- und Kleinschreibung abhängig. Üblich ist Großschreibung, das liest sich besser.
- **Text** steht in **einfachen** Anführungszeichen: `'snow'`. Zahlen stehen ohne: `5`.
- **Textvergleiche mit `=`** unterscheiden Groß- und Kleinschreibung: `'Snow'` ist nicht `'snow'`.
- Zeilenumbrüche und Einrückung sind egal. Setzt jede Klausel (`FROM`, `WHERE`, …) auf eine eigene Zeile.
- Kommentare: `-- bis zum Zeilenende` oder `/* mehrzeilig */`.

---

## 2. Die Datenbanken

### `flat` (Übung 0): eine große Tabelle

**`delays`**

| Spalte      | Typ     | Bedeutung                                   |
| ----------- | ------- | ------------------------------------------- |
| `id`        | INTEGER | Primärschlüssel                             |
| `line`      | TEXT    | Linienname                                  |
| `mode`      | TEXT    | Verkehrsmittel: `tram`, `bus`, `sbahn`      |
| `stop`      | TEXT    | Haltestelle                                 |
| `zone`      | INTEGER | Tarifzone 1 bis 4                           |
| `scheduled` | TEXT    | planmäßige Zeit, z. B. `2026-11-02 07:35`   |
| `weather`   | TEXT    | Wetter, `sun`, `cloud`, `rain`, `snow`                |
| `delay_min` | INTEGER | Verspätung in Minuten                       |
| `boarded`   | INTEGER | Zahl der Einsteiger                         |

### `kvv` (Übung 1): mehrere verknüpfte Tabellen

```
lines ──< line_stops >─────── stops
  │                             │
  └──< trips ──< stop_events >──┘
```

(`──<` bedeutet: eine Zeile links gehört zu vielen Zeilen rechts.)

| Tabelle       | Spalten                                                  | Inhalt                                    |
| ------------- | -------------------------------------------------------- | ----------------------------------------- |
| `lines`       | **`id`**, `name`, `mode`, `operator`                     | Linien                                    |
| `stops`       | **`id`**, `name`, `zone`, `wheelchair` (0/1)             | Haltestellen                              |
| `line_stops`  | `line_id` → lines, `stop_id` → stops, `position`         | welche Linie hält wo, in welcher Reihenfolge |
| `trips`       | **`id`**, `line_id` → lines, `direction`, `weather`      | einzelne Fahrten                          |
| `stop_events` | **`id`**, `trip_id` → trips, `stop_id` → stops, `scheduled`, `delay_min`, `boarded` | ein Halt einer Fahrt an einer Haltestelle |

**Fett** = **Primärschlüssel** (benennt jede Zeile eindeutig). `→` = **Fremdschlüssel** (verweist auf den Primärschlüssel einer anderen Tabelle). Über diese Paare verknüpft ihr Tabellen.

`line_stops` ist eine **Brückentabelle**: Eine Linie hält an vielen Haltestellen, eine Haltestelle wird von vielen Linien bedient. Dafür braucht es eine Tabelle dazwischen.

---

## 3. Reihenfolge einer Abfrage

So schreibt man die Klauseln (jede ist optional außer `SELECT`):

```sql
SELECT   spalten            -- 5. was wird ausgegeben
FROM     tabelle            -- 1. woher
JOIN     andere ON ...      -- 2. Tabellen verknüpfen
WHERE    bedingung          -- 3. einzelne Zeilen filtern
GROUP BY spalten            -- 4. Gruppen bilden
HAVING   bedingung          -- 6. Gruppen filtern
ORDER BY spalten            -- 7. sortieren
LIMIT    n OFFSET m;        -- 8. abschneiden
```

Geschrieben wird von oben nach unten, **gedacht** wird in der Zahlenreihenfolge: erst die Tabelle(n), dann filtern, gruppieren, ausgeben, sortieren, abschneiden.

---

## 4. Übung 0: eine Tabelle abfragen

### SELECT und FROM: Spalten auswählen

```sql
SELECT * FROM delays;                  -- alle Spalten
SELECT line, stop FROM delays;         -- nur diese Spalten, in dieser Reihenfolge
```

### LIMIT und OFFSET: Zeilenzahl begrenzen

```sql
SELECT * FROM delays LIMIT 10;             -- die ersten 10 Zeilen
SELECT * FROM delays LIMIT 10 OFFSET 20;   -- 10 Zeilen, nachdem 20 übersprungen wurden
```

Ohne `ORDER BY` ist die Reihenfolge nicht garantiert. Wollt ihr „die ersten“ oder „die größten“, sortiert ausdrücklich.

### DISTINCT: Duplikate entfernen

```sql
SELECT DISTINCT zone FROM delays;          -- jeder Wert einmal
SELECT DISTINCT line, mode FROM delays;    -- jede Kombination einmal
```

### AS: Spalten umbenennen (Alias)

```sql
SELECT stop AS haltestelle, delay_min AS minuten FROM delays;
```

### WHERE: Zeilen filtern

```sql
SELECT * FROM delays WHERE zone = 2;
SELECT * FROM delays WHERE mode = 'bus';
```

**Vergleichsoperatoren**

| Operator       | Bedeutung            |
| -------------- | -------------------- |
| `=`            | gleich               |
| `<>` oder `!=` | ungleich             |
| `<`, `<=`      | kleiner, kleiner gleich |
| `>`, `>=`      | größer, größer gleich   |

**Bedingungen kombinieren**

| Schlüsselwort | Bedeutung                       |
| ------------- | ------------------------------- |
| `AND`         | beide Bedingungen müssen gelten |
| `OR`          | mindestens eine muss gelten     |
| `NOT`         | verneint eine Bedingung         |

`AND` bindet stärker als `OR`. Im Zweifel **Klammern** setzen:

```sql
SELECT * FROM delays
WHERE (mode = 'bus' OR mode = 'tram') AND delay_min > 5;
```

**IN: Wert steht in einer Liste**

```sql
SELECT * FROM delays WHERE weather IN ('sun', 'cloud');
SELECT * FROM delays WHERE zone NOT IN (1, 2);
```

**BETWEEN: Wert liegt in einem Bereich (Grenzen eingeschlossen)**

```sql
SELECT * FROM delays WHERE delay_min BETWEEN 3 AND 6;   -- 3, 4, 5, 6
```

**LIKE: Textmuster**

| Platzhalter | Bedeutung                                   |
| ----------- | ------------------------------------------- |
| `%`         | beliebig viele beliebige Zeichen (auch null) |
| `_`         | genau ein beliebiges Zeichen                |

```sql
WHERE stop LIKE 'Markt%'     -- beginnt mit "Markt"
WHERE stop LIKE '%straße'    -- endet auf "straße"
WHERE stop LIKE '%brücke%'   -- enthält "brücke"
WHERE line LIKE 'N_'         -- "N" plus genau ein Zeichen
WHERE stop NOT LIKE '%a%'    -- enthält kein "a"
```

`LIKE` achtet in SQLite bei normalen Buchstaben **nicht** auf Groß- und Kleinschreibung.

**NULL: fehlender Wert**

`NULL` heißt „unbekannt/nicht vorhanden“. Mit `= NULL` findet man nichts, es heißt:

```sql
WHERE spalte IS NULL
WHERE spalte IS NOT NULL
```

### ORDER BY: sortieren

```sql
SELECT * FROM delays ORDER BY delay_min;               -- aufsteigend (ASC ist Standard)
SELECT * FROM delays ORDER BY delay_min DESC;          -- absteigend
SELECT * FROM delays ORDER BY stop ASC, boarded DESC;  -- erst nach stop, bei Gleichstand nach boarded
```

Mit `LIMIT` ergibt das Ranglisten: erst `WHERE`, dann `ORDER BY`, dann `LIMIT`.

### Aggregatfunktionen: viele Zeilen zu einem Wert

| Funktion          | Ergebnis                                   |
| ----------------- | ------------------------------------------ |
| `COUNT(*)`        | Anzahl Zeilen                              |
| `COUNT(spalte)`   | Anzahl Zeilen, in denen `spalte` nicht `NULL` ist |
| `COUNT(DISTINCT spalte)` | Anzahl verschiedener Werte          |
| `SUM(spalte)`     | Summe                                      |
| `AVG(spalte)`     | Durchschnitt                               |
| `MIN(spalte)`, `MAX(spalte)` | kleinster, größter Wert         |
| `ROUND(wert, n)`  | auf `n` Nachkommastellen runden            |

```sql
SELECT COUNT(*) FROM delays WHERE zone = 3;
SELECT ROUND(AVG(delay_min), 2) AS schnitt, MAX(delay_min) AS maximum FROM delays;
```

Ohne `GROUP BY` fasst eine Aggregatfunktion die **ganze** Tabelle (nach `WHERE`) zu **einer** Zeile zusammen.

### GROUP BY: pro Gruppe rechnen

```sql
SELECT zone, COUNT(*) AS anzahl, ROUND(AVG(delay_min), 1) AS schnitt
FROM delays
GROUP BY zone;
```

Eine Zeile pro Wert in `zone`. Gruppieren kann man auch nach mehreren Spalten oder nach einem Ausdruck:

```sql
GROUP BY mode, weather
GROUP BY substr(stop, 1, 1)      -- nach dem Anfangsbuchstaben
```

**Faustregel:** Im `SELECT` stehen nur (a) die Spalten, nach denen gruppiert wird, und (b) Aggregatfunktionen.

### HAVING: Gruppen filtern

`WHERE` filtert **Zeilen vor** dem Gruppieren, `HAVING` filtert **Gruppen nach** dem Gruppieren (also Bedingungen auf `COUNT`, `AVG`, …).

```sql
SELECT stop, COUNT(*) AS anzahl
FROM delays
WHERE weather = 'rain'          -- Zeilen vorher aussortieren
GROUP BY stop
HAVING COUNT(*) > 20            -- Gruppen nachher aussortieren
ORDER BY anzahl DESC;
```

### CASE: Bedingungen im SELECT

Erzeugt eine neue Spalte aus Wenn-dann-Regeln. Man kann danach gruppieren.

```sql
SELECT
    CASE
        WHEN delay_min = 0 THEN 'pünktlich'
        WHEN delay_min <= 5 THEN 'leicht'
        ELSE 'stark'
    END AS kategorie,
    COUNT(*) AS anzahl
FROM delays
GROUP BY kategorie;
```

Einen Alias aus dem `SELECT` dürft ihr in SQLite in `GROUP BY` und `ORDER BY` verwenden.

---

## 5. Übung 1: Tabellen verknüpfen

### Warum mehrere Tabellen?

In `kvv` steht der Linienname nur **einmal** in `lines`. Alle anderen Tabellen verweisen per Nummer darauf (Fremdschlüssel). Das spart Platz und verhindert Widersprüche. Um Namen statt Nummern zu sehen, müssen die Tabellen **verknüpft** werden.

### Subquery: Abfrage in der Abfrage

Eine Subquery steht in Klammern und liefert ein Ergebnis, das die äußere Abfrage nutzt.

**Ein einzelner Wert** (eine Zeile, eine Spalte): Vergleich mit `=`, `<`, `>`, …

```sql
SELECT name FROM stops
WHERE zone = (SELECT zone FROM stops WHERE name = 'Marktplatz');

SELECT COUNT(*) FROM stop_events
WHERE boarded > (SELECT AVG(boarded) FROM stop_events);
```

**Eine Liste von Werten** (eine Spalte, mehrere Zeilen): Vergleich mit `IN`

```sql
SELECT name FROM stops
WHERE id IN (SELECT stop_id FROM line_stops WHERE line_id = 2);
```

Subqueries lassen sich verschachteln. Die innerste wird zuerst ausgewertet.

### JOIN: Tabellen nebeneinanderlegen

```sql
SELECT trips.id, lines.name
FROM trips
JOIN lines ON trips.line_id = lines.id;
```

- `JOIN tabelle ON bedingung`: hängt Zeilen der zweiten Tabelle an die der ersten, wenn die Bedingung passt.
- Die Bedingung vergleicht fast immer **Fremdschlüssel = Primärschlüssel**.
- Es bleiben nur Zeilen übrig, die einen **Partner** haben. (`JOIN` ist dasselbe wie `INNER JOIN`.)

**Spalten qualifizieren:** Gibt es einen Spaltennamen in mehreren Tabellen (`id`, `name`, `zone`, …), schreibt `tabelle.spalte`. Sonst meldet SQL „ambiguous column name“.

**Aliase für Tabellen** machen das kürzer:

```sql
SELECT t.id, l.name AS line_name
FROM trips AS t
JOIN lines AS l ON t.line_id = l.id;
```

Hat eine Tabelle einen Alias, nutzt man **nur noch den Alias**.

**Mehr als zwei Tabellen:** `JOIN` einfach anhängen. Jeder `JOIN` braucht sein eigenes `ON`.

```sql
SELECT l.name AS line_name, s.name AS stop_name
FROM lines AS l
JOIN line_stops AS ls ON ls.line_id = l.id
JOIN stops      AS s  ON s.id = ls.stop_id;
```

**Tipp zum Vorgehen:** Zeichnet den Weg durch das Schema (siehe Diagramm oben): Welche Tabellen enthalten die gewünschten Spalten? Welche Brücken liegen dazwischen?

### LEFT JOIN: auch Zeilen ohne Partner behalten

`JOIN` wirft Zeilen weg, die keinen Partner haben. `LEFT JOIN` behält **alle Zeilen der linken Tabelle**. Fehlt der Partner, sind die Spalten der rechten Tabelle `NULL`.

```sql
SELECT s.name, ls.line_id
FROM stops AS s
LEFT JOIN line_stops AS ls ON ls.stop_id = s.id;
```

Typische Muster:

```sql
-- Zeilen ohne Partner finden
... LEFT JOIN b ON b.a_id = a.id
WHERE b.a_id IS NULL

-- Auch Gruppen mit Anzahl 0 zeigen: eine Spalte der RECHTEN Tabelle zählen
SELECT a.name, COUNT(b.id) AS anzahl
FROM a LEFT JOIN b ON b.a_id = a.id
GROUP BY a.id, a.name
```

Achtung:

- `COUNT(*)` zählt auch die `NULL`-Zeile als 1, `COUNT(b.id)` zählt sie als 0.
- Eine Bedingung auf die rechte Tabelle in `WHERE` löscht die Zeilen ohne Partner wieder (denn `NULL = 'x'` ist nie wahr). Soll die Bedingung nur beeinflussen, was *verknüpft* wird, gehört sie ins `ON`: `LEFT JOIN b ON b.a_id = a.id AND b.typ = 'x'`.

### JOIN, GROUP BY, HAVING kombinieren

Erst verknüpfen, dann filtern, gruppieren, Gruppen filtern, sortieren:

```sql
SELECT l.mode, COUNT(*) AS anzahl, ROUND(AVG(e.delay_min), 2) AS schnitt
FROM stop_events AS e
JOIN trips AS t ON t.id = e.trip_id
JOIN lines AS l ON l.id = t.line_id
WHERE e.boarded > 0
GROUP BY l.mode
HAVING COUNT(*) > 100
ORDER BY schnitt DESC;
```

---

## 6. Funktionen für Text, Zahlen und Zeit

| Funktion                       | Zweck                                | Beispiel → Ergebnis                         |
| ------------------------------ | ------------------------------------ | ------------------------------------------- |
| `ROUND(x, n)`                  | runden                               | `ROUND(3.14159, 2)` → `3.14`                |
| `ABS(x)`                       | Betrag                               | `ABS(-4)` → `4`                             |
| `LENGTH(text)`                 | Zeichenzahl                          | `LENGTH('Bus')` → `3`                       |
| `UPPER(text)`, `LOWER(text)`   | Groß-/Kleinschreibung                | `UPPER('bus')` → `'BUS'`                    |
| `substr(text, start, länge)`   | Teilstring (Start zählt ab **1**)    | `substr('2026-11-02 07:35', 12, 2)` → `'07'` |
| `a \|\| b`                     | Texte aneinanderhängen               | `'Linie ' \|\| name`                        |
| `strftime(format, zeit)`       | Teil eines Zeitstempels als Text     | `strftime('%H', '2026-11-02 07:35')` → `'07'` |
| `CAST(x AS INTEGER)`           | Typ umwandeln                        | `CAST('07' AS INTEGER)` → `7`               |

**`strftime`-Formate:** `%Y` Jahr, `%m` Monat, `%d` Tag, `%H` Stunde (00 bis 23), `%M` Minute, `%w` Wochentag (0 = Sonntag).

**Ganzzahl-Division:** `7 / 2` ergibt in SQLite `3`. Für Kommazahlen eine Seite als Kommazahl schreiben: `7 * 1.0 / 2` → `3.5`.

Zeiten sind hier einfach **Text** im Format `JJJJ-MM-TT HH:MM`. Weil dieses Format von groß nach klein aufgebaut ist, lassen sie sich auch als Text korrekt vergleichen und sortieren.

---

## 7. Häufige Fehler

| Fehlermeldung / Symptom | Ursache und Lösung |
| ----------------------- | ------------------ |
| `no such column: ...`   | Tippfehler im Spaltennamen, oder die Spalte gehört zu einer Tabelle, die nicht in `FROM`/`JOIN` steht. Mit Text in `"..."` statt `'...'` meldet SQLite ebenfalls diesen Fehler. |
| `ambiguous column name` | Der Spaltenname existiert in mehreren Tabellen. `tabelle.spalte` oder Alias davor schreiben. |
| `near "...": syntax error` | Komma vergessen oder zu viel (vor `FROM`!), Klausel in falscher Reihenfolge, Klammer nicht geschlossen. |
| Leeres Ergebnis         | Text-Vergleich mit falscher Schreibweise (`'Snow'` statt `'snow'`), oder Bedingung zu streng. Erst ohne `WHERE` ausprobieren und `SELECT DISTINCT spalte` ansehen. |
| Ergebnis hat viel zu viele Zeilen | `JOIN` ohne passendes `ON`, oder falsche Spalten verglichen. |
| `WHERE AVG(...) > 3` → Fehler | Aggregate gehören in `HAVING`, nicht in `WHERE`. |
| Spalte im `SELECT` ist „irgendein“ Wert | Spalte steht weder im `GROUP BY` noch in einer Aggregatfunktion. |
| `= NULL` findet nichts  | `IS NULL` benutzen. |
| Durchschnitt/Division ist ganzzahlig | `* 1.0` nutzen oder `AVG` statt Handrechnung. |
| Subquery: `row value misused` o. ä. | Nach `=` darf nur **ein** Wert kommen, bei mehreren Zeilen `IN` verwenden. |

**Vorgehen, wenn eine Abfrage nicht klappt:**

1. Baut sie in kleinen Schritten auf: erst `SELECT * FROM tabelle LIMIT 5`, dann Spalten, dann `WHERE`, dann `GROUP BY`.
2. Prüft Zwischenergebnisse: Stimmt die Zeilenzahl nach dem `JOIN`?
3. Prüft, welche Spalten und Werte es wirklich gibt: `SELECT DISTINCT weather FROM trips;`
4. Lest die Aufgabe noch einmal: Reihenfolge der Spalten, Sortierung, Rundung, Namen der Ergebnisspalten.

---

## 8. Spickzettel auf einer Seite

```sql
-- Grundgerüst
SELECT   [DISTINCT] spalte, ausdruck AS alias
FROM     tabelle AS t
[LEFT] JOIN andere AS a ON t.fremd_id = a.id
WHERE    bedingung                    -- Zeilen filtern
GROUP BY spalte                       -- Gruppen bilden
HAVING   aggregat_bedingung           -- Gruppen filtern
ORDER BY spalte [ASC|DESC], spalte2   -- sortieren
LIMIT    n [OFFSET m];                -- begrenzen
```

| Ich will …                       | Dann nutze ich …                                   |
| -------------------------------- | -------------------------------------------------- |
| alle Spalten                     | `SELECT *`                                         |
| Duplikate entfernen              | `SELECT DISTINCT`                                  |
| Spalte umbenennen                | `spalte AS name`                                   |
| nur die ersten n Zeilen          | `LIMIT n`                                          |
| Zeilen überspringen              | `LIMIT n OFFSET m`                                 |
| nach Bedingung filtern           | `WHERE`                                            |
| mehrere Bedingungen              | `AND`, `OR`, `NOT`, Klammern                       |
| Wert in Liste                    | `IN (a, b, c)`                                     |
| Wert in Bereich                  | `BETWEEN a AND b`                                  |
| Textmuster                       | `LIKE 'x%'`, `'%x%'`, `'_x'`                       |
| fehlenden Wert prüfen            | `IS NULL`, `IS NOT NULL`                           |
| sortieren                        | `ORDER BY spalte DESC`                             |
| zählen                           | `COUNT(*)`, `COUNT(DISTINCT spalte)`               |
| summieren, mitteln               | `SUM`, `AVG`, `ROUND(…, n)`                        |
| kleinster / größter Wert         | `MIN`, `MAX`                                       |
| pro Wert einer Spalte rechnen    | `GROUP BY spalte`                                  |
| Gruppen nach Ergebnis filtern    | `HAVING COUNT(*) > n`                              |
| Wenn-dann-Spalte                 | `CASE WHEN … THEN … ELSE … END`                    |
| Stunde aus Zeitstempel           | `strftime('%H', spalte)` oder `substr(spalte, 12, 2)` |
| Text zu Zahl                     | `CAST(x AS INTEGER)`                               |
| Wert aus anderer Abfrage         | Subquery `(SELECT …)` mit `=` oder `IN`            |
| Tabellen verknüpfen              | `JOIN … ON fremdschlüssel = primärschlüssel`       |
| auch Zeilen ohne Partner         | `LEFT JOIN`                                        |
| Zeilen ohne Partner finden       | `LEFT JOIN … WHERE rechte.spalte IS NULL`          |
| Gruppen mit 0 mitzählen          | `LEFT JOIN` und `COUNT(rechte.spalte)`             |

**Merksätze**

- `WHERE` = Zeilen vorher, `HAVING` = Gruppen nachher.
- `SELECT`-Spalten ohne Aggregat müssen im `GROUP BY` stehen.
- `JOIN` über Fremdschlüssel = Primärschlüssel, Spalten mit `alias.spalte` qualifizieren.
- Eine Subquery mit `=` liefert genau einen Wert, mit `IN` eine Liste.
- `COUNT(*)` zählt Zeilen, `COUNT(spalte)` zählt Nicht-`NULL`-Werte.
