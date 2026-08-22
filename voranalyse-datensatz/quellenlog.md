# Quellenlog

Stand: 22.08.2026. Erfasst sind die in diesem Durchlauf tatsächlich abgerufenen
Quellen. Die Liste ist nicht vollständig im Sinne von Schritt 1 – sie
dokumentiert, was gesichtet wurde, nicht was es gibt.

## ⚠ TDM-Prüfung nach §44b UrhG: NICHT durchgeführt — und hier auch nicht durchführbar

Die robots.txt und die Nutzungsbedingungen konnten in dieser Umgebung nicht
einzeln abgerufen werden. Damit ist für **keine** der unten genannten Quellen
geprüft, ob ein maschinenlesbarer Nutzungsvorbehalt gegen Text- und Data-Mining
vorliegt.

### Nachtrag 22.08.2026: Ursache gemessen, nicht vermutet

Im zweiten Durchlauf wurde geprüft, warum der Abruf scheitert. Ergebnis: Der
Egress-Proxy der Ausführungsumgebung blockiert **jeden** direkten Seitenabruf,
unabhängig von der Domain. Getestet wurden:

| Ziel | Ergebnis |
|---|---|
| `community.viessmann.de/robots.txt` | `EGRESS_BLOCKED` |
| `www.wolf.eu/robots.txt` | `EGRESS_BLOCKED` |
| `www.haustechnikdialog.de` (Thread) | `EGRESS_BLOCKED` |
| `de.wikipedia.org` (Kontrollabruf) | `EGRESS_BLOCKED` |

Der Kontrollabruf auf Wikipedia zeigt, dass es sich nicht um eine Sperre
einzelner Betreiber handelt, sondern um eine generelle Ausgangsbeschränkung.
Verfügbar ist ausschließlich die **Websuche**, die Titel, URL und Textauszug
liefert, aber keinen Seitenabruf.

**Konsequenz:** Die TDM-Prüfung ist keine offene Aufgabe, die im nächsten
Durchlauf nachgeholt werden kann — sie erfordert eine Umgebung mit freiem
HTTP-Ausgang. Solange die nicht bereitsteht, kann der Bestand nicht in ein
produktives System übernommen werden, unabhängig davon, wie viele Fälle er
enthält. Das ist die vorrangige Voraussetzung, nicht die Fallzahl.

**Zweite Konsequenz, methodisch schwerer:** Ohne Seitenabruf lässt sich eine
Lösungsbestätigung nicht feststellen. Der Suchauszug bricht regelmäßig vor der
Auflösung ab — im F5-Thread endete er bei der Ankündigung, die Firma zu
informieren, während die Erfolgsmeldung vier Wochen später kam. Der
Bestätigungsgrad `bestaetigt` ist in dieser Umgebung damit **nicht vergebbar**.
Neu erhobene Fälle können höchstens `vermutung` erreichen.

Konsequenz nach Regel 8: Der Datensatz ist als **Voruntersuchung** zu behandeln
und nicht ohne nachgeholte Prüfung in ein produktives System zu übernehmen. Die
Prüfung ist pro Quelle nachzuholen und hier mit Prüfdatum und Fundstelle
einzutragen, bevor der Bestand ausgeweitet wird.

Unabhängig davon gilt: Das Urheberrecht an Forenbeiträgen liegt beim jeweiligen
Verfasser, nicht beim Betreiber. Ein AGB-Check des Betreibers ersetzt diese
Ebene nicht. Alle Inhalte in `faelle.jsonl` sind deshalb eigene
Zusammenfassungen ohne Textübernahme.

## Genutzte Quellen

| Quelle | Typ | TDM-Status | gesichtet | verwertbare Fälle | Anmerkung |
|---|---|---|---|---|---|
| community.viessmann.de | Herstellerforum | ungeprüft | 8 Threads | 5 | Beste Quelle: markierte Lösungen, Herstellermitarbeiter, Rückmeldungen der Fragesteller |
| heizungsforum.de | Fachforum | ungeprüft | 8 Threads | 3 | Hohe technische Tiefe, Auflösung aber oft fehlend |
| bau.de | Fachforum | ungeprüft | 1 Thread | 0 | siehe Ausschlüsse |
| wolf.eu (download-asset) | Herstellerdoku | ungeprüft | 1 Dokument | – | Primärquelle für die Wolf-Codes |
| manualslib.de | Herstellerdoku (gespiegelt) | ungeprüft | 1 Seite | – | Installations-/Wartungsanleitung GB172 T, Störungssystematik |
| ersatzteile-koeln.de | Ersatzteilhändler-Wissensbasis | ungeprüft | 1 Seite | – | Buderus EMS-Codes inkl. Zusatzcodes |
| installateur-graf.at | Fachbetrieb-Ratgeber | ungeprüft | 3 Seiten | – | Codelisten Vaillant/Junkers/Wolf; Herkunft der Listen unklar |
| thermenwartung-kundendienst.at | Fachbetrieb-Ratgeber | ungeprüft | 1 Seite | – | einzige Quelle für die F5-Deutung, deshalb als unsicher markiert |
| kesselheld.de | Ratgeberportal | ungeprüft | 3 Seiten | – | brauchbar für Codesystematik, schwach bei Einzelursachen |
| freeboilermanuals.com | Ratgeberportal (EN) | ungeprüft | 1 Seite | – | nur ergänzend, für zwei Junkers-Codes |
| heizungsdiagnose.de | Ratgeberportal | ungeprüft | 1 Seite | – | zwei Wolf-Codes, sonst nicht verwendet |

## Ausgeschlossene Quellen und Inhalte

| Quelle / Inhalt | Grund |
|---|---|
| bau.de, Vitodens-200-Thread: Durchstechen der Membran des Gasströmungswächters als „Lösung" | **Sicherheitsrelevante Manipulation an einer Schutzeinrichtung.** Wird bewusst nicht als Ursache oder Maßnahme aufgenommen, auch nicht als `vermutung`. Ein Voranalyse-System darf so etwas nicht als Lösungsmuster lernen. |
| fehlercode-suche.de: „F75 ist meistens harmlos und in 80 % der Fälle selbst behebbar" | Häufigkeitsaussage ohne Datengrundlage, Regel 4. Die Seite wurde auch sonst nicht verwendet. |
| ebay.de, Ersatzteilshops (diverse) | Kein Problem-/Lösungsinhalt. Machten einen erheblichen Teil der Suchtreffer aus. |
| justanswer.de | Antworten hinter Bezahlschranke, keine überprüfbare Auflösung sichtbar. |
| fixisi.duckdns.org | Automatisch generierte Textzusammenwürfelung ohne erkennbare Quelle. |
| gutefrage.net, Usenet-Archive | Themen ohne Gerätebezug oder ohne Modellangabe. |

## Anmerkung zu den Codelisten

Vollständige Herstellertabellen wurden nicht übernommen. Einzelne Codes sind
Fakten, die Liste als Ganzes kann als Datenbank nach §87a ff. UrhG geschützt
sein. Aufgenommen wurden Codes, die einen Fall verankern, sowie Codes aus
denselben Codegruppen – alle in eigener Formulierung.
