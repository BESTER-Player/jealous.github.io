# Datensätze zum Auftrag — Direct Handwork

Datensammlung rund um den **Handwerksauftrag** für Direct Handwork: Datenmodell,
Referenzlisten und ein vollständiger, in sich konsistenter Beispielbestand in
JSON, CSV und SQL.

Das Repository enthielt zuvor ein unabhängiges Tkinter-Finanzrechner-Skript. Dieser
Bestand wurde vollständig entfernt und durch die hier beschriebenen Datensätze ersetzt.

---

## Inhalt

```
datensaetze/
├── json/          Quelle der Wahrheit — hier wird gepflegt
│   ├── auftraege.json      12 Aufträge inkl. eingebetteter Positionen
│   ├── positionen.json     62 Positionen, normalisiert (eine Zeile je Position)
│   ├── kunden.json         10 Auftraggeber (privat und gewerblich)
│   └── handwerker.json      8 angeschlossene Handwerksbetriebe
├── csv/           Erzeugt aus json/ — Semikolon als Trennzeichen, UTF-8
├── sql/
│   ├── schema.sql          Tabellen, Constraints, Indizes, zwei Auswertungs-Views
│   └── seed.sql            Erzeugt aus json/ — 92 INSERT-Anweisungen
├── schema/        JSON-Schema (Draft 2020-12) je Entität
└── referenz/      Wertelisten: Gewerke, Auftragsstatus, Mengeneinheiten

tools/
├── build.py       json/ → csv/ und sql/seed.sql
└── validate.py    prüft Schema, Referenzen, Summen, Status- und Datumslogik
```

## Datenmodell

```
kunde  1 ──── n  auftrag  n ──── 1  handwerker
                    │
                    │ 1
                    n
             auftragsposition
```

| Entität | Schlüssel | Beschreibung |
|---|---|---|
| `kunde` | `K-1001` | Auftraggeber, privat oder gewerblich. Gewerbliche Kunden benötigen eine Firma. |
| `handwerker` | `H-201` | Ausführender Betrieb mit einem oder mehreren Gewerken, Einsatzradius und Stundensatz. |
| `auftrag` | `A-2026-0001` | Der Auftrag selbst: Format `A-JJJJ-NNNN`, laufende Nummer je Kalenderjahr. |
| `auftragsposition` | `A-2026-0001-010` | Einzelposition, Schlüssel aus Auftrag und Positionsnummer. |

### Wichtige Felder des Auftrags

| Feld | Bedeutung |
|---|---|
| `gewerk` | Einer von zehn Codes aus `referenz/gewerke.json`, z. B. `sanitaer`, `elektro`. |
| `objekt` | Einsatzort mit Straße, PLZ, Ort, Etage und Zugangshinweis — kann von der Rechnungsanschrift abweichen. |
| `kanal` | Eingangsweg: `web`, `app`, `telefon`, `email`, `empfehlung`. |
| `prioritaet` | `niedrig`, `normal`, `hoch`, `notfall`. |
| `status` | Siehe Zustandsautomat unten. |
| `handwerker_id` | `null`, solange kein Betrieb zugeordnet ist. Ab Status `beauftragt` Pflicht. |
| `budget_rahmen_eur` | Vom Kunden genannte Obergrenze, unverbindlich. Ein Angebot darf darüber liegen. |
| `positionen` | Positionsliste, jede mit `art` (`lohn`, `material`, `anfahrt`, `fremdleistung`). |
| `angebotssumme_netto_eur` | Summe aller Positionen. Brutto = netto × 1,19 (19 % USt.). |

### Zustandsautomat des Status

```
neu → in_pruefung → angebot_erstellt → beauftragt → in_arbeit → abgeschlossen → abgerechnet
 └────────┴─────────────────┴──────────────┴────────────┴──────→ storniert
```

Die erlaubten Übergänge stehen maschinenlesbar in `datensaetze/referenz/auftragsstatus.json`.
`abgerechnet` und `storniert` sind Endzustände.

## Bestand im Überblick

| Auftrag | Gewerk | Status | Priorität | Netto (EUR) | Brutto (EUR) |
|---|---|---|---|---:|---:|
| A-2026-0001 | Sanitär | abgerechnet | normal | 276,25 | 328,74 |
| A-2026-0002 | Elektro | abgerechnet | normal | 3.237,80 | 3.852,98 |
| A-2026-0003 | Dachdecker | abgerechnet | **notfall** | 1.584,56 | 1.885,63 |
| A-2026-0004 | Fliesen | abgerechnet | normal | 3.186,60 | 3.792,05 |
| A-2026-0005 | Heizung | abgeschlossen | niedrig | 299,40 | 356,29 |
| A-2026-0006 | Maler | in Arbeit | normal | 3.123,80 | 3.717,32 |
| A-2026-0007 | Elektro | beauftragt | hoch | 1.742,38 | 2.073,43 |
| A-2026-0008 | Tischler | Angebot erstellt | normal | 7.245,17 | 8.621,75 |
| A-2026-0009 | Schlosser | in Arbeit | hoch | 1.746,00 | 2.077,74 |
| A-2026-0010 | Sanitär | in Prüfung | normal | — | — |
| A-2026-0011 | Garten | neu | niedrig | — | — |
| A-2026-0012 | Trockenbau | storniert | normal | 1.209,84 | 1.439,71 |

Die Daten decken bewusst auch Randfälle ab, damit sich Auswertungen und
Eingabemasken realistisch testen lassen:

- **Ohne Betrieb:** A-2026-0010 und A-2026-0011 haben `handwerker_id = null`.
- **Ohne Positionen:** dieselben beiden Aufträge haben Summe 0,00 EUR.
- **Über Budget:** A-2026-0008 liegt mit 7.245,17 EUR über dem genannten Rahmen von 6.000 EUR — das Angebot ist deshalb noch nicht beauftragt.
- **Notfall mit Zuschlägen:** A-2026-0003 enthält Notdienstzuschlag, Fremdleistung (Gerüst) und kilometergenaue Anfahrt.
- **Storniert:** A-2026-0012 trägt Stornodatum und Stornogrund, die Positionen bleiben zur Nachvollziehbarkeit erhalten.
- **Inaktiver Partnerbetrieb:** H-208 ist auf `aktiv = false` gesetzt, weshalb A-2026-0011 noch keine Zuordnung hat.

## Verwendung

**Datenbank aufbauen** (SQLite):

```bash
sqlite3 direct_handwork.db < datensaetze/sql/schema.sql
sqlite3 direct_handwork.db < datensaetze/sql/seed.sql
sqlite3 direct_handwork.db "SELECT * FROM v_umsatz_je_gewerk;"
```

`schema.sql` bringt zwei Views mit: `v_offene_auftraege` (alles außer abgerechnet und
storniert, inkl. Kunde und Betrieb) und `v_umsatz_je_gewerk`.

**Exporte neu erzeugen**, nachdem in `datensaetze/json/` etwas geändert wurde:

```bash
python3 tools/build.py      # schreibt csv/ und sql/seed.sql neu
python3 tools/validate.py   # prüft den gesamten Bestand
```

`validate.py` liefert Rückgabewert 0 bei fehlerfreiem Bestand und 1, sobald ein
Fehler gefunden wurde — damit lässt es sich direkt in eine CI-Prüfung hängen. Ist
das Paket `jsonschema` installiert, werden zusätzlich alle Datensätze gegen die
Schemas unter `datensaetze/schema/` validiert.

Geprüft werden unter anderem: eindeutige Schlüssel, referenzielle Integrität,
ob der zugeordnete Betrieb das geforderte Gewerk überhaupt anbietet, die
Rechenlogik aller Summen einschließlich Mehrwertsteuer, die Status- und
Datumslogik sowie die Aktualität der CSV-Exporte.

## Konventionen

- **Zeichensatz:** durchgängig UTF-8, deutsche Umlaute unverändert.
- **CSV:** Semikolon als Trennzeichen, Punkt als Dezimaltrennzeichen, Wahrheitswerte als `1`/`0`, leere Felder als leerer String.
- **Datumsangaben:** ISO 8601. Reine Daten als `JJJJ-MM-TT`, Zeitstempel mit Zeitzonenangabe (`2026-01-12T09:14:00+01:00`).
- **Beträge:** Euro, netto, auf zwei Nachkommastellen gerundet. Der Mehrwertsteuersatz steht als `mwst_satz` an jedem Auftrag (aktuell durchgängig 0,19).
- **Änderungen** immer in `datensaetze/json/` vornehmen, danach `tools/build.py` ausführen. Die Dateien unter `csv/` und `sql/seed.sql` sind erzeugt und werden überschrieben.

## Hinweise zu den Daten

Sämtliche Datensätze sind **synthetisch**. Namen, Firmen, Adressen, Telefonnummern,
E-Mail-Adressen und Umsatzsteuer-Identifikationsnummern sind frei erfunden und
beziehen sich nicht auf reale Personen oder Betriebe. Die Daten sind für
Entwicklung, Test und Demonstration gedacht, nicht für den Produktivbetrieb.
