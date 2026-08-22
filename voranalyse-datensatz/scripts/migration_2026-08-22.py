#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migration aus dem Audit vom 22.08.2026.

Setzt die Befunde um, die eindeutige Datendefekte sind. Jede Aenderung ist unten
mit der Befundnummer aus report.md kommentiert. Das Skript ist idempotent: ein
zweiter Lauf auf bereits migrierten Daten aendert nichts.

Nicht umgesetzt werden Befunde, die eine Produktentscheidung verlangen - die
stehen als offene Punkte im Report.

Aufruf:  python3 scripts/migration_2026-08-22.py [projektverzeichnis]
"""
import json
import sys
from pathlib import Path

WURZEL = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
aenderungen = []


def notiere(t):
    aenderungen.append(t)


# =============================================================== faelle.jsonl
faelle = [json.loads(z) for z in (WURZEL / "faelle.jsonl").read_text(encoding="utf-8").splitlines() if z.strip()]
nach_id = {f["fall_id"]: f for f in faelle}

# --- Befund 3: Sicherheitsinversion BUD-0002 --------------------------------
# Das Ausbleiben der verriegelnden Stoerung nach Nachstecken an der
# Ionisationssonde wurde als Besserung gelesen. Die Ionisationssonde IST die
# Flammenueberwachung; ein Ausbleiben ihrer Schutzabschaltung kann ebenso den
# Verlust der Schutzwirkung bedeuten. Die Betreiberdeutung wird als
# Diagnoserichtung entfernt und durch den Gegenhinweis ersetzt.
b = nach_id["BUD-0002"]
neue_ursache = (
    "Nicht abschliessend geklaert. Ein gerissener Kondensatsammler am "
    "Waermetauscheranschluss wurde gefunden und ersetzt - das beseitigte Geruch und "
    "Kondensataustritt, die Stoerung 6A 227 blieb jedoch bestehen. Separat beobachtet: "
    "nach mehrfachem Stecken der Sensorleitung der Ionisationssonde trat der Fehler "
    "seltener und nicht mehr verriegelnd auf. Diese Beobachtung wird ausdruecklich NICHT "
    "als Besserung gewertet: die Ionisationssonde ist die Flammenueberwachung, das "
    "Ausbleiben ihrer verriegelnden Abschaltung kann auch den Verlust der Schutzwirkung "
    "bedeuten."
)
if b["tatsaechliche_ursache"] != neue_ursache:
    b["tatsaechliche_ursache"] = neue_ursache
    notiere("BUD-0002 tatsaechliche_ursache: Betreiberdeutung als Besserung entfernt, Gegenhinweis ergaenzt (Befund 3)")

neue_schritte = [
    "[Fachkraft] Abgasgeruch ist vor jeder weiteren Diagnose als Sofortlage zu behandeln",
    "[Fachkraft] Kondensatsammler und dessen Anschluss am Waermetauscher auf Risse pruefen",
    "[Fachkraft] Ein Ausbleiben der verriegelnden Stoerung nach Eingriff an der Ionisationssonde "
    "nicht als Erfolg werten - Funktion der Flammenueberwachung eigenstaendig nachweisen",
]
if b["diagnoseschritte"] != neue_schritte:
    b["diagnoseschritte"] = neue_schritte
    notiere("BUD-0002 diagnoseschritte: Kontaktfehler-Richtung gestrichen, Eskalation und Gegenpruefung ergaenzt (Befund 3)")

# --- Befund 4: benoetigte_teile nennt Teile, die nichts behoben haben -------
# Feldsemantik: nur Teile, deren Austausch die Stoerung nachweislich behoben hat.
for fid, alt in (("VAI-0001", ["Wasserdrucksensor"]), ("BUD-0002", ["Kondensatsammler/Siphon"])):
    if nach_id[fid]["benoetigte_teile"] == alt:
        nach_id[fid]["benoetigte_teile"] = []
        notiere("%s benoetigte_teile geleert - die genannten Teile haben den Fehler laut Falltext "
                "nicht behoben (Befund 4)" % fid)

# --- Befund 5: Bestaetigungsgrad nicht durch die Beleglage gedeckt ----------
# VIE-0001: Erfolg nur im Warmwasserbetrieb belegt, waehrend das Leitsymptom das
# Umschalten betrifft; Beobachtung ca. eine Woche bei einem Fehler nach
# Stillstandsphasen; drei Vortausche konfundieren die Kausalitaet.
if nach_id["VIE-0001"]["bestaetigungsgrad"] == "bestaetigt":
    nach_id["VIE-0001"]["bestaetigungsgrad"] = "vermutung"
    nach_id["VIE-0001"]["tatsaechliche_ursache"] = (
        "Nach Austausch der Gemischklappe trat der Fehler im Warmwasserbetrieb nicht mehr auf. "
        "Der Monteur konnte optisch keinen Unterschied zwischen alter und neuer Klappe erkennen; "
        "ein Defekt der Klappe ist damit die naechstliegende, aber nicht nachgewiesene Erklaerung."
    )
    notiere("VIE-0001 bestaetigungsgrad bestaetigt -> vermutung; Ursache von der Faktenbehauptung "
            "auf die Beobachtung zurueckgenommen (Befund 5)")

# VIE-0003: fremde Anekdote im Thread eines anderen, ohne Code, ohne Baujahr,
# ohne eigene Schilderung. Die Phasenzuordnung war aus dem Kontext aufgefuellt.
if nach_id["VIE-0003"]["bestaetigungsgrad"] == "bestaetigt":
    nach_id["VIE-0003"]["bestaetigungsgrad"] = "vermutung"
    nach_id["VIE-0003"]["symptom_technisch"] = (
        "Stoerabschaltung ausschliesslich bei geschlossener Geraeteverkleidung; "
        "Fehlerphase im Beitrag nicht genannt"
    )
    notiere("VIE-0003 bestaetigungsgrad bestaetigt -> vermutung; symptom_technisch auf das Belegte "
            "reduziert, unbelegte Phasenzuordnung gestrichen (Befund 5, Regel 1)")

# --- Befund 8: zeitliche Unmoeglichkeit ------------------------------------
# VIE-0003 antwortet im Thread von VIE-0002, ist aber zehn Tage frueher datiert.
# Mindestens ein Datum stammt nicht aus dem Beitrag. Report-Linie: Indexdatum ist
# kein Beitragsdatum -> beide auf null.
for fid in ("VIE-0002", "VIE-0003"):
    if nach_id[fid]["quelle_datum"] is not None:
        nach_id[fid]["quelle_datum"] = None
        notiere("%s quelle_datum auf null - Antwortbeitrag war vor dem Thread datiert, "
                "Datum nicht am Beitrag verifizierbar (Befund 8, Regel 1)" % fid)

(WURZEL / "faelle.jsonl").write_text(
    "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in faelle), encoding="utf-8")

print("faelle.jsonl: %d Datensaetze geschrieben" % len(faelle))
for a in aenderungen:
    print("  -", a)


# ==================================================== fehlercode_taxonomie.json
tax = json.loads((WURZEL / "fehlercode_taxonomie.json").read_text(encoding="utf-8"))
tax_aenderungen = []

# --- Befund 12: Codehierarchie 6A / 6A 227 ---------------------------------
# Die Hierarchie ist sachlich real, wurde aber von keinem Feld ausgedrueckt und
# stattdessen durch doppelte fall_ids nachgebildet. Faelle haengen kuenftig nur
# am spezifischsten Knoten; die Zuordnung zum Oberknoten folgt aus gehoert_zu_code.
for c in tax["codes"]:
    c.setdefault("code_typ", "basiscode")
    c.setdefault("gehoert_zu_code", None)

for c in tax["codes"]:
    if c["hersteller"] == "Buderus" and c["code"] == "6A 227":
        if c["code_typ"] != "zusatzcode":
            c["code_typ"] = "zusatzcode"
            c["gehoert_zu_code"] = "6A"
            tax_aenderungen.append("Buderus 6A 227 als zusatzcode von 6A ausgewiesen (Befund 12)")
    if c["hersteller"] == "Buderus" and c["code"] == "6A" and c["fall_ids"]:
        c["fall_ids"] = []
        tax_aenderungen.append("Buderus 6A: fall_ids geleert - Faelle haengen am spezifischeren "
                               "Knoten 6A 227, Zuordnung folgt aus gehoert_zu_code (Befund 12)")

# --- Befund 2, 7, 22, 23: Vokabular konsolidieren ---------------------------
# Bisher lagen Leitsymptome, ein Fallmerkmal, Kontextmarker und Befundsprache in
# einer flachen Liste, und 14 von der Sprachbruecke benutzte Klassen fehlten ganz.
# Neu: EINE Liste, ein Feld 'achse' trennt die Ebenen. Die Kombiklasse
# abgasgeruch_und_kondensataustritt wird zugunsten der Einzelklassen abgeloest,
# weil Mehrfachvergabe die Kombination verlustfrei nachbildet, der umgekehrte Weg
# aber Information vernichtet - und weil die Geruchsschilderung allein feuern muss.
def K(klasse, achse, beschreibung, gefahr, fall_ids=None, **rest):
    e = {"klasse": klasse, "achse": achse, "beschreibung": beschreibung,
         "gefahrenkategorie": gefahr, "status": "aktiv",
         "fall_ids": fall_ids or [], "nachfolger": [], "abgrenzung_zu": [],
         "unsicherheiten": None}
    e.update(rest)
    return e

klassen = [
    K("stoerabschaltung", "leitsymptom",
      "Geraet schaltet auf Stoerung ab. Oberklasse ohne Festlegung auf eine Fehlerphase; "
      "zu verwenden, solange die Schilderung keine engere Klasse hergibt.", "gas",
      abgrenzung_zu=["kein_brennerstart", "flammverlust_im_betrieb"]),
    K("kein_brennerstart", "leitsymptom",
      "Brenner zuendet nicht, das Geraet erreicht den Betrieb gar nicht erst.", "gas"),
    K("flammverlust_im_betrieb", "leitsymptom",
      "Geraet laeuft an und faellt nach einer Betriebsphase aus.", "gas"),
    K("stoerabschaltung_nur_bei_geschlossener_verkleidung", "leitsymptom",
      "Geraet laeuft mit abgenommener Haube stoerungsfrei und stoert bei montierter Haube. "
      "Zeigt auf Undichtigkeit mit Abgasrezirkulation, nicht auf den Feuerungsautomaten.", "gas",
      ["VIE-0002", "VIE-0003"]),
    K("betriebsartabhaengige_stoerung", "leitsymptom",
      "Stoerungsfreier Warmwasserbetrieb bei hoher Last, Stoerung im Heizbetrieb nahe der unteren "
      "Modulationsgrenze. Richtungsmerkmal: die stoerungsfreie Betriebsart ist die mit der "
      "HOEHEREN Leistungsanforderung. Faelle mit umgekehrter Richtung gehoeren nicht hierher.",
      "gas", ["VIE-0005"], abgrenzung_zu=["stoerabschaltung"]),
    K("stoerung_nach_stillstand", "leitsymptom",
      "Stoerung gehaeuft beim ersten Start nach laengerem Stillstand, etwa morgens oder nach "
      "Nachtabsenkung.", "gas", ["VIE-0001"]),
    K("stoerung_nur_temporaer_quittierbar", "leitsymptom",
      "Nach Reset laeuft das Geraet nur kurz und stoert erneut.", "gas"),
    K("stoeranzeige_zuendung", "leitsymptom",
      "Displayanzeige, die auf einen Zuendfehler deutet, ohne dass der Nutzer einen Code nennt.",
      "gas"),
    K("abgasgeruch", "leitsymptom",
      "Wahrnehmbarer Abgasgeruch am oder um das Geraet.", "gas", ["BUD-0002"]),
    K("kondensataustritt", "leitsymptom",
      "Sichtbar austretendes Kondensat am Geraet.", "wasser", ["BUD-0002"]),
    K("geraeusch_gluckern", "leitsymptom",
      "Gluckerndes oder blubberndes Geraeusch am Geraet.", "wasser",
      ursachenhypothesen=["kondensatablauf verstopft"]),
    K("geraeusch_schalten_beim_start", "leitsymptom",
      "Schaltgeraeusch beim Anlaufen. Die Auspraegung ist Teil der Beobachtung: auffaellig kann "
      "sowohl das Vorhandensein als auch das FEHLEN des Geraeusches sein.", "gas",
      auspraegung=None),
    K("zu_geringe_waermeabgabe", "leitsymptom",
      "Heizkoerper werden nicht oder nur lauwarm, ohne dass eine Stoerung angezeigt wird.",
      "wasser"),
    K("kein_druckanstieg_beim_pumpenstart", "leitsymptom",
      "Anlagendruck im zulaessigen Bereich, aber beim Pumpenstart bleibt der erwartete "
      "Druckanstieg aus.", "wasser", ["VAI-0001"]),

    # abgeloest - bleibt als Spur erhalten, damit die Aenderung nachvollziehbar ist
    dict(klasse="abgasgeruch_und_kondensataustritt", achse="leitsymptom",
         beschreibung="Kombiklasse, die beide Merkmale gleichzeitig verlangte. Abgeloest zugunsten "
                      "der Einzelklassen; ein Fall mit beiden Merkmalen traegt kuenftig beide.",
         gefahrenkategorie="gas", status="abgeloest", fall_ids=[],
         nachfolger=["abgasgeruch", "kondensataustritt"], abgrenzung_zu=[],
         unsicherheiten="Am 22.08.2026 abgeloest (Befund 7). Ankerfall BUD-0002 traegt jetzt beide "
                        "Nachfolgeklassen."),

    # andere Achsen
    K("wiederkehrende_stoerung_nach_bauteiltausch", "fallmerkmal",
      "Mehrere Bauteile bereits ersetzt, Stoerung besteht fort. Kein Leitsymptom, sondern ein "
      "Merkmal des Fallverlaufs: Hinweis darauf, dass die bisherige Diagnose der Codebedeutung "
      "gefolgt ist statt dem Leitsymptom.", "keine",
      ["VIE-0001", "VIE-0002", "VAI-0001", "BUD-0002"]),
    K("frustmarker_wiederholte_reparatur", "kontextmarker",
      "Kein technisches Symptom. Signalisiert eine Vorgeschichte erfolgloser Reparaturen. Nie Ziel "
      "einer Diagnose und ohne Wirkung auf die Priorisierung.", "keine"),
    K("codeeingabe_zifferndreher", "eingabenormalisierung",
      "Kein Symptom, sondern eine Eingabeform: der Nutzer gibt einen Fehlercode vertauscht oder in "
      "abweichender Schreibweise an. Fuer die Normalisierung der Codeerkennung.", "keine"),
    K("bauteil_verschlissen", "befundsprache",
      "Kein Symptom, sondern ein Befund nach dem Oeffnen des Geraets. Sprachmaterial fuer die "
      "Fachkraftseite, nicht fuer die Laieneingabe.", "keine"),
    K("absperrorgan_festsitzend", "befundsprache",
      "Kein Symptom, sondern ein Befund nach Pruefung der Gasstrecke. Sprachmaterial fuer die "
      "Fachkraftseite, nicht fuer die Laieneingabe.", "keine"),
]

if [k["klasse"] for k in tax["symptomklassen"]] != [k["klasse"] for k in klassen]:
    alt_n = len(tax["symptomklassen"])
    tax["symptomklassen"] = klassen
    tax_aenderungen.append(
        "symptomklassen von %d auf %d Eintraege konsolidiert, Achsentrennung eingefuehrt "
        "(leitsymptom / fallmerkmal / kontextmarker / eingabenormalisierung / befundsprache); "
        "BUD-0001 aus betriebsartabhaengige_stoerung entfernt (Befunde 2, 7, 10, 22, 23)"
        % (alt_n, len(klassen)))

tax["_meta"]["codes_gesamt"] = len(tax["codes"])
tax["_meta"]["symptomklassen_gesamt"] = len(tax["symptomklassen"])
tax["_meta"]["stand"] = "2026-08-22"
tax["_meta"]["achsen"] = {
    "leitsymptom": "Beobachtbares Symptom, Ziel der Laieneingabe.",
    "fallmerkmal": "Merkmal des Fallverlaufs, kein Symptom.",
    "kontextmarker": "Nicht-technischer Hinweis aus der Schilderung.",
    "eingabenormalisierung": "Form der Nutzereingabe, kein Symptom.",
    "befundsprache": "Formulierung fuer einen Befund nach dem Oeffnen, Fachkraftseite.",
}

(WURZEL / "fehlercode_taxonomie.json").write_text(
    json.dumps(tax, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\nfehlercode_taxonomie.json: %d Codes, %d Klassen" % (len(tax["codes"]), len(tax["symptomklassen"])))
for a in tax_aenderungen:
    print("  -", a)


# ========================================================== sprachbruecke.json
sb = json.loads((WURZEL / "sprachbruecke.json").read_text(encoding="utf-8"))
sb_aenderungen = []

achse_je_klasse = {k["klasse"]: k["achse"] for k in tax["symptomklassen"]}
gefahr_je_klasse = {k["klasse"]: k["gefahrenkategorie"] for k in tax["symptomklassen"]}

# Umhaengen auf das konsolidierte Vokabular. Links: bisheriger Zielname,
# rechts: Zielname nach der Konsolidierung. Nur dort abweichend, wo eine Klasse
# umbenannt wurde (Befund 22).
UMHAENGEN = {
    "kondensatablauf_verstopft": "geraeusch_gluckern",
    "schaltgeraeusch_beim_start": "geraeusch_schalten_beim_start",
}

# Zusatzziele auf anderen Achsen (Befund 23): dieselbe Schilderung darf zugleich
# ein Fallmerkmal treffen. Nur aus im Bestand belegtem Sprachmaterial.
ZUSATZZIELE = {
    "Fass ohne Boden": ["wiederkehrende_stoerung_nach_bauteiltausch"],
}

for e in sb["eintraege"]:
    ziel = UMHAENGEN.get(e["symptomklasse"], e["symptomklasse"])
    if ziel != e["symptomklasse"]:
        sb_aenderungen.append("'%s': Ziel %s -> %s (Befund 22)" % (e["ausdruck"], e["symptomklasse"], ziel))
        e["symptomklasse"] = ziel

    e["ziel_art"] = achse_je_klasse.get(ziel)
    # Gefahrenkategorie wird von der Zielklasse geerbt, nicht am Eintrag gepflegt
    e["gefahrenkategorie"] = gefahr_je_klasse.get(ziel)
    e["zusatzziele"] = ZUSATZZIELE.get(e["ausdruck"], [])
    # sinneskanal ist nur fuer echte Leitsymptome sinnvoll (Befund 22)
    if e["ziel_art"] != "leitsymptom" and e.get("sinneskanal") is not None:
        sb_aenderungen.append("'%s': sinneskanal auf null - Ziel liegt auf der Achse '%s', "
                              "nicht auf einem Leitsymptom (Befund 22)" % (e["ausdruck"], e["ziel_art"]))
        e["sinneskanal"] = None

# Befund 10: Die Anmerkung behauptete eine Ursache statt auf Mehrdeutigkeit hinzuweisen.
for e in sb["eintraege"]:
    if e["ausdruck"] == "Warmwasser geht, Heizung nicht":
        neu = ("Mehrdeutig. Trifft die Klasse nur, wenn die stoerungsfreie Betriebsart die mit der "
               "hoeheren Leistungsanforderung ist. Die umgekehrte Richtung - Warmwasser faellt aus, "
               "Heizung laeuft - gehoert nicht hierher.")
        if e.get("anmerkung") != neu:
            e["anmerkung"] = neu
            sb_aenderungen.append("'Warmwasser geht, Heizung nicht': Anmerkung von der "
                                  "Ursachenbehauptung auf einen Mehrdeutigkeitshinweis umgestellt (Befund 10)")

sb["_meta"]["stand"] = "2026-08-22"
sb["_meta"]["eintraege_gesamt"] = len(sb["eintraege"])
sb["_meta"]["ziel_art"] = ("Achse der Zielklasse in fehlercode_taxonomie.json. Nur ziel_art="
                           "'leitsymptom' ist Ziel einer Laieneingabe; die uebrigen Achsen dienen "
                           "der Normalisierung, der Kontextauswertung oder der Fachkraftseite.")
sb["_meta"]["gefahrenkategorie"] = ("Von der Zielklasse geerbt, nicht am Eintrag gepflegt. Laesst "
                                    "sich kein Ziel aufloesen, ist konservativ wie 'gas' zu "
                                    "verfahren (Regel 8).")

(WURZEL / "sprachbruecke.json").write_text(
    json.dumps(sb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\nsprachbruecke.json: %d Eintraege" % len(sb["eintraege"]))
for a in sb_aenderungen:
    print("  -", a)
verteilung = {}
for e in sb["eintraege"]:
    verteilung[e["ziel_art"]] = verteilung.get(e["ziel_art"], 0) + 1
print("  Verteilung nach ziel_art:", verteilung)
