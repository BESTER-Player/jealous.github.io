# Auditbefunde — Voranalyse-Datensatz Gas-Brennwerttherme

Stand 22.08.2026, zweiter Durchlauf. Erhoben von vier unabhängigen Prüfern
(Fallbasis, Taxonomie, Sprachbrücke, Methodik), fünf Rechercheläufen mit je
angehängter adversarischer Gegenprüfung und einer Konsolidierung — 15 Agenten,
63 Einzelbefunde, zu **36 Befunden** zusammengeführt.

| Schwere | Anzahl | davon umgesetzt |
|---|---:|---:|
| 🔴 kritisch | 7 | 5 |
| 🟠 hoch | 14 | 3 |
| 🟡 mittel | 11 | 2 |
| ⚪ niedrig | 4 | 0 |
| **gesamt** | **36** | **10** |

„Umgesetzt" heißt: die Änderung ist in `scripts/migration_2026-08-22.py` kodiert
und im Bestand wirksam. Die übrigen Befunde verlangen eine Produktentscheidung
oder eine andere Ausführungsumgebung und stehen als offene Punkte in `report.md`.

---

## 🔴 1. TDM-Pruefung nach §44b UrhG ist in dieser Umgebung nicht durchfuehrbar - der Bestand ist damit nicht produktiv verwendbar

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `quellenlog.md`

**Betroffen:** alle 11 verwendeten Domains, alle 8 Faelle, alle 52 Codes

ERHEBUNGSGRENZE, nicht mit Nacharbeit am Bestand behebbar. Genannt von der Methodik-Pruefung, gestuetzt vom Quellenlog selbst. Die Pruefung eines maschinenlesbaren Nutzungsvorbehalts setzt den Abruf von robots.txt und Nutzungsbedingungen je Quelle voraus. Der Egress-Proxy blockiert jeden Seitenabruf domainunabhaengig; das ist im Quellenlog inzwischen gemessen und mit einem Kontrollabruf gegen eine unbeteiligte Domain abgesichert. Fuer keine der 11 in der Taxonomie verwendeten Domains ist der Vorbehalt geprueft. Das ist die vorrangige Verwendbarkeitsschranke: sie haengt nicht an der Fallzahl und wird durch weitere Erhebung nicht kleiner, sondern groesser, weil jeder weitere Fall den Anteil vergroessert, der spaeter womoeglich quellenweise zurueckgebaut werden muss. Positiv und entscheidend fuer die Aufbewahrbarkeit: jeder Fall und jeder Code traegt eine quelle_url, ein quellenweiser Rueckbau ist technisch moeglich. Abschnitt 6 des Reports bildet diesen Stand nicht ab und listet die TDM-Pruefung als Punkt 1 einer Reihenfolge, die im naechsten Durchlauf abgearbeitet werden koenne.

> **Beleg:** quellenlog.md, Abschnitt 'Nachtrag 22.08.2026': Tabelle mit vier Zielen, durchgaengig EGRESS_BLOCKED, einschliesslich Kontrollabruf gegen eine unbeteiligte Domain. Gegenprobe im Bestand: alle 8 Datensaetze in faelle.jsonl und alle 52 Codes in fehlercode_taxonomie.json fuehren ein Feld quelle_url. report.md, Abschnitt 6, Empfehlungspunkte 1 und 3.

**Empfehlung:** Abschnitt 6 des Reports umstellen: Punkt 0 ist die Bereitstellung einer Umgebung mit freiem HTTP-Ausgang, erst danach sind TDM-Pruefung und Volltextlesen ueberhaupt Aufgaben. Im Report ausdruecklich festhalten, was der Bestand heute ist - eine Methoden-Voruntersuchung, keine Wissensbasis - und dass die quellenweise Rueckbaubarkeit ueber quelle_url die Bedingung seiner Aufbewahrung ist. Die Sammlung bis zur Klaerung nicht ausweiten (Regel 8).

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🔴 2. Vokabularbruch zwischen Sprachbruecke und Taxonomie: 14 von 17 Laienausdruecken zeigen auf undefinierte Klassen, der Bestand faellt durch seinen eigenen Validator

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `sprachbruecke.json`

**Betroffen:** 14 der 17 Brueckeneintraege; 3 der 6 Taxonomie-Klassen; scripts/validate.py

DATENDEFEKT, jetzt behebbar. VERSTAERKT: unabhaengig gemeldet von drei Pruefern (Taxonomie, Sprachbruecke, Methodik). Die Taxonomie definiert 6 Symptomklassen, die Bruecke referenziert 17 verschiedene Klassennamen; die Schnittmenge betraegt 3. Damit ist der Pfad Laienausdruck -> Symptomklasse -> Faelle/Codes fuer die Mehrheit der erfassten Ausdruecke funktionslos - genau der Pfad, den der Report als den eigentlichen Produktnutzen bezeichnet. Umgekehrt sind 3 Taxonomie-Klassen ueber keine Laienschilderung erreichbar. Ursache ist kein vergessenes Nachtragen, sondern ein Modellierungsfehler: die Klassen liegen auf mindestens vier Ebenen (Beobachtung am Geraet, Auftretensbedingung, Verlauf/Vorgeschichte, Befund nach Oeffnen sowie Anzeige- und Eingabephaenomene) und werden trotzdem in einer flachen Liste als gleichrangig gefuehrt, obwohl eine Laienschilderung regelmaessig je einen Wert aus mehreren Ebenen traegt. Der Zustand haette auffallen muessen: validate.py erkennt ihn vollstaendig und endet mit Exit-Code 1, und die README sieht das Skript als Pre-Commit-/CI-Schritt vor. Der Bestand ist mit bekanntermassen rotem Gate abgelegt worden, und weder Report noch README erwaehnen das.

> **Beleg:** Eigener Lauf von scripts/validate.py auf dem abgelegten Stand: 15 Fehler, 6 Warnungen, Exit 1; darunter 13 Fehler der Form 'bildet auf Symptomklasse ... ab, die in der Taxonomie nicht definiert ist', ein Fehler zu einem mehrdeutig_zu-Verweis auf 'stoerabschaltung' und 3 Warnungen 'hat keinen Eintrag in der Sprachbruecke'. Mengenvergleich: 6 definierte Klassen gegen 17 referenzierte, Schnittmenge stoerabschaltung_nur_bei_geschlossener_verkleidung, betriebsartabhaengige_stoerung, stoerung_nach_stillstand. Verzeichnis schema/ enthaelt ausschliesslich fall.schema.json.

**Empfehlung:** Einen verbindlichen Klassenkatalog als einzige Wahrheitsquelle festlegen - der Block symptomklassen in fehlercode_taxonomie.json - und die Bruecke ausschliesslich dagegen referenzieren lassen. Beim Aufloesen NICHT die 14 Namen blind nachtragen, sondern je Klasse ein Pflichtfeld 'achse' einfuehren (Beobachtung, Auftretensbedingung, Verlauf) und Mehrfachvergabe ueber Achsen zulassen; sonst wird der Konstruktionsfehler zementiert. Klassen ohne Fallbeleg bleiben mit leeren fall_ids stehen statt aufgefuellt zu werden (Regel 1). Bis zur Aufloesung darf der Bestand nicht weiterverarbeitet werden; den Validatorlauf als Pre-Commit-/CI-Schritt verbindlich machen.

**✅ Umgesetzt am 22.08.2026:** Vokabular konsolidiert, Achsentrennung eingefuehrt

## 🔴 3. Sicherheitsinversion in BUD-0002: Wegfall der verriegelnden Stoerung nach Laienmanipulation an der Flammenueberwachung wird als Besserung gewertet und zum Diagnoseschritt gemacht

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** BUD-0002 (tatsaechliche_ursache, diagnoseschritte[1], symptom_laie)

DATENDEFEKT, jetzt behebbar. Der Fall haelt fest, dass nach mehrfachem Stecken der Sensorleitung der Ionisationssonde der Fehler seltener und nicht mehr verriegelnd auftrat, deutet das als Kontaktfehler und uebernimmt es als Diagnoserichtung. Die Ionisationssonde ist die Flammenueberwachung, die verriegelnde Stoerung ihre Schutzabschaltung. Dass eine Schutzabschaltung ausbleibt, ist kein Indiz fuer Fehlerbehebung, sondern kann ebenso Verlust der Schutzwirkung bedeuten. Der Datensatz nimmt die guenstige Lesart, ohne die unguenstige zu nennen - die Gegenrichtung zu Regel 8. Verschaerfend traegt derselbe Fall Abgasgeruch und Kondensataustritt als Symptom, also eine akut sicherheitsrelevante Lage, und keiner der beiden Diagnoseschritte enthaelt dazu einen Eskalationshinweis. Ein Voranalyse-System lernt hier das Muster, Nachstecken an der Flammenueberwachung bringe Besserung - sachlich dieselbe Klasse wie die im Quellenlog bewusst ausgeschlossene Manipulation am Gasstroemungswaechter, nur nicht als solche erkannt.

> **Beleg:** faelle.jsonl, BUD-0002: tatsaechliche_ursache enthaelt die Beobachtung zum mehrfachen Stecken der Sensorleitung der Ionisationssonde samt Betreiberdeutung als Kontaktfehler; diagnoseschritte[1] fuehrt die Steckverbindungen der Ionisationssonde als Kontaktfehlerquelle; symptom_laie nennt Abgasgeruch und tropfendes Kondensat. Gegenprobe: quellenlog.md, Abschnitt 'Ausgeschlossene Quellen und Inhalte', Zeile zur Manipulation am Gasstroemungswaechter mit der Begruendung, ein Voranalyse-System duerfe so etwas nicht als Loesungsmuster lernen.

**Empfehlung:** Die Betreiberdeutung nicht als Diagnoserichtung fuehren: die Beobachtung entweder ersatzlos streichen oder ausdruecklich mit dem Vermerk versehen, dass ein Ausbleiben der Verriegelung auch Ausfall der Flammenueberwachung bedeuten kann und deshalb keine Entwarnung ist. In Diagnoseschritt 1 aufnehmen, dass Abgasgeruch vor jeder weiteren Diagnose eine Sofortmassnahme ist. Analog zum Gasstroemungswaechter-Fall pruefen, ob der Fall ganz auszuschliessen ist, und die Entscheidung im Quellenlog vermerken.

**✅ Umgesetzt am 22.08.2026:** Betreiberdeutung als Diagnoserichtung entfernt, Eskalations- und Gegenhinweis ergaenzt

## 🔴 4. benoetigte_teile nennt in zwei Faellen genau die Teile, die den Fehler laut Falltext nicht behoben haben

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VAI-0001 und BUD-0002 (benoetigte_teile)

DATENDEFEKT, jetzt behebbar. Bei VAI-0001 steht der Wasserdrucksensor als benoetigtes Teil, obwohl derselbe Fall festhaelt, dass Drucksensor und Pumpe bereits ohne dauerhaften Erfolg getauscht wurden und die eigentliche Pruefrichtung die Verschmutzung der Aufnahmebohrung ist - also gerade kein Teil. Bei BUD-0002 steht der Kondensatsammler, obwohl der Fall ausdruecklich sagt, dass dessen Austausch zwar Geruch und Kondensataustritt beseitigte, die Stoerung 6A 227 aber bestehen blieb. In beiden Faellen empfiehlt das Feld die bereits gescheiterte Massnahme. Fuer ein Voranalyse-System ist das die schaedlichste Form von Fehlinformation, weil sie exakt den Fehlgriff reproduziert, den der Report unter Muster M3 selbst als Kernproblem beschreibt. Zusaetzlich ist bei BUD-0002 aus dem im Text genannten Kondensatsammler im Teilefeld 'Kondensatsammler/Siphon' geworden - der Siphon ist ein anderes Bauteil und kommt im Fall nicht vor (Regel 1). BUD-0001 zeigt mit leerer Liste, dass die korrekte Verwendung im Bestand bereits vorkommt.

> **Beleg:** faelle.jsonl, VAI-0001: benoetigte_teile ['Wasserdrucksensor'] bei symptom_technisch 'Wasserdrucksensor und Pumpe bereits getauscht ohne dauerhaften Erfolg'. BUD-0002: benoetigte_teile ['Kondensatsammler/Siphon'] bei tatsaechliche_ursache '... die Stoerung 6A 227 blieb jedoch bestehen'. BUD-0001: benoetigte_teile []. Vergleiche report.md, Musterbefund M3.

**Empfehlung:** benoetigte_teile in beiden Faellen auf [] setzen. Die Feldsemantik in der README klarstellen: aufzunehmen sind nur Teile, deren Austausch die Stoerung nachweislich behoben hat. validate.py um eine Warnung erweitern, die anschlaegt, wenn benoetigte_teile befuellt ist, waehrend tatsaechliche_ursache eine Nichtaufloesung ausdrueckt.

**✅ Umgesetzt am 22.08.2026:** benoetigte_teile in VAI-0001 und BUD-0002 geleert, Validatorwarnung ergaenzt

## 🔴 5. Der Bestaetigungsgrad ist keine belastbare Groesse - gleiche Beleglage fuehrt zu unterschiedlichen Graden, und alle darauf aufbauenden Kennzahlen sind entwertet

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0001, VIE-0002, VIE-0003, BUD-0001, VIE-0004 (bestaetigungsgrad); report.md Abschnitt 1 und 2; README-Kennzahlen; split_log.md

DATENDEFEKT im Bestand, verursacht durch eine Erhebungsgrenze (siehe Befund zur Volltextsperre). VERSTAERKT: von der Fall-Pruefung in fuenf Einzelbefunden und von der Methodik-Pruefung unabhaengig gemeldet. Von fuenf als bestaetigt gefuehrten Faellen haelt hoechstens einer bis zwei einer inhaltlichen Pruefung stand. BUD-0001 und VIE-0004 tragen im Unsicherheitenfeld denselben Suchauszugsvorbehalt, der bei VAI-0001, BUD-0002 und VIE-0005 zu 'vermutung' fuehrt - ein Kriterium fuer die Ungleichbehandlung ist im Bestand nirgends genannt; der Unterschied liegt allein darin, ob im Auszug zufaellig ein Erfolgssatz sichtbar war, wovor der Report selbst warnt. Bei VIE-0001 heben die eigenen Unsicherheiten die Bestaetigung auf: geprueft wurde nur der Warmwasserbetrieb, waehrend das Leitsymptom gerade das Umschalten betrifft, der Beobachtungszeitraum betrug etwa eine Woche bei einem Fehler, der gehaeuft nach Stillstandsphasen auftritt, drei erfolglose Vortausche konfundieren die Kausalitaet, und am als defekt bezeichneten Teil war optisch kein Unterschied zum Neuteil erkennbar. VIE-0003 ist die Anekdote eines antwortenden Nutzers ohne Fehlercode, ohne Geraetebaujahr und ohne ueberpruefbare Rueckmeldung, traegt aber den hoechsten Grad und behauptet zugleich in symptom_technisch eine spezifische Fehlerphasenzuordnung, fuer die der Fall keine Grundlage nennt (Regel 1). VIE-0002 behauptet als einziger Fall Unsicherheitsfreiheit, obwohl der Wirkmechanismus eine Rekonstruktion ist, die zugehoerige Messung nur als Diagnosevorschlag im selben Fall steht, eine Angabe in symptom_technisch in der Laienschilderung keine Entsprechung hat und eine Betreiberaussage in abweichung_von_doku als Sachverhalt gefuehrt wird. Damit ist 'bestaetigt' im Bestand kein definierter Grad, und die Quoten in Report und README sowie die Grundgesamtheit des Eval-Splits ruhen auf dieser Groesse.

> **Beleg:** faelle.jsonl: BUD-0001 und VIE-0004 mit bestaetigungsgrad 'bestaetigt' und Suchauszugsvorbehalt in unsicherheiten; VAI-0001, BUD-0002, VIE-0005 mit demselben Vorbehalt und Grad 'vermutung'. VIE-0001 unsicherheiten zur Erfolgsmeldung nach ca. einer Woche bei nur geprueftem Warmwasserbetrieb; VIE-0003 unsicherheiten zu fehlendem Fehlercode und unbekanntem Baujahr bei fehlercode null; VIE-0002 unsicherheiten null. Validatorausgabe: bestaetigt=5, vermutung=3. report.md Abschnitt 2: 'bestaetigt | 5 | 62,5 %'. Gegenprobe: quellenlog.md, Nachtrag, mit der eigenen Folgerung, der Grad bestaetigt sei in dieser Umgebung nicht vergebbar.

**Empfehlung:** Ein explizites Kriterium in die README aufnehmen und durchsetzen: 'bestaetigt' nur bei vollstaendig gesichtetem Thread mit Rueckmeldung des Fragestellers. Danach nach Regel 8 alle fuenf Faelle auf 'vermutung' herabsetzen, solange kein belegter Volltextabruf nachweisbar ist, und die Quoten in Report, README und split_log neu rechnen. Bei VIE-0001 zusaetzlich tatsaechliche_ursache von der Faktenbehauptung in eine Beobachtung umschreiben; bei VIE-0003 die Phasenzuordnung in symptom_technisch streichen; bei VIE-0002 unsicherheiten befuellen. validate.py um eine Warnung erweitern, die 'bestaetigt' in Verbindung mit einem Suchauszugsvorbehalt anzeigt.

**✅ Umgesetzt am 22.08.2026:** VIE-0001 und VIE-0003 auf 'vermutung' herabgestuft

## 🔴 6. Beleglage der drei staerksten Faelle ungeklaert: Report behauptet zwei vollstaendig gelesene Threads, Quellenlog misst jeden Seitenabruf als blockiert

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `report.md`

**Betroffen:** report.md Kopfzeile und Abschnitt 1; quellenlog.md Nachtrag; VIE-0001, VIE-0002, VIE-0003; 48 von 52 Codebedeutungen

GRENZFALL: die Behauptung im Report ist jetzt korrigierbar (Datendefekt), die Klaerung der tatsaechlichen Herkunft der drei Faelle setzt eine andere Umgebung voraus (Erhebungsgrenze). VERSTAERKT: von der Fall-Pruefung und der Methodik-Pruefung unabhaengig gemeldet. Der Report stuetzt seinen als wichtigsten bezeichneten methodischen Befund und seine gesamte Planungsempfehlung auf die Gegenueberstellung von zwei vollstaendig gelesenen Threads gegen 25 nur als Suchauszug bewertete Diskussionen und zitiert aus einem Thread woertlich. Das Quellenlog stellt demgegenueber fest, dass der Egress jeden direkten Seitenabruf blockiert, und folgert selbst, der Grad bestaetigt sei in dieser Umgebung nicht vergebbar. Beides zusammen ist nicht haltbar. Genau die drei Faelle ohne Suchauszugsvorbehalt (VIE-0001, VIE-0002, VIE-0003) sind die, deren Bestaetigung an den behaupteten Vollabrufen haengt, und sie sind zugleich die einzigen mit gesetztem quelle_datum. Dieselbe Frage stellt sich fuer die Taxonomie: 48 der 52 Codes tragen eine ausformulierte offizielle_bedeutung samt Baureihenlisten, ueberwiegend aus Seiten, die nach der Abrufbilanz nie abgerufen wurden. Solange das offen ist, ist die Beweislage des belastbarsten Teils des Bestands ungeklaert.

> **Beleg:** report.md, Kopfzeile 'Ein Durchlauf, 12 Abrufe (10 Suchen, 2 vollstaendig gelesene Threads)' und Abschnitt 1 mit woertlichem Threadzitat. quellenlog.md, Nachtrag mit EGRESS_BLOCKED fuer vier Ziele inklusive Kontrollabruf. faelle.jsonl: nur VIE-0001, VIE-0002, VIE-0003 ohne Suchauszugsvorbehalt und mit gesetztem quelle_datum (2020-06-26, 2026-03-02, 2026-02-20). fehlercode_taxonomie.json: 48 von 52 Codes mit befuellter offizielle_bedeutung, 0 von 52 mit quelle_datum. Zusaetzlich weicht die Abrufbilanz vom Quellenlog ab, das 17 Threads und 12 Einzelseiten fuehrt.

**Empfehlung:** Widerspruch aufloesen, bevor der Bestand weitergereicht wird: die Abrufbilanz je Quelle nachziehen und im Quellenlog festhalten, was Suchauszug und was Vollabruf war. Bis dahin nach Regel 8 die konservative Lesart einnehmen - alle Faelle als auszugsbasiert behandeln, die drei quelle_datum-Werte auf null setzen und die Codes ohne belegten Vollabruf mit einem Unsicherheitsvermerk versehen, so wie es bei den vier Viessmann-Codes mit offizielle_bedeutung null bereits vorbildlich gemacht wurde. Das woertliche Threadzitat aus report.md entfernen (Regel 2).

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🔴 7. Sicherheitsrelevantes Leitsymptom Abgasgeruch ist nicht aufloesbar, die Sprachbruecke fuehrt keine Gefahrenkategorie, und die Kombiklasse verlangt zwei Merkmale gleichzeitig

**Schwere:** kritisch &nbsp;·&nbsp; **Datei:** `sprachbruecke.json`

**Betroffen:** Brueckeneintrag 'riecht nach Abgas'; Feldsatz aller 17 Eintraege; Taxonomie-Klasse abgasgeruch_und_kondensataustritt (Ankerfall BUD-0002)

DATENDEFEKT, jetzt behebbar. Gemeldet von der Sprachbruecken-Pruefung, im strukturellen Teil verstaerkt durch den Vokabularbruch-Befund. Die Bruecke ist die Schicht, die Laieneingaben zuerst beruehrt. Der einzige Ausdruck fuer austretende Verbrennungsgase bildet auf eine Klasse ab, die die Taxonomie nicht kennt - die Zuordnung endet im Nichts, und zwar bei genau dem Signal, das eine sofortige Reaktion ausloesen muesste. Verschaerfend kennt das Eintragsschema der Bruecke kein Feld gefahrenkategorie: eine Gefahreneinstufung entsteht erst, wenn eine Symptomklasse oder ein Code aufgeloest ist; faellt die Aufloesung aus, gibt es keine Einstufung, und das Regel-6-Regime haengt an genau diesem Schritt. Die Taxonomie fuehrt den Sachverhalt stattdessen als UND-verknuepfte Kombiklasse abgasgeruch_und_kondensataustritt. Diese ist aus keiner Schilderung erreichbar, die nur eines der Merkmale nennt - also gerade aus der Geruchsschilderung allein -, sie skaliert nicht (n Beobachtungen erzeugen potentiell 2^n Kombiklassen), und sie verlagert eine Ursachenannahme in die Symptomebene. Ihr eigener Ankerfall widerlegt die Kopplung: dort beseitigte der ersetzte Kondensatsammler Geruch und Kondensataustritt, waehrend die Stoerung fortbestand.

> **Beleg:** sprachbruecke.json: Eintrag 'riecht nach Abgas' mit symptomklasse 'abgasgeruch'; getrennter Eintrag 'tropft Kondensat aus dem Geraet' mit symptomklasse 'kondensataustritt'; kein Eintrag der Datei fuehrt ein Feld gefahrenkategorie. fehlercode_taxonomie.json: Klasse 'abgasgeruch_und_kondensataustritt', fall_ids ['BUD-0002']. faelle.jsonl BUD-0002 tatsaechliche_ursache. Validatorausgabe: Fehler zu 'abgasgeruch' und 'kondensataustritt' als undefinierte Klassen, Warnung zur unerreichbaren Kombiklasse.

**Empfehlung:** Konflikt zugunsten der Einzelklassen aufloesen: abgasgeruch (gefahrenkategorie gas) und kondensataustritt (wasser) als eigenstaendige Beobachtungsklassen aufnehmen, die Kombiklasse mit Status 'abgeloest' und Verweis auf beide Nachfolger erhalten, damit die Aenderung nachvollziehbar bleibt. Begruendung der Richtung: Mehrfachvergabe bildet die Kombination verlustfrei nach, der umgekehrte Weg vernichtet Information, und die Geruchsschilderung allein muss feuern koennen. BUD-0002 traegt danach beide Klassen. Das Eintragsschema der Bruecke um gefahrenkategorie erweitern, von der Zielklasse geerbt; solange keine Zielklasse aufloesbar ist, konservativ wie gas behandeln (Regel 8).

**✅ Umgesetzt am 22.08.2026:** Kombiklasse abgeloest, Einzelklassen eingefuehrt, Sprachbruecke erbt gefahrenkategorie

## 🟠 8. Zeitliche Unmoeglichkeit: der Antwortbeitrag VIE-0003 ist zehn Tage vor dem Thread datiert, auf den er antwortet

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0002 und VIE-0003 (quelle_datum)

DATENDEFEKT, jetzt behebbar. VIE-0003 ist laut eigenem Unsicherheitentext eine Antwort im Thread von VIE-0002 und teilt dessen Quell-URL, ist aber frueher datiert. Eine Antwort kann nicht vor dem Beitrag existieren, auf den sie antwortet. Damit ist mindestens eines der beiden Daten falsch oder die Beitragsbeziehung falsch beschrieben. Da beide Faelle als bestaetigt gefuehrt werden und nur drei von acht Faellen ueberhaupt ein quelle_datum tragen, ist das kein Schoenheitsfehler, sondern ein Beleg dafuer, dass die Datumsangaben nicht aus dem Beitrag selbst stammen koennen - und damit ein zweites, unabhaengiges Indiz fuer den ungeklaerten Beleglage-Befund.

> **Beleg:** faelle.jsonl, eigene Nachpruefung: VIE-0002 quelle_datum 2026-03-02, VIE-0003 quelle_datum 2026-02-20, beide mit derselben quelle_url (td-p/606913); VIE-0003 unsicherheiten beschreibt die Eigenerfahrung eines antwortenden Nutzers innerhalb eines fremden Threads. Validatorwarnung zur mehrfach verwendeten Quelle bestaetigt die geteilte URL.

**Empfehlung:** Beide Daten auf null setzen, bis sie am Beitrag selbst verifiziert sind - genau die Linie, die der Report fuer Indexdaten bereits vorgibt. validate.py um eine Pruefung erweitern: bei geteilter quelle_url darf das Datum des als Antwort markierten Falls nicht vor dem des Ausgangsfalls liegen.

**✅ Umgesetzt am 22.08.2026:** quelle_datum von VIE-0002 und VIE-0003 auf null

## 🟠 9. gefahrenkategorie folgt drei einander widersprechenden Zuordnungslogiken, obwohl das Feld das Regel-6-Gatter ausloest

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** gefahrenkategorie aller 52 Codes; Beweispaare F.73/E2, F.32+3C/C1-C6, Wolf 006+001/E9

DATENDEFEKT, jetzt behebbar. In _meta ist nicht festgelegt, wonach die Kategorie vergeben wird; faktisch mischen sich drei Logiken - betroffenes Medium, betroffene Bauteilklasse, Gefahrenwirkung der Stoerung. Drei Paare belegen die Kollision unmittelbar: ein Vaillant-Drucksensorfehler steht auf wasser, waehrend ein Junkers-Vorlauffuehlerfehler auf strom steht, obwohl beides ein Sensor im Wasserkreis ist, der elektrisch auffaellig wird; Geblaesecodes bei Vaillant und Buderus stehen auf strom, waehrend die Junkers-Druckdosencodes desselben Luft- und Abgaswegsystems auf gas stehen; die Wolf-Codes zur Sicherheitstemperaturueberwachung stehen auf wasser, der gleichartige Junkers-Code auf gas. Das ist nicht Ordnungskosmetik: in validate.py loest gas oder strom das Regel-6-Regime aus, das fachkraft_erforderlich und das Praefix [Fachkraft] erzwingt. 10 der 52 Codes stehen auf wasser und wuerden dieses Regime nicht ausloesen, obwohl der gesamte Bestand Gas-Brennwertthermen betrifft und einzelne dieser Codes eine Sicherheitsabschaltung beschreiben.

> **Beleg:** fehlercode_taxonomie.json: F.73 'wasser' gegen E2 'strom'; F.32 und 3C 'strom' gegen C1, C2, C4, C6 'gas'; Wolf 006 und 001 'wasser' gegen Junkers/Bosch E9 'gas'. Eigene Auszaehlung ueber alle Codes: gas 29, strom 13, wasser 10. _meta enthaelt keine Zuordnungsregel.

**Empfehlung:** Zuordnungsregel in _meta schriftlich festlegen und den Bestand einmal danach durchgehen. Empfohlen wird eine Trennung in zwei Felder: gefahrenkategorie ausschliesslich als Sicherheitsgatter - fuer ein gasbefeuertes Geraet nie unterhalb der Wirkung, die die Stoerung ausloesen kann, Sicherheitseinrichtungen nie als reines Wasserthema - und ein neues Feld subsystem fuer die fachliche Einordnung. Solange die Regel fehlt, das Feld nicht fuer Ableitungen ueber Laientauglichkeit verwenden (Regel 8).

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 10. BUD-0001 haengt an einer Symptomklasse, deren Beschreibung dem Fall in der Richtung widerspricht

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Symptomklasse betriebsartabhaengige_stoerung (fall_ids VIE-0005, BUD-0001); sprachbruecke.json Eintrag 'Warmwasser geht, Heizung nicht'

DATENDEFEKT, jetzt behebbar. VERSTAERKT: unabhaengig gemeldet von der Fall- und der Taxonomie-Pruefung. Die Klasse verlangt stoerungsfreien Warmwasserbetrieb bei hoher Last und Stoerung im Heizbetrieb nahe der unteren Modulationsgrenze. VIE-0005 erfuellt das, BUD-0001 widerspricht in drei Punkten: die Richtung ist umgekehrt, denn dort fiel zuerst der Warmwasserbetrieb aus und der Heizbetrieb war erst spaeter dauerhaft betroffen; das Unterscheidungsmerkmal der Klasse, der Lastpunkt an der unteren Modulationsgrenze, kommt im Fall an keiner Stelle vor; und die angegebene Ursache liegt in der vorgelagerten Gasversorgung ausserhalb des Geraets und ist damit nicht lastpunktabhaengig. Wahrscheinlicher Entstehungsweg ist ein Wortabgleich statt eines Bedeutungsabgleichs ueber den Brueckeneintrag mit aehnlichem Wortlaut. Folge: die Klasse traegt zwei fall_ids statt einer und wirkt belegter als sie ist, und die Bruecke leitet die Laienformulierung auf eine Klasse, unter der ein Fall mit gegenlaeufigem Verlauf haengt. Die Klassenanmerkung in der Bruecke traegt zusaetzlich eine Ursachendeutung, die BUD-0001 gerade widerlegt.

> **Beleg:** fehlercode_taxonomie.json, Klasse 'betriebsartabhaengige_stoerung' mit fall_ids ['VIE-0005','BUD-0001'] und der Beschreibung zum stoerungsfreien Warmwasserbetrieb bei hoher Last. faelle.jsonl BUD-0001 symptom_technisch: 'zunaechst nur im Warmwasserbetrieb auffaellig, nach Wiederinbetriebnahme des Heizbetriebs dauerhaft'; tatsaechliche_ursache nennt ein festsitzendes Ventil am Gasdruckregler auf Netzbetreiberseite. sprachbruecke.json, Eintrag 'Warmwasser geht, Heizung nicht' mit der Anmerkung zum Lastpunkt.

**Empfehlung:** BUD-0001 aus der Klasse entfernen; der Fall bleibt ueber seinen Codeknoten verankert, ein Ersatzknoten wird nicht erfunden (Regel 8). Die Klassenbeschreibung um ein explizites Richtungsmerkmal ergaenzen und ein Feld abgrenzung_zu einfuehren. Die Anmerkung in der Sprachbruecke von der Ursachenbehauptung auf einen Hinweis zur Mehrdeutigkeit umstellen. Vermerken, dass die Klasse danach nur noch VIE-0005 traegt.

**✅ Umgesetzt am 22.08.2026:** BUD-0001 aus der Klasse entfernt, Richtungsmerkmal und abgrenzung_zu ergaenzt

## 🟠 11. Aus einer einzigen geteilten Quelle wird eine allgemeine Diagnoseregel - Verallgemeinerung genau dort, wo der Unabhaengigkeitsvorbehalt fehlt

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Symptomklasse stoerabschaltung_nur_bei_geschlossener_verkleidung (fall_ids VIE-0002, VIE-0003); VIE-0002 diagnoseschritte[0]

DATENDEFEKT, jetzt behebbar. Gemeldet von der Fall-Pruefung, in der Taxonomie-Pruefung als Teil des Unabhaengigkeitsproblems bestaetigt. Die Klassenbeschreibung erhebt aus zwei Faellen, die sich eine einzige Thread-URL teilen, eine gerichtete Kausalregel: das Symptom zeige auf Undichtigkeit mit Abgasrezirkulation und nicht auf den Feuerungsautomaten. Beide Faelle haben ausserdem unterschiedliche Ursachen und stuetzen damit nicht einmal dieselbe Hypothese. Der Diagnoseschritt in VIE-0002 wiederholt die Regel in der Fallbasis. Der Unabhaengigkeitsvorbehalt existiert nur als Fliesstext im Unsicherheitenfeld von VIE-0003 - also gerade nicht an der Stelle, an der die Verallgemeinerung tatsaechlich stattfindet, und auch nicht in VIE-0002 selbst. Wer VIE-0002 einzeln verarbeitet, und so wird eine Wissensbasis zeilenweise gelesen, bekommt kein Signal, dass der Fall nicht unabhaengig ist. Die im Report gefeierte saubere Handhabung ist damit nur halb umgesetzt: der Grad mehrfach_unabhaengig wurde korrekt vermieden, die inhaltliche Verdopplung nicht.

> **Beleg:** fehlercode_taxonomie.json, Klasse 'stoerabschaltung_nur_bei_geschlossener_verkleidung', fall_ids ['VIE-0002','VIE-0003'], Beschreibung mit der Ursachenzuweisung auf Undichtigkeit mit Abgasrezirkulation. faelle.jsonl VIE-0002 diagnoseschritte[0] mit derselben Aussage; VIE-0002 unsicherheiten null, waehrend nur VIE-0003 den Hinweis auf die geteilte Quelle traegt. Validatorwarnung: Quelle mehrfach verwendet, diese Faelle sind nicht unabhaengig.

**Empfehlung:** Die Klassenbeschreibung auf die beobachtbare Erscheinung beschraenken und die Ursachenzuweisung streichen oder als offene Pruefrichtung kennzeichnen; in der Klasse vermerken, dass beide fall_ids aus einer Quelle stammen. Den Diagnoseschritt in VIE-0002 von einer Deutung auf eine Pruefaufforderung umstellen. Den Vermerk zur geteilten Quelle symmetrisch in beiden Faellen fuehren, mittelfristig als eigenes Feld statt als Fliesstext.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 12. Doppelverankerung 6A / 6A 227: die Codehierarchie ist sachlich real, wird aber von keinem Feld ausgedrueckt

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Buderus-Codes '6A' und '6A 227'; Faelle BUD-0001, BUD-0002

DATENDEFEKT, jetzt behebbar. VERSTAERKT: von der Taxonomie- und der Fall-Pruefung gemeldet, in der Recherche-Gegenpruefung sachlich gestuetzt und vom Validator bereits als Warnung ausgegeben. Beide Faelle tragen genau einen Codestring, stehen aber in den fall_ids beider Knoten. Die Hierarchie aus Anzeigestoerung und praezisierendem Zusatzcode ist real - die Quell-URL gliedert die Ebenen im Pfad selbst, das Quellenlog kennt den Begriff Zusatzcode -, aber im Datenmodell existiert kein code_typ, kein zusatzcode und kein gehoert_zu_code; beide Knoten sind gleichrangige Listenelemente mit identischem Feldsatz. Damit ist die Doppelverankerung von einem Eintragungsfehler nicht unterscheidbar. Zwei Belege dagegen, dass sie sauber gewollt ist: der Oberknoten verankert BUD-0002, obwohl dessen Modellreihe nur beim Zusatzcodeknoten gelistet ist, und die ebenso reale Beziehung zwischen blockierender und verriegelnder Stoerung steht nur in Prosa. Folgen: jede Auswertung ueber fall_ids zaehlt beide Buderus-Faelle doppelt, und die Kennzahl der verankerten Codes beschreibt nur sechs unterschiedliche Codesachverhalte.

> **Beleg:** fehlercode_taxonomie.json: Knoten '6A' mit betroffene_baureihen ['Logamax plus GB172','Logamax plus GB172 T'] und fall_ids ['BUD-0001','BUD-0002']; Knoten '6A 227' mit betroffene_baureihen ['Logamax plus GB152','Logamax plus GB172','Logamax U154'] und identischen fall_ids. faelle.jsonl BUD-0002 modellreihe 'Logamax plus GB152'. Eigene Auszaehlung: 7 Codes mit fall_ids, davon 2 das Buderus-Duplikatpaar. Validatorausgabe: zweimal die Warnung zu Ober-/Zusatzcode.

**Empfehlung:** Felder ergaenzen: code_typ, zusatzcode, gehoert_zu_code sowie stoerungsart fuer die Beziehung blockierend/verriegelnd. Faelle nur am spezifischsten Knoten verankern und die Zuordnung zum Oberknoten aus gehoert_zu_code ableiten, statt fall_ids zu duplizieren (Regel 8). Zusaetzlich pruefen lassen, ob fall.modellreihe in betroffene_baureihen des verankernden Knotens enthalten ist.

**✅ Umgesetzt am 22.08.2026:** code_typ und gehoert_zu_code ergaenzt, Doppelverankerung aufgeloest

## 🟠 13. Verkappte Haeufigkeits- und Wahrscheinlichkeitsaussagen in Taxonomie, Sprachbruecke und Report (Regel 4), vom Validator nicht erfasst

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Symptomklassen stoerung_nach_stillstand und abgasgeruch_und_kondensataustritt; Codes Viessmann EE, Wolf 040, Vaillant F.75; Sprachbruecken-Eintrag zum Flammensymbol; report.md Musterbefunde M1 und M3

DATENDEFEKT, jetzt behebbar. VERSTAERKT: von drei Pruefern gemeldet (Faelle, Taxonomie, Methodik) und durch die Recherche-Gegenpruefung im Fall M1 zusaetzlich entkraeftet. In faelle.jsonl selbst wurde keine Haeufigkeitsaussage im Sinne von Regel 4 gefunden - die dortigen Woerter beschreiben das Verhalten eines einzelnen Geraets. In den angehaengten Artefakten dagegen mehrfach: eine Klassenbeschreibung nennt ein gehaeuftes Auftreten, gestuetzt auf genau einen Fall; eine zweite behauptet ein Auftreten oft parallel zu Zuendstoerungen, ebenfalls auf einen Fall gestuetzt, dessen eigener Text die Kopplung widerlegt; ein Codeknoten haelt fest, der Code werde in Threads regelmaessig gemeinsam mit zwei anderen genannt - eine ausdruecklich aus gesichteten Beitraegen abgeleitete Haeufigkeitsaussage; zwei weitere Codes nennen einen haeufigen Ausloeser beziehungsweise eine haeufige Wiedergabe in Ratgeberquellen. Im Report gehen M1 und M3 weiter: M1 stuetzt sich auf einen einzigen, als ungeklaert gefuehrten Fall mit Grad vermutung und formuliert dennoch systematisch, durchgaengig und haeufigste Fehlmassnahme; M3 gibt eine Quote aus acht Faellen an. Bemerkenswert ist die Ungleichbehandlung: das Quellenlog schliesst eine ganze Fremdquelle wegen einer Haeufigkeitsaussage aus, waehrend gleichartige Formulierungen im eigenen Bestand stehen bleiben. Der Validator faengt das nicht: sein Muster deckt nur Superlative und Prozentangaben ab und laeuft nur ueber drei Freitextfelder in faelle.jsonl.

> **Beleg:** fehlercode_taxonomie.json: Klasse 'stoerung_nach_stillstand' mit 'Stoerung gehaeuft beim ersten Start nach laengerem Stillstand' bei fall_ids ['VIE-0001']; Klasse 'abgasgeruch_und_kondensataustritt' mit '... oft parallel zu Zuendstoerungen' bei fall_ids ['BUD-0002']; Code EE unsicherheiten 'In Threads regelmaessig gemeinsam mit EB und FE genannt'; Code F.75 unsicherheiten mit 'haeufig'. sprachbruecke.json, Eintrag zum durchgestrichenen Flammensymbol. report.md M1 und M3. scripts/validate.py: RE_HAEUFIGKEIT nur auf Fallfelder angewandt. Gegenprobe: quellenlog.md, Ausschlusstabelle mit einer wegen Regel 4 ausgeschlossenen Fremdquelle.

**Empfehlung:** Alle genannten Formulierungen so umschreiben, dass sie den Beleg statt eine Verteilung nennen. M1 auf die belegbare Kernaussage zuruecknehmen und die Fallzahl offenlegen; M3 von der Quotenform auf eine Aufzaehlung der Fall-IDs umstellen. RE_HAEUFIGKEIT um haeufig, oft, gehaeuft, regelmaessig, ueberwiegend, durchgaengig, typisch erweitern und die Pruefung auf fehlercode_taxonomie.json, sprachbruecke.json und report.md sowie auf alle Freitextfelder ausdehnen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 14. Ausbeutequote und Hochrechnung des Reports sind nicht rekonstruierbar und widersprechen dem eigenen Kernbefund

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `report.md`

**Betroffen:** report.md Abschnitt 1 (Nenner, beide Quotenzeilen) und Abschnitt 6 (Hochrechnung 400-600 Threads)

DATENDEFEKT, jetzt behebbar. Der Nenner von rund 27 unterscheidbaren Diskussionen laesst sich aus dem Quellenlog nicht herleiten: dort sind 17 Threads und 12 Dokument- beziehungsweise Ratgeberseiten verzeichnet, was weder 27 noch die Zwischenzeile mit rund 21 Problemschilderungen ergibt. Beide Prozentangaben und die Aussage ueber die uebrigen 25 nur als Auszug bewerteten Diskussionen ruhen damit auf einer nirgends hergeleiteten Zahl. Die Hochrechnung in Abschnitt 6 wechselt zusaetzlich in einem Schritt Nenner, Zaehler und Quellenklasse: die 30 Prozent entstehen in Abschnitt 1 aus verwertbar geteilt durch gesichtet und werden in Abschnitt 6 als Ausbeute bestaetigter Faelle je vollstaendig gelesenem Thread aus einem Herstellerforum weiterverwendet. Die im Bestand tatsaechlich behauptete Groesse zeigt in die Gegenrichtung, und die zweite Quote der Spanne wird nirgends eingefuehrt. Das ist zugleich ein Regel-4-Verstoss, weil aus Thread-Anzahlen eine erwartete Trefferwahrscheinlichkeit fortgeschrieben wird, und ein Regel-8-Verstoss, weil der Report seine Quoten selbst als nach oben verzerrt bezeichnet und die guenstigere Variante dennoch als Planungsuntergrenze setzt.

> **Beleg:** quellenlog.md, Tabelle 'Genutzte Quellen': 8 + 8 + 1 Threads sowie 12 Seiten/Dokumente. report.md Abschnitt 1: 'unterscheidbare Diskussionen gesichtet ca. 27', 'davon mit erkennbarer Problemschilderung ca. 21', Quoten 30 % und 19 %, sowie 'Diese Quoten sind nach oben verzerrt'. report.md Abschnitt 6 mit der Spanne 400-600 gelesenen Threads.

**Empfehlung:** Entweder die 27 im Quellenlog belegen, indem die gesichteten Threads je Quelle aufgelistet werden, oder die Quoten mit dem belegten Nenner neu ausweisen und als Spanne darstellen. Die Zeile zur erkennbaren Problemschilderung belegen oder streichen. Die Hochrechnung streichen oder ohne Punktschaetzung und ausdruecklich als nicht belastbar kennzeichnen; wenn eine Planungszahl verlangt wird, nach Regel 8 die unguenstigste dokumentierte Quote verwenden und den Rechenweg mit Zaehler- und Nennerdefinition offenlegen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 15. Belegtiefe eines Codes ist im Modell nicht darstellbar - die Haelfte der Codes ruht auf einer einzigen Ratgeberliste unklarer Herkunft

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Feld quelle_url (einwertig) aller 52 Codes; besonders die 26 Codes einer Quelle sowie F5, 2E, 3C, F7, 040, 091, 6A 227

DATENDEFEKT, jetzt behebbar. Das Feld quelle_url ist einwertig. Dadurch laesst sich nicht unterscheiden, ob ein Code auf einer einzigen Seite oder auf mehreren uebereinstimmenden Quellen beruht, und ein Widerspruch zwischen Quellen ist ueberhaupt nicht darstellbar. Auf der Fallseite gibt es dafuer bestaetigungsgrad, auf der Codeseite fehlt jede Entsprechung - eine Asymmetrie im Modell. Inhaltlich stammen 26 der 52 Codes von einer Fachbetriebs-Ratgeberseite, die das Quellenlog selbst mit unklarer Listenherkunft fuehrt. Einzelne Codes ruhen auf je einer nicht-primaeren Quelle, darunter ausgerechnet der Knoten, der beide Buderus-Faelle verankert, und der Knoten, der den staerksten Viessmann-Fall verankert und dabei selbst keine belegte Bedeutung traegt. Die Recherche-Gegenpruefung hat unabhaengig davon gezeigt, dass die einschlaegigen Ratgeberportale erkennbar dieselben Herstellertabellen weiterreichen und deshalb nie als voneinander unabhaengige Bestaetigung gezaehlt werden duerfen.

> **Beleg:** Eigene Auszaehlung der Hosts in fehlercode_taxonomie.json: installateur-graf.at 26, wolf.eu 9, community.viessmann.de 5, heizungsforum.de 3, manualslib.de 2, heizungsdiagnose.de 2, je 1 fuer thermenwartung-kundendienst.at, ersatzteile-koeln.de, kesselheld.de, buderuscode.de, freeboilermanuals.com. quellenlog.md fuehrt die 26er-Quelle mit dem Vermerk, die Herkunft der Listen sei unklar.

**Empfehlung:** quelle_url durch ein Array 'quellen' ersetzen, je Eintrag mit typ (herstellerdoku, herstellerforum, fachforum, ratgeber, haendler, spiegelung) und Pruefdatum, und ein Feld beleggrad als Gegenstueck zu bestaetigungsgrad einfuehren. Bis dahin die Codes aus dieser einen Liste nicht als verifiziert behandeln und nach Regel 8 alle Codes ohne mindestens eine Primaerquelle im Modell als unverifiziert kennzeichnen, statt sie mit den herstellerdokumentierten Codes gleichrangig zu fuehren.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 16. Kein Schema fuer Taxonomie und Sprachbruecke - die Codestring-Kollision E8 ist nur im Pruefskript abgesichert

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** schema/ (enthaelt nur fall.schema.json); Viessmann 'E8' gegen Junkers/Bosch 'E8'; Felder sinneskanal und belegzahl der Bruecke

DATENDEFEKT, jetzt behebbar. VERSTAERKT: von der Taxonomie- und der Sprachbruecken-Pruefung gemeldet. Fuer die Fallsammlung existiert ein Schema mit additionalProperties false, das laut README Regel 4 mit absichert. Fuer Taxonomie und Bruecke gibt es keines. Damit ist dort weder der Feldsatz kontrolliert noch die Wertemenge von sinneskanal oder gefahrenkategorie noch die Zulaessigkeit numerischer Zaehlfelder. Die einzige Kollision im Bestand - derselbe Codestring bei zwei Herstellern mit unterschiedlicher Gefahrenkategorie - ist ausschliesslich zur Laufzeit abgesichert: validate.py schluesselt korrekt ueber das Paar aus Hersteller und Code, aber der Schluessel ist nirgends deklariert, hersteller ist in der Taxonomie ein freier String ohne die Enum-Bindung des Fallschemas, und der Fall verweist mit einem blanken Codestring ohne herstellerqualifizierten Bezug. Es gibt zudem keine Normalisierungsregel, obwohl der Bestand Gross- und Kleinschreibung tragend nutzt, fuehrende Nullen kennt und ein Leerzeichen innerhalb eines Codes enthaelt. Ein Schreibfehler im Herstellernamen oder eine unachtsame Normalisierung wuerde den Verbund lautlos trennen beziehungsweise einen Gas- und einen Wasserknoten zusammenfallen lassen.

> **Beleg:** Verzeichnis schema/ enthaelt ausschliesslich fall.schema.json. fehlercode_taxonomie.json besitzt keine Schemareferenz, _meta nennt keinen Schluessel. Codeliste: Viessmann E8 (gas, Ionisationsstrom ausserhalb des gueltigen Bereichs) und Junkers/Bosch E8 (Mindestdruckwaechter). sprachbruecke.json fuehrt Schreibvarianten eines Buderus-Codes unter einer Pseudo-Symptomklasse, die ihrerseits zu den undefinierten Klassen gehoert.

**Empfehlung:** schema/taxonomie.schema.json und schema/sprachbruecke.schema.json anlegen, beide mit additionalProperties false, mit Enums fuer hersteller, gefahrenkategorie, sinneskanal und achse, mit Pflichtfeldern und einem ausdruecklichen Verbot numerischer Zaehlfelder. Den Schluessel aus Hersteller und Code explizit dokumentieren, auf der Codeseite ein Feld schreibvarianten und einen normalisierten Schluessel ergaenzen und die Eingabenormalisierung dort verankern statt in der Sprachbruecke. Im Fallschema fehlercode um einen herstellerqualifizierten Verweis ergaenzen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 17. VIE-0004 macht die Instandsetzung einer sicherheitsrelevanten Leiterplatte zur bestaetigten Loesung und zweckentfremdet dabei das Teilefeld

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0004 (tatsaechliche_ursache, benoetigte_teile, unsicherheiten)

DATENDEFEKT, jetzt behebbar. Der Fall haelt fest, eine externe Instandsetzung der Platine durch Nachloeten habe die Stoerung behoben, fuehrt das als bestaetigt und schreibt in benoetigte_teile den Vermerk, eine Instandsetzung statt eines Tauschs sei moeglich. Damit wird eine Empfehlung zur Reparatur der Steuerung einer Gas-Brennwerttherme in die Wissensbasis geschrieben - eines Bauteils, das die Feuerungsueberwachung traegt. Das steht in Spannung zu der Linie, die derselbe Bestand beim ausgeschlossenen Eingriff an einer Schutzeinrichtung zieht. Zweitens ist benoetigte_teile zweckentfremdet: es enthaelt keinen Teilebezeichner, sondern einen eingeklammerten Ratschlag, was die Liste maschinell unbrauchbar macht. Drittens verweist das Unsicherheitenfeld auf einen defekten Zuendtrafo, der in keinem anderen Feld des Falls vorkommt - der Vorbehalt relativiert eine Aussage, die der Fall gar nicht trifft, sodass unklar bleibt, welcher Teil der Ursachenangabe unsicher ist.

> **Beleg:** faelle.jsonl, VIE-0004: bestaetigungsgrad 'bestaetigt', benoetigte_teile ['Leiterplatte (Instandsetzung statt Tausch moeglich)'], gefahrenkategorie 'strom', unsicherheiten mit dem Verweis auf eine Betreiberdeutung zum Zuendtrafo. Vergleiche quellenlog.md, Ausschlusstabelle.

**Empfehlung:** Den Klammerzusatz aus benoetigte_teile entfernen und die Aussage, sofern sie erhalten bleiben soll, in ein Freitextfeld verschieben. Grad auf 'vermutung' setzen (siehe Befund zum Bestaetigungsgrad). Ausdruecklich entscheiden und im Quellenlog vermerken, ob Instandsetzung sicherheitsrelevanter Steuerungen ueberhaupt als Loesungsmuster aufgenommen werden soll; nach Regel 8 spricht die konservative Wahl dagegen. Den Zuendtrafo-Verweis entweder mit dem zugehoerigen Sachverhalt ergaenzen oder streichen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 18. belegzahl in der Sprachbruecke ist ein Regel-4-Risiko - der erklaerende Vorbehalt reist nicht mit dem Wert mit

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `sprachbruecke.json`

**Betroffen:** Feld belegzahl in allen 17 Eintraegen; _meta.belegzahl_bedeutung

DATENDEFEKT, jetzt behebbar. Die Erlaeuterung im _meta ist fachlich richtig und trotzdem wirkungslos. Der Vorbehalt steht einmal im Kopf der Datei, die Zahl dagegen an jedem Eintrag - sobald Eintraege einzeln in Trainingsbeispiele, Embeddings, Promptkontext oder eine Tabellenansicht ueberfuehrt werden, bleibt die Zahl und der Vorbehalt faellt weg. Der Wert ist ordinal verwertbar: jeder Konsument kann danach sortieren, und eine sortierte Liste von Symptomausdruecken ist faktisch eine Haeufigkeitsaussage, unabhaengig von der Erklaerung. Die Zahl selbst ist zudem nicht belastbar: die gezaehlte Einheit ist der Beitrag, es gibt keinen Nenner, keine Liste der gezaehlten Beitraege und keine Herkunftspruefung, und der Bestand enthaelt nachweislich eine Quelle, die zwei Faelle traegt - Mehrfachzaehlung derselben Herkunft ist also moeglich. Die einzige maschinelle Regel-4-Sicherung greift hier nicht, weil sie eine Textpruefung ueber drei Fallfelder ist und ein Zahlenfeld grundsaetzlich nicht sehen kann. Der Bedarf dahinter ist real - man will wissen, ob ein Ausdruck auf einem Ratgebersatz oder auf mehreren Nutzerbeitraegen ruht -, die Zahl ist nur das falsche Instrument.

> **Beleg:** sprachbruecke.json: _meta.belegzahl_bedeutung erklaert die Zahl als Beleghaeufigkeit des Wortes und ausdruecklich nicht als Ursachenhaeufigkeit, waehrend jeder der 17 Eintraege ein numerisches Feld belegzahl traegt. scripts/validate.py: Regel-4-Pruefung nur ueber tatsaechliche_ursache, abweichung_von_doku und symptom_technisch in faelle.jsonl. Validatorwarnung zur mehrfach verwendeten Quelle.

**Empfehlung:** Nach Regel 8 das numerische Feld aus dem ausgelieferten Artefakt entfernen. Ersatz erstens durch eine Liste 'belege' mit expliziten Herkunftsverweisen auf fall_id oder Quellenlog-Eintrag, zweitens - falls eine Staerkeangabe gewuenscht ist - durch ein zweiwertiges Merkmal einzelbeleg/mehrfachbeleg ohne nutzbare Ordnung. Soll die Zaehlung fuer die interne Arbeit erhalten bleiben, gehoert sie in eine getrennte Herkunftsdatei ausserhalb der an das Modell uebergebenen Wissensbasis. Den Validator um eine Strukturpruefung erweitern, die numerische Zaehlfelder in Wissensbasis-Artefakten meldet.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 19. Die dokumentierte Auswahlregel der Taxonomie beschreibt den tatsaechlichen Bestand nicht - die urheberrechtliche Begruendung traegt so nicht

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** _meta.auswahlregel; die Wolf-, Junkers/Bosch- und Vaillant-Codebloecke

DATENDEFEKT, jetzt behebbar. _meta begruendet den Teilbestand damit, aufgenommen seien Codes, die einen Fall verankern, sowie Codes aus denselben Codegruppen; vollstaendige Herstellertabellen seien bewusst nicht uebernommen worden, weil die Liste als Ganzes als Datenbank geschuetzt sein koenne. Die Daten passen dazu nicht: Wolf und Junkers/Bosch haben zusammen einen erheblichen Teil des Bestands und keinen einzigen verankernden Fall, Vaillant hat 15 Codes bei einem Fall. Ohne verankernden Fall gibt es auch keine Codegruppe, an die angeknuepft werden koennte. Die Wolf-Codes bilden zudem einen nahezu zusammenhaengenden Nummernblock aus einem einzigen Herstellerdokument, die Vaillant- und Junkers-Codes je einen sortierten Durchlauf durch eine einzige Ratgeberliste - das aeussere Bild einer Tabellenentnahme, also genau dessen, was die Regel ausschliessen sollte. Damit ist die Regel nicht falsifizierbar formuliert und die auf sie gestuetzte konservative Entscheidung nicht belegt. Das ist keine Rechtsauskunft, sondern der Hinweis, dass die dokumentierte Begruendung den Bestand nicht deckt - relevant, weil die TDM-Pruefung fuer keine Quelle erfolgt ist.

> **Beleg:** fehlercode_taxonomie.json, _meta.auswahlregel, gegen die eigene Auszaehlung: nur 7 Codes tragen ueberhaupt fall_ids, alle bei Viessmann, Buderus und Vaillant; die Wolf- und Junkers/Bosch-Bloecke haben durchgaengig leere fall_ids. report.md, Abschnitt 3, weist fuer beide Hersteller null Faelle aus.

**Empfehlung:** Entweder die Auswahlregel so praezisieren, dass sie den tatsaechlichen Bestand beschreibt - etwa Codes aus derselben Anzeigegruppe eines verankerten Codes, hoechstens eine benannte Zahl Nachbarcodes -, und den Bestand daran messen; oder die nicht verankerten Bloecke bis zur nachgeholten TDM- und Schutzrechtspruefung zuruecknehmen. Konservative Wahl nach Regel 8 ist die Zuruecknahme, weil der Bestand ohnehin nicht produktiv verwendbar ist und die Codes ohne Fall derzeit keinen Nutzen tragen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 20. Die Rechercheausgabe enthaelt eine konstruierte URL und mehrere ueber den Titel hinaus aufgefuellte Symptomfelder - Regelverstoesse im Erhebungsprozess

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `quellenlog.md`

**Betroffen:** Rechercheausgaben der Bereiche ohne_code, junkers, wolf, code_gegenpruefung (nicht im Bestand)

PROZESSDEFEKT, jetzt behebbar - kein Datendefekt, da nichts davon in den Bestand gelangt ist. Die adversarische Gegenpruefung hat in der Recherche einen Fall gefunden, in dem ein real existierender Thread unter einer zusammengesetzten Adresse gefuehrt wurde: die Thread-Nummer stimmt, das Pfadsegment wurde offenbar aus dem Muster anderer Threads derselben Plattform gebildet und ist in keinem Suchtreffer auffindbar. Ein zweiter Eintrag trug einen fehlerhaften Adress-Slug, wurde aber vom Rechercheur selbst als unsicher gekennzeichnet und zum Verwerfen empfohlen - das ist das richtige Verhalten und die einzige Selbstmeldung, die den Fehler vor einer Uebernahme abgefangen haette. Daneben wurden mehrfach Symptomfelder ueber den belegten Titeltext hinaus ausgefuellt: ein Betriebszustand, ein Austrittsort und eine Bauteilfunktion wurden ergaenzt, obwohl die Beleglage im selben Eintrag mit 'nur Titel und URL' angegeben ist. Beides sind Verstoesse gegen Regel 1 und gegen die Vorgabe, niemals URLs zu erfinden. Uebergreifend gilt zusaetzlich: das Merkmal 'ohne Stoerungscode' ist in keinem Recherchefall positiv festgestellt, sondern durchgaengig aus dem Schweigen des Titels geschlossen.

> **Beleg:** Gegenpruefung Bereich ohne_code: ein Viessmann-Eintrag mit korrekter Thread-Nummer, aber nicht auffindbarem Rubrikensegment; ein Wolf-Eintrag mit verungluecktem Slug, vom Rechercheur selbst gekennzeichnet. Aufgefuellte Felder: Umschaltvorgang bei einem Vaillant-Heizgeraet ohne belegten Speicher, Austrittsort bei einem Viessmann-Kondensatfall, Funktionszuordnung zur Durchflussmessung bei einem Wolf-Bauteilfall. Gegenpruefung Bereich code_gegenpruefung: ein Fallkandidat, dessen Laiensymptom allein aus dem Dringlichkeitswort des Threadtitels gebildet war.

**Empfehlung:** Vor jeder Uebernahme in den Bestand jede URL erneut per Suche verifizieren und jedes Symptomfeld zeichenweise gegen den Titeltext abgleichen; was nicht im Titel steht, bleibt null (Regel 1). Das Feld zur sichtbaren Aufloesung umbenennen oder qualifizieren, da es eine Aussage ueber den Zugriff des Rechercheurs ist und nicht ueber die Quelle. Das Merkmal 'ohne Stoerungscode' im Datensatz ausdruecklich als Annahme kennzeichnen, solange es nur aus dem Titelschweigen folgt.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟠 21. Volltextabgleich unmoeglich: Bestaetigung, Codeverifikation und Regel-2-Pruefung sind in dieser Umgebung nicht durchfuehrbar

**Schwere:** hoch &nbsp;·&nbsp; **Datei:** `quellenlog.md`

**Betroffen:** bestaetigungsgrad aller Faelle; offizielle_bedeutung aller 52 Codes; symptom_laie aller Faelle

ERHEBUNGSGRENZE, nicht mit Nacharbeit am Bestand behebbar. Diese Grenze ist die Ursache mehrerer der oben genannten Datendefekte und muss getrennt gefuehrt werden, damit sie nicht als Nachlaessigkeit gelesen wird. Drei Pruefungen sind hier prinzipiell nicht ausfuehrbar. Erstens laesst sich ohne Seitenabruf keine Loesungsbestaetigung feststellen, weil der Suchauszug regelmaessig vor der Aufloesung abbricht - der Grad bestaetigt ist damit nicht vergebbar, neu erhobene Faelle koennen hoechstens vermutung erreichen. Zweitens ist die sachliche Richtigkeit der Codebedeutungen gegenueber Herstellerdokumentation nicht pruefbar; alle vier unabhaengigen Recherchelaeufe berichten uebereinstimmend, dass die Suche in dieser Umgebung ausschliesslich Titel und URL sowie eine maschinell erzeugte Zusammenfassung liefert und keine woertlichen Seitenauszuege, sodass Titeltext die einzige zitierfaehige Quelle bleibt. Drittens ist der Abgleich der Laienschilderungen gegen die Originalbeitraege - und damit die Pruefung auf Textuebernahme nach Regel 2 - nicht moeglich; mehrere symptom_laie-Felder sind vollstaendige umgangssprachliche Saetze, das Schema erlaubt aber nur charakteristische Einzelausdruecke woertlich. Diese Punkte sind als offene Pruefpunkte zu fuehren und ausdruecklich nicht als festgestellte Verstoesse.

> **Beleg:** quellenlog.md, Nachtrag mit der ausdruecklichen Folgerung zur Nichtvergebbarkeit des Grades bestaetigt. Uebereinstimmende Negativbefunde der vier Recherchebereiche zur fehlenden Auszugsebene. fehlercode_taxonomie.json: 0 von 52 Codes mit quelle_datum, 4 Codes mit offizielle_bedeutung null als vorbildliche Handhabung. scripts/validate.py: Regel-2-Warnung greift erst ab 200 Zeichen, alle betroffenen symptom_laie-Felder liegen darunter.

**Empfehlung:** Die drei Punkte im Report als Erhebungsgrenze und nicht als Aufgabe fuer den naechsten Durchlauf fuehren. Bei nachgeholtem Vollabruf jede Laienschilderung gegen das Original abgleichen und auf Paraphrase umstellen, den charakteristischen Ausdruck isoliert in Anfuehrung setzen - so, wie es in einem Fall bereits richtig gemacht wird. Die Laengenheuristik im Validator als ungeeignet kennzeichnen und stattdessen eine bewusst menschliche Pruefung in der README dokumentieren.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 22. Symptomvokabular vermischt Beobachtung, Ursachenhypothese, Befund nach Oeffnen und Kontextmarker

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `sprachbruecke.json`

**Betroffen:** kondensatablauf_verstopft, bauteil_verschlissen, absperrorgan_festsitzend, schaltgeraeusch_beim_start, frustmarker_wiederholte_reparatur, codeeingabe_zifferndreher

DATENDEFEKT, jetzt behebbar. Vier zusammengehoerige Maengel derselben Ursache. Erstens sind drei Klassen nach der vermuteten Ursache benannt statt nach der Beobachtung: bei der Kondensatklasse ist die Beobachtung ein gluckerndes Geraeusch und die Verstopfung die Deutung; die beiden anderen sind ueberhaupt keine Symptome, sondern ein Befund nach dem Oeffnen und eine weitergegebene Fremdaussage - Wissen, das erst nach der Voranalyse entsteht und dort als Eingang nicht zur Verfuegung steht. Stehen solche Klassen im Symptomvokabular, kann ein Modell sie als Ausgabe waehlen und liefert eine Ursachenbehauptung, die es nicht beobachtet hat. Zweitens kehrt die Klasse zum Schaltgeraeusch die Bedeutung ihres eigenen Belegs um: die Anmerkung haelt fest, dass im Beleg das Fehlen des Geraeusches das Auffaellige war, der Klassenname behauptet das Gegenteil - dem Feldsatz fehlt jede Moeglichkeit, eine Abwesenheitsbeobachtung auszudruecken, obwohl Laien regelmaessig beschreiben, was nicht mehr passiert. Drittens gehoeren Frustmarker und Codeeingabe-Phaenomen in ein anderes Vokabular: sie beschreiben nicht das Geraet, sondern die Schilderung beziehungsweise die Eingabe, sie fuehren zu anderen Folgen und sind zu den technischen Klassen nicht alternativ, sondern orthogonal; landet der Klassifikator dort, geht der technische Gehalt derselben Nachricht verloren. Viertens zwingt der Pflichtfeldsatz beide zu einem sinneskanal, obwohl keiner ueber einen Sinneskanal wahrgenommen wird - die Werte sind nicht ungenau, sondern falsch und verfaelschen jede spaetere Auswertung der Kanalabdeckung.

> **Beleg:** sprachbruecke.json: Eintrag zum gluckernden Geraeusch mit Klasse 'kondensatablauf_verstopft' und Anmerkung zur schwaecheren Ratgeberquelle; Eintraege zu 'bauteil_verschlissen' und 'absperrorgan_festsitzend' mit Anmerkung zur Betreiberwiedergabe; Eintrag 'klack beim Anlaufen' mit Klasse 'schaltgeraeusch_beim_start' und Anmerkung zum fehlenden Geraeusch; Frustmarker-Eintrag mit sinneskanal 'verhalten' und Anmerkung, es handele sich um kein technisches Symptom; Zifferndreher-Eintrag mit sinneskanal 'optisch'. Gegenbeleg: dieselben Sachverhalte stehen in faelle.jsonl bereits in tatsaechliche_ursache (VIE-0002, BUD-0001).

**Empfehlung:** Die Kondensatklasse in eine Beobachtungsklasse zum gluckernden Geraeusch umbenennen und die Verstopfung als gekennzeichnete Ursachenhypothese daran haengen. Die beiden Befundklassen aus dem Symptomvokabular streichen, da die Sachverhalte in den Ursachenfeldern der Faelle korrekt verortet sind. Der Geraeuschklasse ein Pflichtmerkmal auspraegung (vorhanden|fehlend) geben und den vorliegenden Beleg auf fehlend setzen; solange nicht belegt, null lassen statt einen Vorgabewert zu setzen (Regel 1). Getrennte Vokabulare fuer Kontextmarker und Eingabenormalisierung einfuehren, mit einem Feld ziel_art am Brueckeneintrag; sinneskanal dann nur noch fuer echte Symptomklassen verpflichtend, bis dahin bei den beiden Eintraegen auf null setzen. Der Frustmarker bleibt hinweisend, nie Ziel einer Diagnose und ohne Wirkung auf die Priorisierung.

**✅ Umgesetzt am 22.08.2026:** Achsen getrennt, Kondensatklasse in eine Geraeuschklasse umbenannt, sinneskanal nur fuer Leitsymptome

## 🟡 23. Symptomklasse wiederkehrende_stoerung_nach_bauteiltausch liegt auf einer anderen Achse und traegt eine Gefahrenkategorie, die ihren eigenen Mitgliedern widerspricht

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Symptomklasse wiederkehrende_stoerung_nach_bauteiltausch (VIE-0001, VIE-0002, VAI-0001, BUD-0002)

DATENDEFEKT, jetzt behebbar. VERSTAERKT: von der Taxonomie- und der Sprachbruecken-Pruefung gemeldet. Die Klasse beschreibt kein beobachtbares Symptom, sondern einen Reparaturverlauf. Sie liegt damit auf einer anderen Achse als die uebrigen fuenf und ueberlappt zwangslaeufig: alle vier ihrer Faelle stehen zugleich in einer Leitsymptomklasse, und sie ist die einzige Ursache dafuer, dass ueberhaupt Faelle mehrfach zugeordnet sind. Die sechs Klassen bilden folglich keine trennscharfe Einteilung, sondern zwei vermischte Achsen. Zusaetzlich traegt die Klasse die Gefahrenkategorie 'keine', waehrend ihre vier Mitgliedsfaelle gas, gas, wasser und gas fuehren - die Kategorie widerspricht den eigenen Mitgliedern. Die Sprachbruecke behandelt denselben Sachverhalt konsequenter, naemlich ausdruecklich als nicht technisches Symptom; gleichzeitig ist die technische Klasse ueber keine Laienschilderung erreichbar, obwohl das passende Sprachregister im Bestand vorliegt und vollstaendig auf den Frustmarker geleitet wurde. Damit wird eine technisch verwertbare Vorgeschichte als reine Stimmungsaeusserung abgelegt und die Klasse bleibt tot - und zwar ausgerechnet die Klasse, die den Kernbefund des Projekts traegt.

> **Beleg:** fehlercode_taxonomie.json: Klasse mit fall_ids ['VIE-0001','VIE-0002','VAI-0001','BUD-0002'] und gefahrenkategorie 'keine'; dieselben Faelle stehen in stoerung_nach_stillstand, stoerabschaltung_nur_bei_geschlossener_verkleidung, kein_druckanstieg_beim_pumpenstart und abgasgeruch_und_kondensataustritt. faelle.jsonl: gefahrenkategorie der vier Faelle gas, gas, wasser, gas. Validatorwarnung: Klasse hat keinen Eintrag in der Sprachbruecke.

**Empfehlung:** Aus der flachen Klassenliste herausnehmen und als eigene Achse oder als Merkmal am Fall fuehren; danach ist eine Aussage darueber moeglich, ob sich die verbleibenden Leitsymptomklassen gegenseitig ausschliessen. Die Gefahrenkategorie von der begleitenden Beobachtungsklasse erben lassen statt sie fest zu setzen. Bruecken-Eintraege ausschliesslich aus im Bestand belegtem Sprachmaterial anlegen und dabei Doppelvergabe nutzen: dieselbe Schilderung erhaelt die technische Klasse und, wo zutreffend, zusaetzlich den Kontextmarker. Keine Ausdruecke erfinden (Regel 1).

**✅ Umgesetzt am 22.08.2026:** Als eigene Achse 'fallmerkmal' gefuehrt, ueber zusatzziele erreichbar

## 🟡 24. quelle_url des Codes F.22 stuetzt den Eintrag nicht - der Beleg gehoert zu anderen Codes

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Vaillant F.22 (quelle_url)

DATENDEFEKT, jetzt behebbar. Von der Recherche-Gegenpruefung gemeldet; die adversarische Zweitpruefung hat den Befund als Fehlalarm zurueckgewiesen, dabei aber eine andere Adresse geprueft als die im Bestand hinterlegte. Ich habe den Bestand selbst nachgesehen: der F.22-Knoten traegt als quelle_url einen Forenthread, dessen Adresse auf die Fehler 75 und 72 lautet, nicht auf F.22. Derselbe Thread ist zugleich als Quelle des F.75-Knotens hinterlegt, wo er sachlich passt. Die Codebedeutung von F.22 ist davon unberuehrt und in allen gesichteten Quellen einheitlich; beanstandet wird ausschliesslich, dass der Beleg die Aussage nicht traegt. Der Befund bleibt damit stehen, die Zurueckweisung der Zweitpruefung ist auf eine Verwechslung zwischen der im Bestand gespeicherten URL und einer in der Recherche zusaetzlich genannten Adresse zurueckzufuehren. Randnotiz zur Einordnung: der Knoten steht auf gefahrenkategorie wasser, was fuer die Ursachenseite stimmt; da der Code eine Schutzfunktion an einem Gasgeraet beschreibt, sollte die Laienkommunikation dennoch der gas-Regel folgen und ohne Handlungsanweisung auskommen (Regel 6).

> **Beleg:** Eigene Nachpruefung in fehlercode_taxonomie.json: der Knoten Vaillant F.22 mit offizielle_bedeutung zum Trockenbrand fuehrt dieselbe heizungsforum-Adresse als quelle_url wie der Knoten Vaillant F.75, und diese Adresse benennt im Pfad die Fehler 75 und 72.

**Empfehlung:** quelle_url des F.22-Knotens gegen einen Beleg austauschen, der den Code tatsaechlich behandelt; die Recherche hat dafuer zwei Betriebsanleitungs-PDFs auf der Herstellerdomain als existierend bestaetigt. Eine kursierende konkrete Ausloeseschwelle in bar NICHT aufnehmen, da sie nur ueber eine maschinelle Zusammenfassung belegt ist (Regel 1). validate.py um eine Warnung erweitern, die jede in faelle.jsonl oder fehlercode_taxonomie.json verwendete Domain gegen quellenlog.md abgleicht.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 25. Eine in der Taxonomie verwendete Quelle ist im Quellenlog nicht gefuehrt

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `quellenlog.md`

**Betroffen:** quelle_url eines Buderus-Codeknotens (Domain buderuscode.de)

DATENDEFEKT, jetzt behebbar. VERSTAERKT: von der Fall- und der Taxonomie-Pruefung gemeldet, von mir durch Domainabgleich verifiziert. Ein Codeknoten stuetzt sich auf eine Domain, die in der Quellentabelle des Quellenlogs nicht auftaucht. Damit ist diese Quelle nicht nur - wie alle anderen - TDM-ungeprueft, sondern in der Liste der nachzuholenden Pruefungen gar nicht enthalten; die angekuendigte Nachholung pro Quelle wuerde sie schlicht uebersehen. Die uebrigen zehn in der Taxonomie verwendeten Domains sind vollstaendig im Log gefuehrt, das Verfahren ist also grundsaetzlich intakt - hier fehlt ein Eintrag. Nebenbefund derselben Art: das Quellenlog schreibt einer englischsprachigen Ratgeberquelle zwei Junkers-Codes zu, waehrend im Bestand nur ein Code diese URL traegt.

> **Beleg:** Eigener Abgleich aller elf in fehlercode_taxonomie.json verwendeten Hosts gegen quellenlog.md: genau ein Fehltreffer, die Domain kommt im Log nicht vor. Auszaehlung im Bestand: ein Code mit dieser Quelle; ein Code mit der englischsprachigen Ratgeberquelle gegenueber der Angabe von zwei Codes im Log.

**Empfehlung:** Eintrag im Quellenlog nachtragen mit Typ, TDM-Status ungeprueft und Ausbeute; die Abweichung bei der englischsprachigen Quelle aufloesen. validate.py um die oben genannte Domain-Abgleichpruefung erweitern, damit das Log automatisch vollstaendig bleibt.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 26. Codes ohne belegte Bedeutung tragen dennoch eine Gefahrenkategorie, eine davon aus dem Einzelfall rueckgeschlossen

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Viessmann F5 (gas), FD (gas), FE (strom), EE (gas)

DATENDEFEKT, jetzt behebbar. Fuer diese vier Codes steht offizielle_bedeutung bewusst auf null, weil die Bedeutung nicht belastbar zu belegen war - eine vorbildliche Handhabung, die die unabhaengige Recherche ausdruecklich bestaetigt hat. Gleichzeitig traegt jeder von ihnen eine gefahrenkategorie, also eine inhaltliche Aussage darueber, welches Gewerk betroffen ist, die ohne bekannte Bedeutung keine Grundlage hat. Besonders auffaellig ist der Code, dessen Einstufung auf strom sich mit der ermittelten Ursache seines einzigen zugehoerigen Falls deckt und nicht mit einer Aussage ueber den Code - damit wird aus einem Einzelfall eine Codeeigenschaft, derselbe Zirkelschluss, den der Report unter M2 als Modellrisiko beschreibt. Ein weiterer traegt eine Kategorie ohne Bedeutung und ohne verankerten Fall, also ohne jede Grundlage. Ursache ist ein Modellmangel: das Feld kennt keinen Wert fuer unbekannt, und 'keine' bedeutet etwas anderes.

> **Beleg:** fehlercode_taxonomie.json: F5, FD, FE, EE mit offizielle_bedeutung null und gefahrenkategorie gas, gas, strom, gas; FE mit unsicherheiten 'Bedeutung nicht verifiziert.' und fall_ids ['VIE-0004']; faelle.jsonl VIE-0004 nennt als Ursache einen Fehler auf der Leiterplatte. EE hat keine fall_ids und dennoch eine Kategorie.

**Empfehlung:** gefahrenkategorie nullable machen oder um den Wert unbekannt erweitern und fuer diese vier Codes so setzen. Das Regel-6-Gatter muss unbekannt konservativ wie gas behandeln, damit die Absicherung nicht schwaecher wird (Regel 8). Ableitungen von der Fallursache auf die Codeeigenschaft ausschliessen und im Modell trennen, was ueber den Code belegt ist und was nur ueber einen Fall beobachtet wurde.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 27. Codeknoten sind ohne Baureihe und ohne Datum nicht auf ein konkretes Geraet anwendbar, und eine gefuellte Baureihenliste widerspricht ihrem eigenen Fall

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** betroffene_baureihen (leer bei 36 von 52), quelle_datum (null bei 52 von 52), Buderus-Knoten '6A' gegen BUD-0002

DATENDEFEKT, jetzt behebbar. Der Bestand haelt selbst fest, dass Codebedeutungen baureihen- und reglergenerationsabhaengig sind; die unabhaengige Recherche bestaetigt das mit dem Befund, dass mindestens zwei Codesysteme desselben Herstellers nebeneinander existieren und dieselbe Codenummer je Dokumentenfamilie unterschiedlich belegt sein kann. Zugleich ist bei 36 der 52 Codes das Baureihenfeld leer und bei allen 52 das Quelldatum null. Ein leeres Baureihenfeld ist doppeldeutig: es kann heissen, der Code gelte herstellerweit, oder er sei nicht ermittelt - das Modell unterscheidet beides nicht. In Verbindung mit dem fehlenden Datum laesst sich weder pruefen, fuer welches Geraet ein Knoten gilt, noch wann seine Aussage zuletzt Bestand hatte. Dass quelle_datum durchgehend null ist, entspricht Regel 1 und ist insoweit richtig, bedeutet aber, dass eine Nachpruefungspflicht im Modell nicht abbildbar ist. Der Widerspruch beim Buderus-Oberknoten zeigt, dass das Feld auch dort, wo es gefuellt ist, nicht gegengeprueft wird: er verankert einen Fall, dessen Modellreihe nur beim Zusatzcodeknoten gelistet ist.

> **Beleg:** Eigene Auszaehlung in fehlercode_taxonomie.json: 36 von 52 Codes mit betroffene_baureihen leer, 0 von 52 mit gesetztem quelle_datum. Knoten '6A' mit betroffene_baureihen ohne GB152, aber fall_ids einschliesslich BUD-0002; faelle.jsonl BUD-0002 modellreihe 'Logamax plus GB152'. Ein Codeknoten haelt in unsicherheiten selbst fest, dass die Codes des Herstellers baureihen- und reglergenerationsabhaengig sind.

**Empfehlung:** Zwischen 'gilt herstellerweit' und 'nicht ermittelt' unterscheiden, etwa durch ein Feld geltungsbereich mit den Werten herstellerweit, baureihen, unbekannt. Ein Feld geprueft_am ergaenzen, das das eigene Pruefdatum festhaelt und damit unabhaengig vom unbekannten Beitragsdatum ist. Eine Pruefung ergaenzen, die fall.modellreihe gegen betroffene_baureihen des verankernden Knotens stellt. Die aus der Recherche stammende Empfehlung, zwei konkrete Buderus-Baureihen als unbelegt zu markieren, wird NICHT uebernommen - die Gegenpruefung hat beide in Verbindung mit dem Zusatzcode auffindbar gemacht.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 28. Kennzeichnung schwacher Einzelquellen wird uneinheitlich vergeben und taugt nicht als Filter

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** unsicherheiten von 15 der 52 Codes; markiert 2E, 040, 091 gegen unmarkiert 6A 227, 3C, F7 und die 26 Codes einer Ratgeberliste

DATENDEFEKT, jetzt behebbar. Drei Codes tragen den ausdruecklichen Hinweis, sie stammten nur aus einer Ratgeberquelle. Strukturgleiche Faelle tragen ihn nicht: der Knoten, der beide Buderus-Faelle verankert, ruht auf einer einzelnen Haendler-Wissensbasis; ein weiterer auf einem Ratgeberportal, das das Quellenlog selbst als schwach bei Einzelursachen einstuft; ein dritter auf einem englischsprachigen Ratgeberportal; und die grosse Mehrheit der Codes aus der Liste unklarer Herkunft hat unsicherheiten null. Insgesamt tragen nur 15 von 52 Codes ueberhaupt einen Zusatz. Wer den Bestand nach belastbaren Codes filtern will, kann sich auf dieses Feld daher nicht stuetzen: die Abwesenheit eines Hinweises bedeutet nicht, dass die Quellenlage traegt. Ein weiterer Mangel derselben Art: bei einem Code weicht der Bedeutungstext zwischen Fall und Codeknoten ab, weil der Fall eine Einschaetzung aus einem Forenbeitrag an den Bedeutungstext anhaengt, waehrend der Knoten sie korrekt im Unsicherheitenfeld fuehrt - die Bedeutung ist redundant in zwei Dateien gespeichert und driftet bereits auseinander, ohne dass eine Pruefung das bemerkt.

> **Beleg:** Eigene Auszaehlung: 15 von 52 Codes mit befuelltem unsicherheiten; die Codes 2E, Wolf 040 und Wolf 091 mit ausdruecklichem Einzelquellenhinweis, waehrend 6A 227, 3C und F7 unsicherheiten null tragen. faelle.jsonl VIE-0005 code_offizielle_bedeutung enthaelt zusaetzlich zur Bedeutung eine Threadbewertung, waehrend fehlercode_taxonomie.json diese beim Code E8 im Feld unsicherheiten fuehrt; bei den uebrigen sechs verankerten Paarungen stimmen die Texte ueberein.

**Empfehlung:** Die Quellenstaerke maschinell aus dem vorgeschlagenen Feld quellen.typ ableiten, statt sie von Hand in Prosa zu vermerken; unsicherheiten sollte nur noch inhaltliche Vorbehalte tragen. code_offizielle_bedeutung im Fall entweder ganz streichen und zur Anzeigezeit aus der Taxonomie ziehen oder per Pruefung auf Gleichheit mit dem Codeknoten zwingen. Quellenabhaengige Einschaetzungen ausschliesslich in unsicherheiten fuehren, nie in offizielle_bedeutung.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 29. abweichung_von_doku beschreibt eine Abweichung vom Forenverstaendnis, nicht von der Dokumentation

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0001 und VIE-0002 (abweichung_von_doku bei code_offizielle_bedeutung null)

DATENDEFEKT, jetzt behebbar. Beide Faelle fuehren code_offizielle_bedeutung als null, weil die Bedeutung der Codes nicht gegen Herstellerdokumentation verifiziert werden konnte - das ist regelkonform. Im selben Fall behaupten sie aber eine Abweichung von der Dokumentation, obwohl der Bezugspunkt ausdruecklich fehlt; der Vergleich erfolgt tatsaechlich gegen die Lesart im Forum. Ein Voranalyse-System, das diese Felder als Korrekturwissen gegen Herstellerangaben verwendet, wuerde eine Forendeutung fuer eine Herstelleraussage halten. Der Validator kennt diesen Fall bereits als Warnung, prueft ihn aber nur gegen fehlercode und nicht gegen code_offizielle_bedeutung und greift deshalb hier nicht. Bei VIE-0001 kommt eine kleine Ueberzeichnung hinzu: der Fall spricht im Plural von Fremdquellen, waehrend die Taxonomie an derselben Stelle korrekt eine einzige Fachbetriebsquelle nennt.

> **Beleg:** faelle.jsonl VIE-0001 und VIE-0002: code_offizielle_bedeutung null bei befuelltem abweichung_von_doku, das jeweils auf die Fuehrung des Codes als Feuerungsautomat-Stoerung abstellt. fehlercode_taxonomie.json, Code F5: unsicherheiten nennt eine Fachbetriebsquelle im Singular und haelt fest, das Feld sei nicht zu befuellen, bis die Serviceanleitung der Baureihe vorliegt. scripts/validate.py, Regel-1-Block, prueft nur fehlercode is None.

**Empfehlung:** Das Feld umformulieren, sodass der Bezugspunkt benannt wird - Abweichung gegenueber der im Thread verbreiteten Lesart -, oder auf null setzen, bis die Serviceanleitung vorliegt. Die Validator-Warnung erweitern: abweichung_von_doku befuellt bei code_offizielle_bedeutung null. Bei VIE-0001 den Plural auf Singular korrigieren.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 30. Unbelegte Hypothese steht in VIE-0005 als beobachtetes Symptom und wandert von dort in eine Klassendefinition

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0005 (symptom_technisch, code_offizielle_bedeutung, symptom_laie)

DATENDEFEKT, jetzt behebbar. Auf der Ursachenebene ist der Fall stimmig: tatsaechliche_ursache sagt korrekt, die Ursache sei nicht geklaert, und der Grad ist vermutung. Die Beobachtungsebene ist es nicht. symptom_technisch behauptet als beobachtetes Symptom eine Stoerung nahe der unteren Modulationsgrenze, obwohl die Laienschilderung nur von Betriebsartwechsel und einer kurzen Laufzeit spricht - die Modulationsgrenze ist die Hypothese aus dem Thread, nicht die Beobachtung, und sie wandert von dort unveraendert in die Klassenbeschreibung der Taxonomie und wird so zur Definition. Ausserdem mischt code_offizielle_bedeutung eine Forenmeinung in ein Feld, das laut Schema die dokumentierte Bedeutung traegt. Randnotiz: die Laienschilderung enthaelt zwei nicht ganz vereinbare Zeitangaben, was im Fall unkommentiert bleibt.

> **Beleg:** faelle.jsonl VIE-0005: tatsaechliche_ursache beginnt mit 'Nicht geklaert', symptom_technisch nennt die untere Modulationsgrenze, code_offizielle_bedeutung enthaelt zusaetzlich eine Bewertung aus einer Threadantwort, symptom_laie traegt beide Zeitangaben. fehlercode_taxonomie.json, Klasse 'betriebsartabhaengige_stoerung', verwendet dieselbe Formulierung zur unteren Modulationsgrenze.

**Empfehlung:** symptom_technisch auf die Beobachtung reduzieren - stoerungsfrei im Warmwasserbetrieb, Stoerung im Heizbetrieb nach kurzer Laufzeit - und die Modulationsdeutung in die Diagnoseschritte verschieben, wo sie als Pruefrichtung bereits korrekt steht. code_offizielle_bedeutung auf den Dokumentationstext kuerzen und die Threadbewertung nach unsicherheiten verschieben. Die widerspruechliche Zeitangabe in symptom_laie als offen kennzeichnen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 31. Bewertende Aussagen ueber ueber die Quell-URL identifizierbare Dritte sowie ein Firmen- und Ortsbezug in einer Quelladresse

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0002 (abweichung_von_doku), BUD-0001 (unsicherheiten), Sprachbruecken-Eintrag zum Zifferndreher, Codeknoten F5 (quelle_url)

DATENDEFEKT, jetzt behebbar. Direkte Personendaten sind nicht vorhanden: keine Namen, keine Handles, keine Kontaktdaten, keine Wohnorte; Personen erscheinen durchgaengig als Rolle, und ein Fall dokumentiert ausdruecklich, dass Angaben zum Dienstleister entfernt wurden. Zwei Restpunkte bleiben. Erstens enthaelt der Bestand bewertende Aussagen ueber Dritte, die ueber die mitgelieferte Thread-URL zuordenbar sind - mehreren Monteuren wird implizit vorgehalten, einen mit blossem Auge erkennbaren Schaden uebersehen zu haben, und einem Betreiber wird an zwei Stellen ein durchgaengiger Zifferndreher attestiert. Das sind keine Personendaten im engen Sinn, aber personenbezogene Bewertungen, und eine Wissensbasis braucht sie fuer ihren Zweck nicht. Zweitens ist die einzige Quelle eines Codeknotens die Adresse eines namentlich benannten Fachbetriebs mit Ortsangabe im Pfad. Als Quellenangabe ist das legitim und fuer die Nachpruefbarkeit noetig, aber es ist der einzige Orts- und Firmenbezug im Bestand und sollte eine bewusste Entscheidung sein, kein Nebeneffekt.

> **Beleg:** faelle.jsonl VIE-0002 abweichung_von_doku mit der Aussage zu drei vorherigen Monteuren und der laut Betreiber mit blossem Auge erkennbaren Dichtung; BUD-0001 unsicherheiten zum durchgaengigen Zifferndreher; sprachbruecke.json, Eintrag zur vertauschten Codeangabe. fehlercode_taxonomie.json, Code F5, quelle_url mit Firmenname und Stadt im Pfad. scripts/validate.py prueft nur E-Mail, Telefon, Handle und Profil-URL.

**Empfehlung:** Die Bewertungen auf den sachlichen Kern kuerzen: erfolglose Vortausche benennen, ohne die Handelnden zu bewerten. Fuer die Fachbetriebsquelle ausdruecklich entscheiden und im Quellenlog vermerken, ob die Adresse als Nachweis erhalten bleibt; nach Regel 8 spricht fuer Erhalt, dass der Codeknoten ohne sie unbelegt waere. Dass die Personendatenpruefung Firmen- und Ortsbezuege in URLs durchlaesst, ist als bekannte Luecke zu dokumentieren.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## 🟡 32. Zeitangabe zur Erfolgsmeldung im F5-Thread widerspricht dem Falldatensatz

**Schwere:** mittel &nbsp;·&nbsp; **Datei:** `report.md`

**Betroffen:** report.md Abschnitt 1, quellenlog.md Nachtrag, faelle.jsonl VIE-0001

DATENDEFEKT in der Darstellung, jetzt behebbar; die Aufloesung selbst ist eine Erhebungsgrenze. Report und Quellenlog datieren die Erfolgsmeldung im F5-Thread auf vier Wochen nach dem letzten im Suchauszug sichtbaren Beitrag, der zugehoerige Falldatensatz nennt etwa eine Woche. Die Stelle ist nicht beliebig: sie ist das einzige konkrete Beispiel, mit dem der Report seinen Hauptbefund belegt, dass Suchauszuege vor der Bestaetigung abbrechen, und sie wird im Quellenlog zur Begruendung herangezogen, dass der Grad bestaetigt in dieser Umgebung nicht vergebbar sei. Welche der beiden Angaben zutrifft, ist hier nicht klaerbar, da der Thread nicht abrufbar ist.

> **Beleg:** faelle.jsonl VIE-0001, unsicherheiten: Erfolgsmeldung nach ca. einer Woche. report.md Abschnitt 1 und quellenlog.md, Nachtrag: jeweils vier Wochen spaeter.

**Empfehlung:** Nach Regel 1 und 8 die Angabe an allen drei Stellen auf das reduzieren, was belegt ist: die Erfolgsmeldung stand in einem spaeteren Beitrag und war im Suchauszug nicht sichtbar. Eine konkrete Zeitspanne nur nennen, wenn sie am Thread nachpruefbar ist, sonst null.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## ⚪ 33. Diagnoseschritte, die einzeln stehend als Handlungsanweisung lesbar sind

**Schwere:** niedrig &nbsp;·&nbsp; **Datei:** `faelle.jsonl`

**Betroffen:** VIE-0001 diagnoseschritte[1], BUD-0001 diagnoseschritte[1]

DATENDEFEKT, jetzt behebbar. Die Diagnoseschritte des Bestands sind ueberwiegend sauber als Fachkraft-Hinweis formuliert: sie benennen, was zu bewerten oder zu pruefen ist, und nicht, was zu tun ist; die durchgaengige Praefigierung mit [Fachkraft] auch ausserhalb von gas und strom ist ein Pluspunkt. Zwei Ausnahmen. Bei VIE-0001 ist der zweite Schritt keine Diagnose, sondern eine Ausfuehrungsanweisung zur Reparatur samt Begruendung, warum die Alternative unterbleiben soll - eine Handlungsanweisung an einem gasfuehrenden Bauteil, die zudem eine unsachgemaesse Praxis ueberhaupt erst benennt. Bei BUD-0001 setzt der zweite Schritt geoeffnete Absperrungen voraus und laesst sich beim Herausloesen aus dem Kontext als Aufforderung lesen, an der Gasabsperrung zu handeln. Das Praefix aendert daran nichts, denn Diagnoseschritte werden in einer Voranalyse typischerweise einzeln ausgespielt.

> **Beleg:** faelle.jsonl VIE-0001 diagnoseschritte[1] mit dem Herstellerhinweis, die Klappe zu tauschen statt sie umzudrehen; BUD-0001 diagnoseschritte[1]: '[Fachkraft] Bei fehlendem Gaszustrom trotz geoeffneter Absperrungen den Netzbetreiber einbeziehen'. Vergleiche README.md, Abschnitt zur Konvention fuer Diagnoseschritte.

**Empfehlung:** Den VIE-0001-Schritt aus den Diagnoseschritten entfernen und als Bauteilhinweis am Teil oder im Fliesstext fuehren. Den BUD-0001-Schritt so umformulieren, dass die Pruefung der Absperrungen Teil der Feststellung ist und nicht als Voraussetzung mitschwingt. In der README ergaenzen, dass Diagnoseschritte auch einzeln stehend als Hinweis lesbar bleiben muessen (Regel 6).

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## ⚪ 34. Woertliche Uebernahme von Fremdtext in Report und Quellenlog (Regel 2)

**Schwere:** niedrig &nbsp;·&nbsp; **Datei:** `report.md`

**Betroffen:** report.md Abschnitt 1 (Zitat aus einem Forenbeitrag); quellenlog.md Ausschlusstabelle (Zitat einer Ratgeberseite)

DATENDEFEKT, jetzt behebbar. Regel 2 verlangt eigene Formulierung ohne Uebernahme von Originaltext. Der Report gibt den Abbruchpunkt des Suchauszugs als woertliches Zitat eines Forenbeitrags wieder, das Quellenlog zitiert eine Ratgeberseite woertlich einschliesslich Prozentangabe. Beides ist kurz, und im Quellenlog ist es durch den Dokumentationszweck - die Begruendung des Ausschlusses - am ehesten vertretbar; die Fallbasis selbst ist sauber, dort sind durchgaengig eigene Zusammenfassungen hinterlegt. Der Vollstaendigkeit halber vermerkt, weil die Regel keine Ausnahme fuer Belegzitate vorsieht.

> **Beleg:** report.md, Abschnitt 1, Zitat in Anfuehrungszeichen aus dem Vitodens-Thread; quellenlog.md, Ausschlusstabelle, Zeile mit vollstaendig zitiertem Satz einschliesslich Prozentangabe.

**Empfehlung:** Beide Zitate paraphrasieren, etwa dahingehend, dass der Auszug mit der Ankuendigung endete, einen Fachbetrieb einzuschalten. Alternativ eine ausdrueckliche Ausnahme fuer kurze Belegzitate in der Auftragsdokumentation festhalten und begruenden; nach Regel 8 ist die Paraphrase die konservativere Option.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## ⚪ 35. split_eval.py: die Schutzregel fuer kleine Schichten ist toter Code, und der Ausfuehrungspfad ueberschreibt das Protokoll

**Schwere:** niedrig &nbsp;·&nbsp; **Datei:** `split_eval.py`

**Betroffen:** Schichtenschleife und Schreibblock fuer split_log.md; split_log.md

DATENDEFEKT, jetzt behebbar. Die Nachrechnung bestaetigt das Protokoll: der Dry-Run mit dem dokumentierten Seed reproduziert exakt die protokollierte Ziehung, zweimal identisch. Zwei Nebenbefunde am Skript. Erstens kann die Bedingung, die kleine Schichten trotzdem im Testset vertreten soll, nie eintreten, weil die Rundung die gezogene Anzahl erst bei sehr kleinen Gruppen auf null bringt, die Bedingung aber eine groessere Mindestgruppe verlangt. Die Regel laeuft leer, und Hersteller mit ein bis zwei bestaetigten Faellen fallen dauerhaft aus dem Eval-Set. Zweitens schreibt der Ausfuehrungspfad split_log.md komplett neu und loescht damit die Begruendung, warum der Split zunaechst nicht gezogen wurde. Verbunden damit ist ein inhaltlicher Punkt: der Dry-Run zieht ausgerechnet den am schwaechsten abgesicherten der bestaetigten Faelle, dessen Codebedeutung zudem null ist. Die Entscheidung, den Split nicht auszufuehren, faengt das derzeit ab, das Problem kehrt aber bei jeder spaeteren Ziehung wieder. Regel 5 ist im Uebrigen nicht verletzbar gewesen, weil eval_set.jsonl leer ist.

> **Beleg:** Ausgefuehrter Dry-Run: gezogen wird genau ein Fall, deckungsgleich mit der Tabelle in split_log.md; Validatorausgabe 'Eval-Set: 0 Faelle', Eval-Anteil 0,0 %. Code: die Berechnung der Ziehungsanzahl gefolgt von der nie erreichbaren Mindestgruppenbedingung; spaeter ein vollstaendiges Neuschreiben von split_log.md.

**Empfehlung:** Die Bedingung auf eine erreichbare Schwelle korrigieren oder ersatzlos streichen und stattdessen dokumentieren, dass Schichten unterhalb einer benannten Groesse nicht ins Testset gelangen. Das Protokoll beim Ausfuehren anhaengen statt ueberschreiben, damit die Entscheidungshistorie erhalten bleibt. Als Kriterium festhalten, dass Faelle mit eingeschraenkter Erfolgsmeldung nicht als alleiniger Eval-Fall taugen.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

## ⚪ 36. Ein in zwei Texten referenzierter Code hat keinen Knoten in der Taxonomie

**Schwere:** niedrig &nbsp;·&nbsp; **Datei:** `fehlercode_taxonomie.json`

**Betroffen:** Viessmann-Code EE (unsicherheiten); faelle.jsonl VIE-0005 (unsicherheiten)

DATENDEFEKT, jetzt behebbar. Beide Texte stellen einen Bezug zu einem Viessmann-Code EB her, einmal als gemeinsam genannter Code, einmal als moegliche Verwechslung. Die Taxonomie fuehrt fuer diesen Hersteller nur sechs Codes, EB ist nicht darunter. Der Verweis liegt in Prosa und ist deshalb weder pruefbar noch aufloesbar; bei VIE-0005 betrifft er die Frage, ob der Fall ueberhaupt am richtigen Code haengt.

> **Beleg:** fehlercode_taxonomie.json, Code EE, unsicherheiten nennt EB und FE; faelle.jsonl VIE-0005, unsicherheiten haelt fest, dass eine Antwort im Thread von E8 oder EB spricht. Eigene Auszaehlung der Viessmann-Codes: E3, E8, F5, FD, FE, EE.

**Empfehlung:** Entweder einen Knoten mit offizielle_bedeutung null anlegen, sofern die Existenz des Codes belegt ist, oder die Nennung als das kennzeichnen, was sie ist - eine unbestaetigte Angabe aus einem Beitrag. Nichts dazwischen ergaenzen (Regel 1). Bezuege zwischen Codes gehoeren in ein Feld verwandte_codes, damit sie pruefbar werden.

**⏸ Offen** — verlangt eine Produktentscheidung oder eine andere Umgebung.

