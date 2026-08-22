# voranalyse-datensatz

Datengrundlage für die KI-Voranalyse von Handwerks-Serviceanfragen.
Gerätetyp: Gas-Brennwerttherme.

**Stand 22.08.2026, dritter Durchlauf: 150 Fälle, 74 Codes, 38 Symptomklassen,
40 Sprachbrücken-Einträge.**

Der Zielkorridor für die Fälle (120–250) ist erreicht, der für die
Fehlercode-Einträge (200–500) nicht. Der Sammellauf brach nach 12 von 30
Suchzellen ab, weil das WebSearch-Kontingent der Session erschöpft war –
**Junkers/Bosch und Wolf haben deshalb weiterhin null Fälle** bei 26 erfassten
Codes. Einzelheiten in `report.md`, Abschnitt 9.

Vorgeschichte: Durchlauf 1 sammelte 8 Fälle; Durchlauf 2 prüfte den Bestand
(15 Agenten, 36 Befunde in `audit_befunde.md`, 10 umgesetzt).

Drei Punkte vor der Weiterverwendung:
- Die **TDM-Prüfung nach §44b UrhG ist nicht erfolgt und in dieser Umgebung auch
  nicht durchführbar** (siehe `quellenlog.md`): der Egress-Proxy blockiert jeden
  direkten Seitenabruf. Der Bestand ist eine Voruntersuchung, nicht produktiv
  verwendbar.
- Der Grad **`bestaetigt` ist ohne Seitenabruf nicht vergebbar**, weil die
  Lösungsbestätigung am Threadende steht und der Suchauszug davor abbricht.
  **Alle 142 im dritten Durchlauf ergänzten Fälle tragen deshalb `vermutung`.**
  Der Anteil belastbarer Fälle liegt bei 2 % (3 von 150) – in absoluten Zahlen
  unverändert gegenüber dem Stand vor dem Sammellauf.
- Der **Eval-Split ist weiterhin nicht gezogen** (siehe `split_log.md`); nach den
  Herabstufungen des zweiten Durchlaufs stehen noch 3 bestätigte Fälle.

## Aufbau

```
fehlercode_taxonomie.json   Skelett: Codes + Symptomklassen (mit Achsentrennung)
faelle.jsonl                Wissensbasis (ein Fall pro Zeile)
eval_set.jsonl              Testset, aus der Wissensbasis entfernt
sprachbruecke.json          Laienausdruck -> Symptomklasse
quellenlog.md               Quelle, Datum, TDM-Status, Ausbeute
report.md                   Abschlussbericht (Abschnitt 8 = zweiter Durchlauf)
audit_befunde.md            36 Befunde des Audits, einzeln mit Beleg
schema/fall.schema.json     Feldsatz, exakt nach Auftrag
scripts/validate.py         prüft Schema, harte Regeln und Querverweise
scripts/split_eval.py       zieht den Eval-Split (Schritt 6)
scripts/migration_2026-08-22.py  setzt die umgesetzten Auditbefunde um
```

## Symptomklassen: die Achsentrennung

Die 20 Klassen in `fehlercode_taxonomie.json` liegen **nicht alle auf derselben
Ebene**. Das Feld `achse` trennt sie:

| Achse | Bedeutung | Ziel einer Laieneingabe? |
|---|---|---|
| `leitsymptom` | Beobachtbares Symptom | ja |
| `fallmerkmal` | Merkmal des Fallverlaufs | nein |
| `kontextmarker` | Nicht-technischer Hinweis | nein |
| `eingabenormalisierung` | Form der Nutzereingabe | nein |
| `befundsprache` | Befund nach dem Öffnen, Fachkraftseite | nein |

Ein Eintrag in `sprachbruecke.json` trägt in `ziel_art` die Achse seiner
Zielklasse und **erbt** deren `gefahrenkategorie` – sie wird dort nicht gepflegt.
Der Validator erzwingt beides. Eine Klasse mit `status: abgeloest` ist historisch
und muss über `nachfolger` auf ihren Ersatz zeigen.

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
| Verankerung | Jeder Fall hängt an einem Code- oder Symptomknoten (Auftrag Schritt 2); tote Verweise in beide Richtungen |
| Achsentreue | `ziel_art` spiegelt die Achse der Zielklasse; `gefahrenkategorie` wird geerbt, eine Abweichung könnte das Regel-6-Gatter unterlaufen |
| Unabhängigkeit | Mehrfachnutzung derselben Quelle wird gemeldet; `mehrfach_unabhaengig` bei geteilter Quelle ist ein **Fehler** |
| Teilesemantik | `benoetigte_teile` befüllt, während die Ursache eine Nichtauflösung ausdrückt |

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

0. **Beleglage der drei stärksten Fälle ist ungeklärt.** Der Report nennt zwei
   vollständig gelesene Threads, der Quellenlog verzeichnet jeden Seitenabruf als
   blockiert. Davon hängt ab, ob überhaupt ein Fall `bestaetigt` verdient
   (Befund 6). Vor dieser Klärung ist keine Aussage über die Qualität des
   Bestands belastbar.
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

4. **Das Kriterium für `bestaetigt` steht nirgends.** Fünf Fälle trugen im
   Unsicherheitenfeld denselben Vorbehalt – nur der Suchauszug ausgewertet – und
   erhielten trotzdem unterschiedliche Grade. Solange das Kriterium nicht hier
   festgeschrieben ist, ist jede darauf aufbauende Kennzahl entwertet, auch der
   Eval-Split. Die vollständige Liste offener Punkte steht in `report.md`,
   Abschnitt 8.6.
