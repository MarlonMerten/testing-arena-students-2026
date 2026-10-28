# TEST_PLAN.md

## 1. parse_time(time_text)
- Standard: "14:21" -> 861
- Grenzen: "00:00" -> 0 und "23:59" -> 1439
- Format: "9:5" und "09:05" (ohne Null / mit Null)
- Fehler (ValueError): "24:00", "12:60", "abc", "14:21:00", ""

## 2. parse_measurement(line)
- Standard: "Köln;14:21;21.7"
- Leerzeichen: " Köln ; 14:21 ; 21.7 "
- Fehler (ValueError): Kein String, nicht 3 Felder, Stadt leer (" ;14:21;20"), Temp kein Float ("Köln;14:21;heiß")

## 3. filter_by_temperature(measurements, lower, upper)
- Normales Filtern von Werten
- Grenzen: Werte genau auf lower/upper, lower == upper
- Duplikate bleiben drin
- Fehler (ValueError): lower > upper
- Seiteneffekt: Original-Liste wird nicht verändert, neue Liste entsteht

## 4. average_temperature(measurements, city)
- Durchschnitt richtig berechnen
- Gross-/Kleinschreibung: "Köln" vs "köln"
- Fehler (ValueError): Stadt nicht in Liste, leere Liste
- Seiteneffekt: Original-Liste bleibt gleich

## 5. hottest_measurement(measurements)
- Eindeutig höchste Temp finden
- Gleichstand 1: Gleiche Temp -> frühere Zeit gewinnt
- Gleichstand 2: Gleiche Temp + Zeit -> der erste Eintrag gewinnt
- Fehler (ValueError): Leere Liste
- Seiteneffekt: Original-Liste bleibt gleich