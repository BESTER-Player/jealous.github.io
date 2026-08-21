# Abschlussbericht – Voranalyse-Datensatz Gas-Brennwerttherme

Stand 22.08.2026. Ein Durchlauf, 12 Abrufe (10 Suchen, 2 vollständig gelesene
Threads).

**Zielumfang nicht erreicht.** Vorgabe waren 120–250 destillierte Fälle und
200–500 Fehlercode-Einträge; erreicht wurden **8 Fälle und 52 Codes**. Nach dem
Leitprinzip des Auftrags ist das ein Ergebnis und kein Anlass, aufzufüllen. Was
dieser Durchlauf liefert, ist deshalb weniger ein Datensatz als eine Messung:
er zeigt, woran die Erhebung tatsächlich hängt – und das ist nicht die Menge
verfügbarer Threads.

---

## 1. Ausbeutequote

| Kennzahl | Wert |
|---|---|
| Abrufe (Suchen + Seitenabrufe) | 12 |
| unterscheidbare Diskussionen gesichtet | ca. 27 |
| davon mit erkennbarer Problemschilderung | ca. 21 |
| ins Schema überführt | 8 |
| davon mit Lösungsbestätigung | 5 |
| Ausbeutequote (verwertbar / gesichtet) | **≈ 30 %** |
| bestätigte Fälle / gesichtet | **≈ 19 %** |

Diese Quoten sind nach oben verzerrt, weil gezielt nach Threads mit
Lösungsformulierungen gesucht wurde. Ein ungefilterter Durchlauf würde
niedriger liegen.

### Der wichtigste methodische Befund

Von den 27 Diskussionen wurden nur **2 vollständig gelesen** – beide lieferten
einen bestätigten Fall, eine davon sogar zwei. Die übrigen 25 wurden nur als
Suchauszug bewertet.

Das ist kein Zufall, sondern systematisch: **Suchauszüge brechen vor der
Bestätigung ab.** Im Vitodens-200-Thread zu F5 endete der Auszug bei „ich werde
es der Firma mitteilen" – die eigentliche Erfolgsmeldung kam vier Wochen später
und war im Auszug unsichtbar. Wer den Bestätigungsgrad aus Suchauszügen
ableitet, stuft systematisch zu niedrig ein und verwirft brauchbare Fälle.

Der Engpass ist also **das Lesen ganzer Threads, nicht das Finden von Threads**.
Das hat unmittelbare Folgen für die Planung: Die Erhebung skaliert über
Seitenabrufe, nicht über Suchanfragen.

## 2. Verteilung der Bestätigungsgrade

| Grad | Anzahl | Anteil |
|---|---|---|
| bestaetigt | 5 | 62,5 % |
| mehrfach_unabhaengig | 0 | 0 % |
| vermutung | 3 | 37,5 % |

`mehrfach_unabhaengig` wurde bewusst **nie** vergeben. Die beiden Fälle mit
identischem Leitsymptom (VIE-0002, VIE-0003) stammen aus demselben Thread und
sind damit nicht unabhängig – der zweite ist eine Antwort auf den ersten. Genau
das ist die Falle, vor der das offene Problem im README warnt: Ohne
Herkunftsprüfung wäre hier zweimal „unabhängig bestätigt" entstanden, wo eine
Quelle vorliegt.

## 3. Abdeckungslücken

| Hersteller | Fälle | bestätigt | Codes |
|---|---|---|---|
| Viessmann | 5 | 4 | 6 |
| Buderus | 2 | 1 | 5 |
| Vaillant | 1 | 0 | 15 |
| Junkers/Bosch | **0** | 0 | 15 |
| Wolf | **0** | 0 | 11 |

Die Verteilung bildet ab, wo ein gut strukturiertes Herstellerforum existiert –
nicht, wo Geräte häufig ausfallen. Viessmann dominiert, weil
`community.viessmann.de` Lösungen markiert und Rückmeldungen einfordert. Für
Junkers/Bosch und Wolf wurde in diesem Durchlauf kein einziger auflösbarer Fall
gefunden.

Dünn sind außerdem:
- **Fälle ohne Fehlercode.** Nur einer (VIE-0003). Der Zielnutzer beschreibt aber
  oft gerade keinen Code – das ist die schwächste Stelle des Bestands.
- **Geruchs- und Geräuschsymptome.** Die Sprachbrücke hat dafür Einträge, die
  Fallbasis nicht.
- **Codes ohne belegte Bedeutung.** Fünf Viessmann-Codes stehen mit
  `offizielle_bedeutung: null` – die Bedeutung ist baureihen- und
  reglergenerationsabhängig und war ohne Serviceanleitung nicht belastbar zu
  klären.

## 4. Auffällige Muster: Ursache ≠ offizielle Codebedeutung

**M1 – F.75 wird systematisch falsch gelesen.**
Die Dokumentation sagt: keine Drucksprungerkennung beim Start der Pumpe.
Bewertet wird der Druck*anstieg* von etwa 0,2 bar, nicht der absolute
Anlagendruck. Ratgeberseiten und Betreiber lesen den Code jedoch durchgängig als
„Wasserdruck zu niedrig" und füllen Wasser nach. Zu wenig Wasser wäre F.22. Ein
Voranalyse-System, das hier der verbreiteten Lesart folgt, würde die häufigste
Fehlmaßnahme reproduzieren.

**M2 – Die Codegruppe „kein Flammensignal" ist strukturell unspezifisch.**
In drei bestätigten Fällen zeigte der Code auf den Brenner, die Ursache lag
außerhalb der Brennerbaugruppe: eine defekte Gemischklappe (VIE-0001), eine
zerstörte Brennerdichtung mit Abgasrezirkulation (VIE-0002) und ein festsitzendes
Ventil beim Netzbetreiber, also vollständig außerhalb des Geräts (BUD-0001).
Mehrere Quellen beschreiben Wolf 004 und Viessmann E8 selbst ausdrücklich als
nicht-spezifisch. **Empfehlung: Diese Codegruppe darf im Modell keine
Ursachenhypothese auslösen, sondern nur einen Diagnosepfad.**

**M3 – Der Bauteiltausch folgt der Codebedeutung, nicht dem Leitsymptom.**
In vier von acht Fällen wurden Teile erfolglos getauscht, bevor die Ursache
gefunden war – bei VIE-0002 Zündelektroden und Radialgebläse, dazu der Vorschlag,
Wärmetauscher oder ganzes Gerät zu ersetzen, während die schadhafte Dichtung
laut Betreiber sichtbar war. Bei VIE-0001 blieb die defekte Gemischklappe auch im
direkten Vergleich mit dem Neuteil optisch unauffällig.

Daraus folgt der eigentliche Produktnutzen: Der Wert der Voranalyse liegt nicht
darin, den Code zu übersetzen – das können Tabellen. Er liegt darin, das
**Leitsymptom** aus der Laienschilderung zu ziehen. „Läuft ohne Haube, mit Haube
Störung" grenzt stärker ein als der Code selbst.

## 5. Quellenqualität

- **Herstellerforum (community.viessmann.de)** – klar am besten. Markierte
  Lösungen, Herstellermitarbeiter im Thread, Betreiber melden Ergebnisse zurück.
  Nachteil: sehr große Seiten, hoher Abrufaufwand pro Fall.
- **Fachforum (heizungsforum.de)** – gute technische Tiefe, oft mit Messwerten.
  Aber die Auflösung fehlt häufig oder steht in einem Nebensatz.
- **Ratgeberportale** – für die Codesystematik brauchbar, für Einzelursachen
  nicht. Eine Quelle beschreibt F.28 als Flammenausfall im Betrieb; das ist F.29.
  Solche Fehler wandern beim ungeprüften Übernehmen direkt in die Taxonomie.
- **Ersatzteilhändler und Marktplätze** – reines Rauschen. Ein erheblicher Teil
  der Suchtreffer bestand aus Artikelseiten.
- **Herstellerdokumentation** – qualitativ am besten für Schritt 2, dafür der
  einzige Bereich mit einem ernsten Rechtsrisiko (siehe Quellenlog).

## 6. Empfehlung: Ausweitung auf weitere Gerätetypen?

**Nein, noch nicht.** Der Engpass ist nicht der Gerätetyp, sondern die Erhebung:
gefunden werden Threads reichlich, gelesen werden können sie kaum. Eine
Ausweitung auf Wärmepumpen oder Weiße Ware würde dieses Problem
vervielfachen statt lösen.

Sinnvolle Reihenfolge stattdessen:

1. **TDM-Prüfung nachholen**, pro Quelle, dokumentiert. Ohne das ist der
   Bestand nicht produktiv verwendbar.
2. **Gezielt statt breit erheben.** Die Lösungs-Übersichtsseiten von
   `community.viessmann.de` listen akzeptierte Lösungen direkt – das ist ein
   Einstiegspunkt mit sehr viel höherer Trefferdichte als eine Websuche.
3. **Vollständig lesen, nicht Auszüge bewerten.** Siehe Abschnitt 1.
4. **Erst dann** Junkers/Bosch und Wolf gezielt nachziehen, um die
   Herstellerschieflage zu korrigieren.

Realistische Schätzung auf dieser Basis: ca. 30 % Ausbeute pro vollständig
gelesenem Thread aus einem Herstellerforum. Für 120 bestätigte Fälle sind damit
grob 400–600 gelesene Threads anzusetzen.

---

## Getroffene Entscheidungen (Regel 8)

| Entscheidung | Konservative Wahl | Begründung |
|---|---|---|
| Eval-Split | **nicht gezogen** | Bei 5 bestätigten Fällen ergäbe der 20-%-Split ein Testset von einem Fall. Das misst nichts und entzieht der Wissensbasis 20 % ihres belastbaren Teils. Der Split ist als Dry-Run gerechnet und in `split_log.md` dokumentiert; er wird nachgeholt, sobald der Bestand trägt. |
| `mehrfach_unabhaengig` | nie vergeben | Kriterium für Unabhängigkeit ist nicht definiert; zwei Fälle stammen aus demselben Thread. |
| Fehlercode-Taxonomie | nur Teilbestand, keine vollständigen Herstellertabellen | Datenbankschutz §87a ff. UrhG |
| Nicht belegbare Codebedeutungen | `null` statt plausibler Formulierung | Regel 1 |
| Gasströmungswächter-Manipulation | vollständig ausgeschlossen | Sicherheitsrelevante Manipulation an einer Schutzeinrichtung, siehe Quellenlog |
| Quellendatum | `null`, wo nur der Suchindex ein Datum lieferte | Regel 1 – Indexdatum ist nicht Beitragsdatum |
| Diagnoseschritte | durchgängig mit `[Fachkraft]` präfigiert, auch außerhalb von Gas und Strom | Regel 6, einheitlich statt selektiv |
