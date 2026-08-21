# voranalyse-datensatz

Datengrundlage für die KI-Voranalyse von Handwerks-Serviceanfragen.
Gerätetyp: Gas-Brennwerttherme.

**Stand 22.08.2026: 8 Fälle, 52 Codes, 17 Sprachbrücken-Einträge.** Der
Zielumfang (120–250 Fälle) ist deutlich verfehlt – warum und was daraus folgt,
steht in `report.md`. Nichts ist mit Plausiblem aufgefüllt.

Zwei Punkte vor der Weiterverwendung:
- Die **TDM-Prüfung nach §44b UrhG ist nicht erfolgt** (siehe `quellenlog.md`).
  Der Bestand ist eine Voruntersuchung, nicht produktiv verwendbar.
- Der **Eval-Split ist bewusst nicht gezogen** (siehe `split_log.md`); bei 5
  bestätigten Fällen ergäbe er ein Testset von einem Fall.

## Aufbau

```
fehlercode_taxonomie.json   Skelett: Codes + Symptomklassen
faelle.jsonl                Wissensbasis (ein Fall pro Zeile)
eval_set.jsonl              Testset, aus der Wissensbasis entfernt
sprachbruecke.json          Laienausdruck -> Symptomklasse
quellenlog.md               Quelle, Datum, TDM-Status, Ausbeute
report.md                   Abschlussbericht
schema/fall.schema.json     Feldsatz, exakt nach Auftrag
scripts/validate.py         prüft Schema + harte Regeln
scripts/split_eval.py       zieht den Eval-Split (Schritt 6)
```

## Ablauf

```bash
# nach jedem Sammelabschnitt, nicht erst am Ende (Regel 7)
python3 scripts/validate.py

# erst wenn die Sammlung steht - genau einmal
python3 scripts/split_eval.py --dry-run
python3 scripts/split_eval.py --seed 42
```

`validate.py` endet mit Exit-Code 1, sobald ein Fehler vorliegt – damit lässt
es sich als Pre-Commit-Hook oder CI-Schritt einhängen. Warnungen brechen nicht
ab, sie markieren Stellen zum Nachschauen.

## Was der Validator durchsetzt

| Regel | Prüfung |
|---|---|
| 1 – nichts erfinden | Pflichtfelder, keine `code_offizielle_bedeutung` ohne `fehlercode` |
| 2 – kein Originaltext | Warnung bei überlangem `symptom_laie` |
| 3 – kein Personenbezug | E-Mail, Telefonnummer, `@handle`, Profil-URLs |
| 4 – keine Häufigkeiten | `additionalProperties: false` blockt neue Felder; Textprüfung auf „meistens", „häufigste", „x % der Fälle" |
| 5 – Eval getrennt | Überschneidung von `fall_id` und `quelle_url` zwischen beiden Dateien |
| 6 – Gas/Strom | `fachkraft_erforderlich` erzwungen, jeder Diagnoseschritt braucht Präfix `[Fachkraft]` |

## Konvention für Diagnoseschritte

Bei `gefahrenkategorie` `gas` oder `strom` beginnt jeder Schritt mit
`[Fachkraft]` und ist als Hinweis an die Fachkraft formuliert, nicht als
Handlungsanweisung an den Endnutzer:

```
"[Fachkraft] Gasfließdruck am Messnippel prüfen"     ok
"Drehen Sie die Gaszufuhr ab und ..."                 nicht ok
```

Das ist eine Formkonvention – sie kann Regel 6 maschinell erzwingen, aber nicht
beurteilen, ob der Inhalt eines Schritts für Laien gefährlich verwertbar ist.
Diese Prüfung bleibt menschlich.

## Offene Entscheidungen für die Projektleitung

1. **`mehrfach_unabhaengig` ist unterdefiniert.** Foren zitieren sich
   gegenseitig, dieselbe Person postet in mehreren. Ohne Herkunftsprüfung wird
   aus einem Fall drei – und der Grad, der eigentlich der belastbarste sein
   soll, wird der unzuverlässigste. Nötig ist ein Kriterium: zwei Quellen
   gelten erst dann als unabhängig, wenn keine die andere zitiert und die
   Formulierungen sich nicht überschneiden. Solange das nicht definiert ist,
   nur `bestaetigt` und `vermutung` vergeben.
2. **Der Eval-Split zieht ausschließlich aus `bestaetigt`.** Das Testset besteht
   damit aus dem saubersten Teil der Daten, während das System produktiv genau
   an den unklaren Fällen scheitern wird. Empfehlung: zusätzlich eine kleine
   Menge `vermutung`-Fälle als Kontrollset – nicht als Ground Truth, sondern um
   zu messen, ob das System dort korrekt „unklar" ausgibt statt zu raten.
3. **Fälle ohne Modellreihe.** Das Schema verlangt sie. Viele Threads nennen nur
   den Hersteller. Entweder solche Fälle verwerfen (aktuelle Einstellung) oder
   das Feld nullable machen – das ist eine Produktentscheidung, keine
   Datenentscheidung, und gehört nicht still in der Sammlung getroffen.
