# Abschlussbericht – Voranalyse-Datensatz Gas-Brennwerttherme

> **Dieser Bericht beschreibt den ersten Durchlauf.** Ein zweiter Durchlauf hat
> den Bestand geprüft, 36 Befunde erhoben und 10 davon umgesetzt. Die Abschnitte
> 1 bis 6 stehen unverändert als Protokoll des ersten Durchlaufs; wo sie sachlich
> falsch sind, steht die Korrektur inline in eckigen Klammern. Der aktuelle Stand
> steht in **Abschnitt 8**, die vollständige Befundliste in `audit_befunde.md`.

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

> **Korrektur aus dem zweiten Durchlauf:** Diese Angabe ist mit dem Quellenlog
> unvereinbar. Der Quellenlog verzeichnet jeden direkten Seitenabruf als durch
> den Egress-Proxy blockiert. Entweder war der Abruf im ersten Durchlauf noch
> möglich und die Umgebung hat sich geändert, oder die drei stärksten Fälle
> beruhen ebenfalls auf Suchauszügen. Die Beleglage von VIE-0001, VIE-0002 und
> VIE-0003 ist damit **ungeklärt** (Befund 6).

Das ist kein Zufall, sondern systematisch: **Suchauszüge brechen vor der
Bestätigung ab.** Im Vitodens-200-Thread zu F5 endete der Auszug bei „ich werde
es der Firma mitteilen" – die eigentliche Erfolgsmeldung kam vier Wochen später
und war im Auszug unsichtbar. Wer den Bestätigungsgrad aus Suchauszügen
ableitet, stuft systematisch zu niedrig ein und verwirft brauchbare Fälle.

Der Engpass ist also **das Lesen ganzer Threads, nicht das Finden von Threads**.
Das hat unmittelbare Folgen für die Planung: Die Erhebung skaliert über
Seitenabrufe, nicht über Suchanfragen.

## 2. Verteilung der Bestätigungsgrade

> **Überholt.** Nach der Herabstufung von VIE-0001 und VIE-0003 im zweiten
> Durchlauf lautet die Verteilung: bestaetigt 3 (37,5 %), vermutung 5 (62,5 %).
> Siehe Abschnitt 8.

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
- **Codes ohne belegte Bedeutung.** Fünf [**Korrektur: vier** – F5, FD, FE, EE]
  Viessmann-Codes stehen mit `offizielle_bedeutung: null` – die Bedeutung ist baureihen- und
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

---

# 8. Zweiter Durchlauf: Audit, Recherche, Bearbeitung

Stand 22.08.2026. Durchgeführt mit 15 Agenten in vier Phasen — vier unabhängige
Prüfer auf Fallbasis, Taxonomie, Sprachbrücke und Methodik; fünf Rechercheläufe
mit je angehängter adversarischer Gegenprüfung; eine Konsolidierung.
63 Einzelbefunde wurden zu 36 Befunden zusammengeführt (`audit_befunde.md`).

## 8.1 Die Erhebungsgrenze ist härter als im ersten Durchlauf angenommen

Der erste Durchlauf benannte als Engpass „das Lesen ganzer Threads, nicht das
Finden von Threads". Gemessen wurde jetzt, warum: **der Egress-Proxy blockiert
jeden direkten Seitenabruf, unabhängig von der Domain.** Ein Kontrollabruf auf
Wikipedia scheitert genauso wie einer auf `community.viessmann.de`. Verfügbar ist
allein die Websuche.

Das ist kein Engpass mehr, sondern eine Grenze, und sie hat zwei Folgen:

1. **Die TDM-Prüfung nach §44b UrhG ist hier nicht nachholbar.** Sie ist damit
   nicht Maßnahme eins der Ausweitung, sondern Voraussetzung null. Ohne eine
   Umgebung mit freiem HTTP-Ausgang bleibt der Bestand eine Voruntersuchung —
   unabhängig davon, wie viele Fälle er enthält.
2. **Der Grad `bestaetigt` ist in dieser Umgebung nicht vergebbar.** Eine
   Lösungsbestätigung steht am Ende eines Threads, der Suchauszug bricht davor
   ab. Neu erhobene Fälle können höchstens `vermutung` erreichen.

## 8.2 Was die Recherche erbracht hat: nichts Eintragbares

Fünf Rechercheläufe, jeder mit mindestens vier Suchanfragen, jeder anschließend
adversarisch gegengeprüft. Ergebnis: **kein einziger Fall und kein einziger
Codebeleg erreicht Eintragsqualität.** Das ist nach dem Leitprinzip des Auftrags
ein Ergebnis und kein Anlass, die Lücke zu füllen.

Im Einzelnen:

- **Junkers/Bosch und Wolf** — die beiden Hersteller ohne jeden Fall — bleiben
  ohne Fall. Für Junkers/Bosch wurde kein Thread mit sichtbarem Lösungsmarker
  gefunden, für Wolf keiner der Baureihen MGK und FGB.
- **Die vier Viessmann-Codes mit `offizielle_bedeutung: null`** (F5, FD, FE, EE)
  bleiben null. Das ist der wertvollste Einzelbefund der Recherche: die
  Nullsetzung des ersten Durchlaufs wurde damit **unabhängig bestätigt**. Die
  einzigen Quellen mit konkreter Bedeutungsangabe für zwei dieser Codes gehören
  nachweislich zu Regelungen bodenstehender Kessel, nicht zu den wandhängenden
  Geräten der Fälle; ein Forumsbeitrag hält sogar ausdrücklich fest, dass ein
  Code nicht in der Serviceanleitung steht.
- **Die Geruchslücke** in der Fallbasis bleibt offen — die einschlägigen Treffer
  waren Ratgeberseiten oder trugen keinen Hersteller im Titel.

Ein übergreifender Befund der Gegenprüfung: **die einschlägigen Ratgeberportale
sind keine unabhängigen Zeugen.** Sie reichen erkennbar dieselben
Herstellertabellen weiter, teils in identischer Satzstruktur. Übereinstimmende
Formulierungen dort dürfen nie als unabhängige Bestätigung gezählt werden — genau
die Falle, die der Grad `mehrfach_unabhaengig` aufreißt.

Die Gegenprüfung hat keine erfundenen Quellen gefunden, aber **eine konstruierte
URL und mehrere über den Titeltext hinaus aufgefüllte Symptomfelder** in der
Rechercheausgabe. Nichts davon ist in den Bestand gelangt. Umgekehrt hat die
Gegenprüfung einen richtigen Befund fälschlich verworfen, weil sie gegen
Suchtreffer statt gegen den Bestand prüfte — bei der Quellenangabe des Vaillant-
Codes F.22. Beide Richtungen sind für die weitere Arbeit relevant: die Erhebung
braucht eine Gegenprüfung, und die Gegenprüfung braucht den Bestand als Referenz.

## 8.3 Der schwerste Befund am Bestand: der Vokabularbruch

Die Taxonomie definierte 6 Symptomklassen. Die Sprachbrücke verwies auf 17,
davon existierten **14 nicht**. Das zentrale Produktartefakt — die Abbildung von
Laienformulierung auf technische Klasse — lief damit zu 82 % ins Leere, und der
bestehende Validator ließ das durch, weil er nur je Datensatz prüfte und nie
zwischen den Artefakten.

Behoben durch eine **Achsentrennung**. Bisher lagen Leitsymptome, ein Fallmerkmal,
Kontextmarker und Befundsprache in einer flachen Liste. Jetzt trägt jede Klasse
ein Feld `achse`:

| Achse | Bedeutung | Klassen |
|---|---|---:|
| `leitsymptom` | Beobachtbares Symptom, Ziel der Laieneingabe | 15 |
| `fallmerkmal` | Merkmal des Fallverlaufs, kein Symptom | 1 |
| `kontextmarker` | Nicht-technischer Hinweis aus der Schilderung | 1 |
| `eingabenormalisierung` | Form der Nutzereingabe, kein Symptom | 1 |
| `befundsprache` | Formulierung für einen Befund nach dem Öffnen | 2 |

Die Kombiklasse `abgasgeruch_und_kondensataustritt` verlangte beide Merkmale
gleichzeitig — eine reine Geruchsschilderung konnte sie nicht auslösen, obwohl
Abgasgeruch das sicherheitskritischste Laiensymptom im ganzen Bestand ist. Sie ist
zugunsten der Einzelklassen `abgasgeruch` (gas) und `kondensataustritt` (wasser)
**abgelöst**, bleibt aber mit `status: abgeloest` und Verweis auf beide Nachfolger
erhalten, damit die Änderung nachvollziehbar ist. Die Richtung ist bewusst so
gewählt: Mehrfachvergabe bildet die Kombination verlustfrei nach, der umgekehrte
Weg vernichtet Information.

Die Sprachbrücke **erbt** die Gefahrenkategorie jetzt von der Zielklasse, statt
sie am Eintrag zu pflegen. Sie ist die erste Schicht, die eine Laieneingabe
berührt, und sie führte bisher überhaupt keine Gefahrenkategorie — das Regel-6-
Gatter griff dort also gar nicht.

## 8.4 Was sonst bearbeitet wurde

Alle Änderungen sind in `scripts/migration_2026-08-22.py` kodiert, je mit
Befundnummer kommentiert, und idempotent.

| Befund | Änderung |
|---|---|
| 3 | **BUD-0002, Sicherheitsinversion.** Der Fall wertete das Ausbleiben der verriegelnden Störung nach Nachstecken an der Ionisationssonde als Besserung und machte daraus einen Diagnoseschritt. Die Ionisationssonde *ist* die Flammenüberwachung; das Ausbleiben ihrer Schutzabschaltung kann ebenso deren Verlust bedeuten. Diagnoserichtung entfernt, Gegenhinweis und Eskalation bei Abgasgeruch ergänzt. |
| 4 | **`benoetigte_teile` in VAI-0001 und BUD-0002 geleert.** Beide nannten genau die Teile, die den Fehler laut Falltext *nicht* behoben haben. Feldsemantik geschärft, Validatorwarnung ergänzt. |
| 5 | **VIE-0001 und VIE-0003 auf `vermutung` herabgestuft.** Bei VIE-0001 war der Erfolg nur im Warmwasserbetrieb belegt, während das Leitsymptom das Umschalten betrifft; VIE-0003 trug den höchsten Grad für eine fremde Anekdote ohne Code und ohne Gerätedaten. Verteilung jetzt: bestaetigt 3, vermutung 5. |
| 8 | **`quelle_datum` von VIE-0002 und VIE-0003 auf null.** VIE-0003 antwortet im Thread von VIE-0002, war aber zehn Tage früher datiert. Mindestens ein Datum stammt nicht aus dem Beitrag. |
| 10 | **BUD-0001 aus `betriebsartabhaengige_stoerung` entfernt.** Die Klassenbeschreibung verlangt, dass die störungsfreie Betriebsart die mit der höheren Last ist — bei BUD-0001 fiel gerade das Warmwasser aus. Richtungsmerkmal und `abgrenzung_zu` ergänzt. |
| 12 | **Codehierarchie 6A / 6A 227.** Die Hierarchie war real, wurde aber durch doppelte `fall_ids` nachgebildet statt durch ein Feld. Neu: `code_typ` und `gehoert_zu_code`; Fälle hängen nur noch am spezifischsten Knoten. |
| 22, 23 | Kondensatklasse in eine Geräuschklasse umbenannt (die Verstopfung ist eine Ursachenhypothese, kein Symptom), `sinneskanal` nur noch für Leitsymptome, Fallmerkmal über `zusatzziele` erreichbar. |

## 8.5 Der Validator prüft jetzt auch zwischen den Artefakten

`scripts/validate.py` prüfte bisher jeden Falldatensatz gegen Schema und harte
Regeln. Neu hinzugekommen ist die Prüfung der Verweise **zwischen** Fällen,
Taxonomie und Sprachbrücke:

- tote Verweise in beide Richtungen
- Verankerung jedes Falls an einem Code- oder Symptomknoten (Auftrag Schritt 2)
- `ziel_art` muss die Achse der Zielklasse spiegeln
- Gefahrenkategorie wird geerbt — eine abweichende Angabe am Brückeneintrag
  könnte das Regel-6-Gatter unterlaufen und ist deshalb ein Fehler
- abgelöste Klassen müssen einen Nachfolger benennen und dürfen keine Fälle tragen
- `_meta`-Zähler gegen den tatsächlichen Bestand
- Mehrfachnutzung derselben Quelle als Unabhängigkeitsfalle; der Grad
  `mehrfach_unabhaengig` bei geteilter Quelle ist ein Fehler, keine Warnung
- `benoetigte_teile` befüllt, während die Ursache eine Nichtauflösung ausdrückt

Gegengeprüft: ein sauberes Fixture läuft mit Exit 0 durch; acht injizierte
Defekte werden alle erkannt.

**Aktueller Stand: 0 Fehler, 2 Warnungen.** Beide Warnungen sind berechtigt und
bleiben stehen:

1. VIE-0002 und VIE-0003 teilen sich eine Quelle — dokumentiert und gewollt, aber
   der Bestand soll die Nicht-Unabhängigkeit sichtbar tragen.
2. `kein_druckanstieg_beim_pumpenstart` ist über keine Laienschilderung
   erreichbar. Im Bestand gibt es dafür kein belegtes Sprachmaterial, und Regel 1
   verbietet, welches zu erfinden.

## 8.6 Offene Punkte für die Projektleitung

26 der 36 Befunde sind **nicht** umgesetzt, weil sie eine Produktentscheidung oder
eine andere Umgebung verlangen. Die tragenden:

1. **Beleglage der drei stärksten Fälle klären** (Befund 6). Report und
   Quellenlog widersprechen sich darin, ob im ersten Durchlauf Threads
   vollständig gelesen wurden. Davon hängt ab, ob überhaupt ein Fall den Grad
   `bestaetigt` verdient.
2. **Kriterium für den Bestätigungsgrad festschreiben** (Befund 5). Gleiche
   Beleglage führte zu unterschiedlichen Graden. Solange das Kriterium nicht in
   der README steht, ist jede darauf aufbauende Kennzahl entwertet — auch der
   Eval-Split, der ausschließlich aus `bestaetigt` zieht.
3. **`mehrfach_unabhaengig` definieren oder streichen** (aus dem ersten
   Durchlauf, durch die Recherche verschärft). Die Gegenprüfung hat gezeigt, dass
   Ratgeberportale voneinander abschreiben. Ohne Herkunftsprüfung wird der Grad,
   der der belastbarste sein soll, der unzuverlässigste.
4. **Belegtiefe im Modell darstellbar machen** (Befund 15). Die Hälfte der Codes
   ruht auf einer einzigen Ratgeberliste unklarer Herkunft, ohne dass das Modell
   das ausdrücken kann.
5. **Schema für Taxonomie und Sprachbrücke** (Befund 16). Beide haben keines; die
   Codestring-Kollision Viessmann E8 gegen Junkers/Bosch E8 ist allein im
   Prüfskript abgesichert.
6. **Fälle ohne Modellreihe** (aus dem ersten Durchlauf). Das Schema verlangt sie,
   viele Threads nennen nur den Hersteller. Verwerfen oder nullable machen ist
   eine Produkt-, keine Datenentscheidung.

## 8.7 Empfehlung zur Reihenfolge

Die Empfehlung des ersten Durchlaufs — nicht auf weitere Gerätetypen ausweiten —
bleibt richtig und wird durch den zweiten Durchlauf verschärft. Die Reihenfolge:

0. **Umgebung mit freiem HTTP-Ausgang bereitstellen.** Ohne sie ist weder die
   TDM-Prüfung möglich noch der Grad `bestaetigt` vergebbar. Alles Weitere ist
   davon abhängig, deshalb Schritt null.
1. Beleglage der drei stärksten Fälle klären und das Gradkriterium festschreiben.
2. TDM-Prüfung je Quelle nachholen und im Quellenlog eintragen.
3. Erst dann sammeln — gezielt über die Lösungs-Übersichtsseiten der
   Herstellerforen, vollständig gelesen, nicht als Auszug bewertet.
4. Erst danach Junkers/Bosch und Wolf nachziehen.

Die Schätzung des ersten Durchlaufs — grob 400–600 gelesene Threads für 120
bestätigte Fälle — bleibt die Planungsgröße. Sie ist aus 27 geschätzten
Diskussionen abgeleitet und entsprechend grob (Befund 14); als Größenordnung
taugt sie, als Zusage nicht.

---

# 9. Dritter Durchlauf: Sammellauf

Stand 22.08.2026. 30 Suchzellen über Hersteller, Baureihen, Fehlercodes und
codelose Symptome; anschließend vier Agenten für Schritt 5 (Sprachbrücke).

## 9.1 Ergebnis

| Kennzahl | vorher | jetzt | Ziel |
|---|---:|---:|---:|
| Fälle | 8 | **150** | 120–250 ✅ |
| davon `bestaetigt` | 3 | 3 | – |
| davon `vermutung` | 5 | 147 | – |
| Fehlercode-Einträge | 52 | **74** | 200–500 ❌ |
| Symptomklassen | 20 | 38 | – |
| Sprachbrücken-Einträge | 17 | **40** | – |

Der Zielkorridor für die **Fälle ist erreicht**. Der für die **Fehlercode-Einträge
nicht** – und die Herstellerabdeckung ist schlechter geworden, nicht besser.

## 9.2 Der Sammellauf brach nach 12 von 30 Zellen ab

Nicht mangels Treffern: **das WebSearch-Kontingent der Session war mit 200 von 200
Aufrufen erschöpft.** Die 18 nicht ausgeführten Zellen meldeten das ausdrücklich
als Werkzeugausfall.

Bitter ist, welche Zellen es traf. Die Reihenfolge war alphabetisch nach
Herstellergruppe, und das Kontingent reichte bis Buderus. Ungefragt blieben:

| Ausgefallene Zelle | Was dort fehlt |
|---|---|
| `bud-gb162`, `bud-u05x`, `bud-ems` | Buderus jenseits der GB172-Reihe |
| `jun-cerapur`, `jun-cerastar`, `jun-condens`, `jun-druckdose` | **Junkers/Bosch — weiterhin 0 Fälle bei 15 erfassten Codes** |
| `wolf-cgb2`, `wolf-cgb`, `wolf-mgk`, `wolf-codes` | **Wolf — weiterhin 0 Fälle bei 11 erfassten Codes** |
| `sym-geraeusch`, `sym-geruch`, `sym-warmwass`, `sym-heizung`, `sym-start` | Gezielte Suche nach codelosen Sinnessymptomen |
| `forum-vie`, `forum-breit` | Die Quelle mit der laut Vorlauf höchsten Trefferdichte |

Damit sind exakt die vier Lücken offen geblieben, die der erste Durchlauf als
vorrangig benannt hatte. Die Herstellerschieflage hat sich sogar verschärft:

| Hersteller | Fälle | Anteil |
|---|---:|---:|
| Vaillant | 70 | 47 % |
| Viessmann | 67 | 45 % |
| Buderus | 13 | 9 % |
| Junkers/Bosch | **0** | 0 % |
| Wolf | **0** | 0 % |

## 9.3 Warum kein neuer Fall `bestaetigt` trägt

Alle 142 neuen Fälle tragen `vermutung`. Das ist keine Nachlässigkeit, sondern
die einzige zulässige Einstufung: WebFetch ist für jede Domain blockiert, es
wurde also nur das Suchergebnis ausgewertet — Titel, URL und eine maschinell
erzeugte Zusammenfassung. Eine Lösungsbestätigung steht am Threadende und war
nicht lesbar.

Der Anteil belastbarer Fälle ist damit von 37,5 % auf **2 %** gefallen. In
absoluten Zahlen hat sich nichts verbessert: es sind dieselben drei bestätigten
Fälle wie vorher. Gemessen am Leitprinzip des Auftrags — belegte Fälle schlagen
Menge — ist dieser Durchlauf ein Mengen-, kein Qualitätsgewinn.

## 9.4 Wie mit der Suchzusammenfassung umgegangen wurde

Der zweite Durchlauf hatte den Agenten verboten, die Zusammenfassung zu nutzen.
Das war zu eng und der Grund für die damalige Nullausbeute. Für den Sammellauf
galt eine abgestufte Regel:

- **Starker Beleg: der Seitentitel.** Forenthread-Titel nennen sehr oft
  Hersteller, Baureihe, Code und Kernsymptom.
- **Schwacher Beleg: die Zusammenfassung.** Nutzbar für die Richtung einer
  Ursache, nie als Tatsachenbehauptung.

Der Anlass für diese Abstufung ist belegbar: in einer Testsuche zu einem
Gasgerät schob die Zusammenfassung ein „Rückschlagventil hinter dem Öl" ein —
sachlich unmöglich. Entsprechend steht in den neuen Fällen in
`tatsaechliche_ursache` überwiegend „Nicht geklärt" mit ausdrücklich als
ungesichert gekennzeichneter Richtungsangabe.

Die Regeltreue der Agenten wurde nach dem Lauf maschinell geprüft:

| Prüfung | Verstöße |
|---|---:|
| Regel 6 – `[Fachkraft]`-Präfix bei gas/strom | 0 |
| Regel 6 – `fachkraft_erforderlich` bei gas/strom | 0 |
| Regel 1 – Codebedeutung ohne Fehlercode | 0 |
| Regel 2 – `symptom_laie` über 200 Zeichen | 0 |
| Suchvorbehalt in `unsicherheiten` vermerkt | 0 fehlend |

## 9.5 Wie die neuen Codes eingetragen wurden

22 neue Codeknoten. Ihre `offizielle_bedeutung` steht durchgängig auf **null**,
obwohl die Agenten Bedeutungen aus den Suchzusammenfassungen mitgeliefert haben.
Diese Angaben stehen stattdessen im Feld `unsicherheiten`, ausdrücklich als
ungesichert markiert.

Das ist dieselbe Linie, die der erste Durchlauf für die vier Viessmann-Codes
gewählt hat — und die der Recherchelauf des zweiten Durchlaufs unabhängig
bestätigt hat. Eine aus einer Suchzusammenfassung stammende Bedeutung zur
„offiziellen Bedeutung" zu erheben, wäre genau der Fehler, den der erste
Durchlauf bei den Ratgeberportalen beschrieben hat.

Zwei Codeangaben wurden dabei bereinigt: `A6 227` ist der im Bestand bereits
dokumentierte Zifferndreher von `6A 227` und wurde normalisiert; `Eb` und `EB`
sind Schreibvarianten desselben Viessmann-Codes.

## 9.6 Schritt 5: Sprachbrücke von 17 auf 40 Einträge

Die 18 neuen Symptomklassen aus dem Sammellauf waren zunächst über keine
Laienschilderung erreichbar — der Validator meldete das als 18 Warnungen. Vier
Agenten haben daraus 23 Brückeneinträge gebildet, **ohne jede weitere Suche**,
allein aus den Laienschilderungen der gesammelten Fälle.

Ein Vorbehalt steht dazu jetzt in `sprachbruecke.json`: die Schilderungen sind
bereits Zusammenfassungen, nicht der Originalwortlaut der Nutzer. Die neuen
Ausdrücke sind also plausible alltagssprachliche Fassungen, keine belegten
Zitate.

Neu abgedeckt sind unter anderem Warmwasserverhalten („beim Duschen wird das
Wasser nach kurzer Zeit kalt"), Druckverhalten („Wasser muss ständig nachgefüllt
werden"), Geräusche („es knallt, wenn der Brenner ausgeht") und Zeitbezüge
(„seit der Wartung geht sie immer wieder auf Störung").

## 9.7 Was jetzt zu tun ist

1. **`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` anheben oder eine frische Session
   starten.** Ohne das sind die 18 ausgefallenen Zellen nicht nachholbar. Sie
   sind unverändert im Workflow-Skript hinterlegt und wieder ausführbar.
2. **Junkers/Bosch und Wolf gezielt nachziehen** — 26 Codes ohne einen einzigen
   Fall.
3. **Umgebung mit freiem HTTP-Ausgang.** Bleibt Voraussetzung null: ohne sie
   keine TDM-Prüfung und kein einziger neuer `bestaetigt`-Fall, egal wie viele
   Suchen zur Verfügung stehen.
4. **Die 142 neuen Fälle stichprobenartig gegen die Threads prüfen**, sobald
   Seitenabruf möglich ist. Erst dann lässt sich sagen, wie viele davon zu
   `bestaetigt` aufsteigen — und wie viele zu verwerfen sind.

---

# 10. Vierter Durchlauf: die nachgeholten 18 Suchzellen

Stand 22.08.2026. Das WebSearch-Kontingent war wieder verfügbar. Die im dritten
Durchlauf am erschöpften Budget gescheiterten 18 Zellen wurden nachgeholt —
diesmal **nach Priorität geordnet** (Junkers/Bosch und Wolf zuerst) und mit einem
Deckel von 8 Suchen je Zelle, damit alle 18 durchkommen. Ergebnis: **147 von 200
Suchen verbraucht, alle 18 Zellen ausgeführt.**

## 10.1 Ergebnis

| Kennzahl | Durchlauf 1 | Durchlauf 3 | **jetzt** | Ziel |
|---|---:|---:|---:|---:|
| Fälle | 8 | 150 | **269** | 120–250 ✅ |
| Fehlercode-Einträge | 52 | 74 | **100** | 200–500 ❌ |
| Symptomklassen | 6 | 38 | 51 | – |
| Sprachbrücken-Einträge | 17 | 40 | **56** | – |

Und die eigentliche Korrektur — die Herstellerschieflage ist weg:

| Hersteller | vorher | **jetzt** | Anteil | Codes |
|---|---:|---:|---:|---:|
| Vaillant | 70 | 79 | 29 % | 23 |
| Viessmann | 67 | 82 | 30 % | 19 |
| Buderus | 13 | 41 | 15 % | 17 |
| Junkers/Bosch | **0** | **36** | 13 % | 22 |
| Wolf | **0** | **31** | 12 % | 19 |

Beide Nulllücken sind geschlossen. Codes mit Fallverankerung: von 42 auf **80 von
100** — der Anteil verwaister Codeknoten ist von 43 % auf 20 % gefallen.

Auch die zweite dokumentierte Lücke ist bearbeitet: **112 der 269 Fälle tragen
keinen Fehlercode** (42 %). Der erste Durchlauf hatte dafür genau einen Fall und
nannte es „die schwächste Stelle des Bestands" — der Zielnutzer beschreibt eben
meist keinen Code. Neu abgedeckt sind Geräusche, Gerüche, Warmwasserverhalten,
Druckverhalten und Ausfälle ohne Anzeige.

## 10.2 Die Gegenprüfung hat 40 % verworfen

235 Kandidaten wurden erhoben, **95 davon in einer adversarischen Offline-Prüfung
verworfen** — je Suchzelle ein Prüfer, der jeden Fall gegen sechs Kriterien hielt
und im Zweifel verwerfen sollte. Bewusst ohne Suchzugriff: die knappe Ressource
ist die Suche, nicht das Denken.

Die häufigsten Verwerfungsgründe:

- **Überdehnung** — eine Ursache steht als Tatsache statt als ungesicherte
  Richtung, oder `symptom_technisch` nennt eine Fehlerphase, die aus dem Titel
  nicht ableitbar ist. Beispiel: ein Fall räumte selbst ein, „Bedeutung des Codes
  EF nicht belegt", behauptete aber eine „Störabschaltung des Feuerungsautomaten".
- **Kein individueller Fall** — die URL zeigt auf eine Codedatenbank oder
  Ratgeberseite statt auf die Schilderung eines Betreibers.
- **Modellreihe unbelegt** — der Titel nennt nur „Fehlercode OE" ohne Baureihe,
  die Zuordnung kam aus der Zusammenfassung.

Danach blieben 130; nach Abzug von 9 Dubletten wurden **121 aufgenommen**.

## 10.3 Was bei der Aufnahme bereinigt wurde

| Bereinigung | Anzahl | Begründung |
|---|---:|---|
| Codeangabe normalisiert | 16 | `6A / 227` → `6A 227` (Basis- plus Zusatzcode), Wolf `52` → `052`, Klammerzusätze entfernt |
| Codeangabe entwertet | 4 | Aufzählungen wie `004 und 061` oder `E8; A4` sind kein Code — Feld auf `null`, Angabe nach `unsicherheiten` (Regel 1) |
| `code_offizielle_bedeutung` entwertet | 23 | Der Text trug den Herkunftsvorbehalt selbst („laut Zusammenfassung", „nicht verifiziert"). Eine aus der Suchzusammenfassung abgeleitete Bedeutung ist keine offizielle Bedeutung |
| Fälle wegen Quellsprache entfernt | 2 | Zwei polnischsprachige Foren. Die Auftragskonfiguration nennt „primär Deutsch, Englisch nur ergänzend"; zusätzlich ist eine fremdsprachige Überschrift ohne Seitenabruf nicht auf Übersetzungsfehler prüfbar (Regel 8) |

## 10.4 Neue Symptomklassen, darunter eine sicherheitskritische

13 neue Leitsymptomklassen. Die wichtigste ist **`gasgeruch`** — bisher kannte das
Vokabular nur `abgasgeruch`. Das ist keine Feinheit: Abgasgeruch bedeutet
verbrannte Abgase, Gasgeruch unverbranntes Brenngas. Der Brückeneintrag ist
bewusst so gefasst, dass die reine Geruchsschilderung ihn auslöst, ohne dass der
Anrufer irgendetwas anderes angeben muss.

Weiter neu: `display_ohne_funktion` (das Gerät ist dunkel, ein Code ist deshalb
gar nicht ablesbar — der Fall, in dem eine codebasierte Voranalyse strukturell
scheitert), `abgasweg_undicht`, `ueberdruck_abschaltung`,
`druckanzeige_weicht_ab`, `modulation_untere_grenze`, `mehrere_codes_gleichzeitig`,
`stoerung_nach_gasumstellung` sowie vier Geräuschklassen.

Eine Klasse wurde nach der Extraktion korrigiert: `waermetauscherschaden` stand
als Leitsymptom, ist aber ein Befund am geöffneten Gerät. Der Extraktionsagent
hat sie folgerichtig als nicht belegbar zurückgewiesen, statt einen Laienausdruck
zu erfinden — sie liegt jetzt auf der Achse `fallmerkmal`.

## 10.5 Was sich NICHT verbessert hat

**Der Bestätigungsgrad.** Weiterhin 3 bestätigte Fälle, jetzt neben 266
Vermutungen — ein Anteil von 1,1 %. Der Grund ist unverändert: WebFetch bleibt
für jede Domain blockiert, eine Lösungsbestätigung steht am Threadende und ist
ohne Seitenabruf nicht lesbar.

Das ist die zentrale Einschränkung des gesamten Bestands. Gemessen am Leitprinzip
des Auftrags — belegte Fälle schlagen Menge — sind 269 Fälle mit 3 Bestätigungen
ein **Breiten-, kein Tiefengewinn**. Der Bestand taugt als Landkarte des
Problemraums, nicht als Ground Truth.

**Die Fehlercode-Einträge.** 100 statt der geforderten 200–500. Der erste
Durchlauf hat vollständige Herstellertabellen bewusst nicht übernommen
(Datenbankschutz §87a ff. UrhG); diese Linie ist beibehalten. Die 100 Codes sind
fallverankert oder stammen aus derselben Codegruppe — der Zielkorridor ist ohne
Übernahme ganzer Tabellen nicht erreichbar, und das ist eine Rechts-, keine
Datenentscheidung.

**Die TDM-Prüfung.** Unverändert für alle 12 Domains ungeprüft.

## 10.6 Regeltreue über den Gesamtbestand

| Prüfung | Verstöße |
|---|---:|
| Regel 6 – `[Fachkraft]`-Präfix bei gas/strom über alle 269 Fälle | 0 |
| Regel 2 – `symptom_laie` über 200 Zeichen | 0 |
| Regel 1 – Codebedeutung ohne Fehlercode | 0 |
| Validator gesamt | 0 Fehler, 1 Warnung |

Die eine verbleibende Warnung ist berechtigt und soll stehen bleiben: VIE-0002 und
VIE-0003 teilen sich eine Quelle und sind damit nicht unabhängig.

## 10.7 Nächste Schritte

1. **Umgebung mit freiem HTTP-Ausgang.** Bleibt Voraussetzung null. Ohne sie
   keine TDM-Prüfung und kein einziger weiterer `bestaetigt`-Fall.
2. **Die 269 Fälle stichprobenartig gegen die Threads prüfen**, sobald
   Seitenabruf möglich ist. Erst dann lässt sich sagen, wie viele aufsteigen und
   wie viele zu verwerfen sind. Die Gegenprüfung hat 40 % der Rohkandidaten
   aussortiert — eine ähnliche Quote ist auch für die aufgenommenen nicht
   auszuschließen.
3. **Eval-Split** bleibt ausgesetzt, bis das Kriterium für `bestaetigt`
   festgeschrieben ist und genügend bestätigte Fälle vorliegen.
