#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nimmt die Fallkandidaten des Sammellaufs vom 22.08.2026 in den Bestand auf.

Quelle: 30 Suchzellen, davon 12 mit Ergebnis - die uebrigen 18 liefen leer, weil
das WebSearch-Kontingent der Session bei 200 Aufrufen erschoepft war.

Jeder aufgenommene Fall traegt bestaetigungsgrad "vermutung". Grund: WebFetch ist
in dieser Umgebung fuer jede Domain blockiert, es wurde also nur das Suchergebnis
ausgewertet. Eine Loesungsbestaetigung steht am Threadende und war nicht lesbar.

Aufruf:  python3 scripts/ingest_2026-08-22.py <kandidaten.json> [projektverzeichnis]
"""
import json
import re
import sys
from pathlib import Path

KAND = Path(sys.argv[1])
WURZEL = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent

PRAEFIX = {"Vaillant": "VAI", "Viessmann": "VIE", "Buderus": "BUD",
           "Junkers/Bosch": "JUN", "Wolf": "WOL"}

# --- Codenormalisierung -----------------------------------------------------
# A6 227 ist der im Bestand dokumentierte Zifferndreher von 6A 227; "Eb" und "EB"
# sind Schreibvarianten desselben Viessmann-Codes. "F.62 und F.63" ist kein
# einzelner Code, sondern eine Aufzaehlung - dafuer gibt es kein Feld (Regel 1).
CODE_NORM = {("Buderus", "A6 227"): "6A 227", ("Viessmann", "Eb"): "EB"}
CODE_VERWERFEN = {("Viessmann", "F.62 und F.63")}

# --- Symptomklassen fuer codelose Faelle ------------------------------------
REGELN = [
 (r"Wasseransammlung in der Brennkammer|Wasser in der Brennkammer", "wasser_in_der_brennkammer"),
 (r"Verpuffung|Knallger[aä]e?usch", "verpuffung_beim_abschalten"),
 (r"Umschaltvorgang|Umschaltventil", "geraeusch_beim_umschalten"),
 (r"Str[oö]mungsger[aä]e?usch|rauschend", "geraeusch_stroemung"),
 (r"Knarren|Brummen|Rattern|Ger[aä]e?uschpegel", "geraeusch_stroemung"),
 (r"gesperrte Bedienung|Bedieneinheit reagiert nicht", "bedienung_gesperrt"),
 (r"eBUS|Kommunikation|Datenaustausch gest[oö]rt|Solarmodul", "kommunikationsstoerung_regler"),
 (r"Zeitprogramm", "zeitprogramm_wird_nicht_umgesetzt"),
 (r"Takten|taktet|Kurztakt|kurze Brennerlaufzeit|Brennerlaufzeit", "takten_kurze_brennerlaufzeit"),
 (r"Dauerhafter Brennerbetrieb", "dauerbetrieb_ohne_modulation"),
 (r"Anstieg des Heizkreisdrucks|selbstt[aä]e?tig", "druckanstieg_ohne_nachspeisung"),
 (r"ohne erkennbaren Druckanstieg", "kein_druckanstieg_beim_pumpenstart"),
 (r"Druckabfall|Druckverlust|Druckabweichung|Anlagendruckverlust|Druckanzeige", "druckverlust_im_heizkreis"),
 (r"Wassermangel", "meldung_wassermangel"),
 (r"Volumenstrom", "warmwasser_zu_geringer_volumenstrom"),
 (r"Zapftemperatur|Auslauftemperatur|Temperatureinbruch|Bereitstellungszeit", "warmwasser_temperatur_schwankt"),
 (r"Warmwasser", "warmwasser_bleibt_aus"),
 (r"Vorlauftemperatur nicht|W[aä]e?rmeabgabe|Heizk[oö]e?rper|W[aä]e?rmeeintrag", "zu_geringe_waermeabgabe"),
 (r"nach der Nachtabsenkung|nach Stillstand", "stoerung_nach_stillstand"),
 (r"unmittelbar auf eine durchgef[uü]e?hrte Wartung", "stoerung_nach_wartung"),
 (r"Fr[uü]e?hausfall", "fruehausfall"),
 (r"Z[uü]e?ndausf[aä]e?lle|Z[uü]e?ndverhalten|kein Brennerstart|Startausfall|Brennerfreigabe|Z[uü]e?ndvorgang", "kein_brennerstart"),
 (r"[UÜ]e?berhitzung|Temperaturw[aä]e?chter", "uebertemperatur_abschaltung"),
 (r"Abgas[uü]e?berwachung", "stoeranzeige_zuendung"),
 (r"Gemischklappe|Gasumstellung|Umstellung der Gas|St[oö]e?rungsspeicher|ohne angezeigten Fehlercode", "stoerabschaltung"),
 (r"St[oö]e?rabschaltung|St[oö]e?rungsabschaltung|St[oö]e?rung", "stoerabschaltung"),
]

NEUE_KLASSEN = {
 "druckverlust_im_heizkreis": ("wasser", "Anlagendruck faellt wiederkehrend ab, Nachspeisung ist regelmaessig noetig."),
 "druckanstieg_ohne_nachspeisung": ("wasser", "Anlagendruck steigt selbsttaetig ueber den Sollbereich, ohne dass nachgespeist wurde."),
 "meldung_wassermangel": ("wasser", "Geraet meldet Wassermangel, ohne dass ein Fehlercode genannt wird."),
 "warmwasser_bleibt_aus": ("wasser", "Warmwasserbereitung setzt nicht ein oder bricht ab, waehrend der Heizbetrieb laeuft."),
 "warmwasser_temperatur_schwankt": ("wasser", "Zapftemperatur schwankt, faellt waehrend der Zapfung ab oder wird erst spaet erreicht."),
 "warmwasser_zu_geringer_volumenstrom": ("wasser", "Warmwasserseitiger Volumenstrom ist an allen Zapfstellen vermindert."),
 "takten_kurze_brennerlaufzeit": ("gas", "Brenner schaltet in kurzen Abstaenden ein und aus, ohne einen stabilen Modulationspunkt zu erreichen."),
 "dauerbetrieb_ohne_modulation": ("gas", "Brenner laeuft dauerhaft ohne Stoerabschaltung; Frage nach korrekter Modulation und Auslegung."),
 "geraeusch_beim_umschalten": ("wasser", "Mechanisches Geraeusch beim Umschalten zwischen Heiz- und Warmwasserbetrieb."),
 "geraeusch_stroemung": ("wasser", "Rauschendes, brummendes oder ratterndes Stroemungsgeraeusch im Betrieb."),
 "verpuffung_beim_abschalten": ("gas", "Knallgeraeusch im Moment der Brennerabschaltung."),
 "wasser_in_der_brennkammer": ("wasser", "Kondensat sammelt sich in der Brennkammer, etwa bei blockiertem Siphonschwimmer."),
 "uebertemperatur_abschaltung": ("wasser", "Sicherheitstemperaturbegrenzer oder -waechter loest wegen Uebertemperatur aus."),
 "bedienung_gesperrt": ("strom", "Bedieneinheit reagiert nicht auf Eingaben oder meldet eine gesperrte Bedienung."),
 "kommunikationsstoerung_regler": ("strom", "Datenaustausch zwischen Regler, Geraet oder Zusatzmodul ist gestoert."),
 "zeitprogramm_wird_nicht_umgesetzt": ("strom", "Eingestellte Zeitprogramme werden nicht wie erwartet ausgefuehrt."),
 "stoerung_nach_wartung": ("gas", "Stoerung tritt zeitlich unmittelbar nach einer durchgefuehrten Wartung auf."),
 "fruehausfall": ("gas", "Stoerung wenige Wochen oder Monate nach Inbetriebnahme des Geraets."),
}


def klasse_fuer(f):
    text = f["symptom_technisch"] + " " + f["symptom_laie"]
    for rx, kl in REGELN:
        if re.search(rx, text, re.I):
            return kl
    return None


def main():
    kandidaten = json.loads(KAND.read_text(encoding="utf-8"))
    faelle = [json.loads(z) for z in (WURZEL / "faelle.jsonl").read_text(encoding="utf-8").splitlines() if z.strip()]
    tax = json.loads((WURZEL / "fehlercode_taxonomie.json").read_text(encoding="utf-8"))

    bekannte_urls = {f["quelle_url"] for f in faelle}
    lfd = {}
    for f in faelle:
        p, n = f["fall_id"].split("-")
        lfd[p] = max(lfd.get(p, 0), int(n))

    protokoll = {"dublette_url": 0, "kein_leitsymptom": 0, "code_normalisiert": 0,
                 "code_verworfen": 0, "aufgenommen": 0}
    neu = []
    for k in kandidaten:
        url = k["quelle_url"]
        if url in bekannte_urls:
            protokoll["dublette_url"] += 1
            continue
        bekannte_urls.add(url)

        schluessel = (k["hersteller"], k["fehlercode"])
        code = k["fehlercode"]
        bedeutung = k["code_offizielle_bedeutung"]
        zusatz = []
        if schluessel in CODE_VERWERFEN:
            zusatz.append("Die Quelle nennt zwei Codes gemeinsam (%s); ein einzelner Code ist daraus "
                          "nicht ableitbar, das Feld bleibt leer (Regel 1)." % code)
            code, bedeutung = None, None
            protokoll["code_verworfen"] += 1
        elif schluessel in CODE_NORM:
            zusatz.append("Die Quelle schreibt den Code als '%s'; hier auf die Normalform '%s' "
                          "gebracht." % (code, CODE_NORM[schluessel]))
            code = CODE_NORM[schluessel]
            protokoll["code_normalisiert"] += 1

        klasse = None
        if not code:
            klasse = klasse_fuer(k)
            if klasse is None:
                # Ohne Code UND ohne erkennbares Leitsymptom ist der Fall fuer die
                # Voranalyse wertlos - er wird nicht aufgenommen (Regel 8).
                protokoll["kein_leitsymptom"] += 1
                continue

        p = PRAEFIX[k["hersteller"]]
        lfd[p] = lfd.get(p, 0) + 1
        fid = "%s-%04d" % (p, lfd[p])

        unsich = k["unsicherheiten"] or ""
        if zusatz:
            unsich = (unsich + " " + " ".join(zusatz)).strip()

        neu.append({
            "fall_id": fid,
            "geraeteart": "Gas-Brennwerttherme",
            "hersteller": k["hersteller"],
            "modellreihe": k["modellreihe"],
            "baujahr_hinweis": k["baujahr_hinweis"],
            "symptom_laie": k["symptom_laie"],
            "symptom_technisch": k["symptom_technisch"],
            "fehlercode": code,
            "code_offizielle_bedeutung": bedeutung if code else None,
            "tatsaechliche_ursache": k["tatsaechliche_ursache"],
            "abweichung_von_doku": k["abweichung_von_doku"] if code else None,
            "bestaetigungsgrad": "vermutung",
            "diagnoseschritte": k["diagnoseschritte"],
            "benoetigte_teile": k["benoetigte_teile"],
            "fachkraft_erforderlich": k["fachkraft_erforderlich"],
            "gefahrenkategorie": k["gefahrenkategorie"],
            "quelle_url": url,
            "quelle_datum": None,
            "unsicherheiten": unsich or None,
            "_klasse": klasse,
        })
        protokoll["aufgenommen"] += 1

    # ------------------------------------------------------------- Taxonomie --
    codes_idx = {(c["hersteller"], c["code"]): c for c in tax["codes"]}
    klassen_idx = {k["klasse"]: k for k in tax["symptomklassen"]}
    neue_codes = 0

    for f in neu:
        if f["fehlercode"]:
            s = (f["hersteller"], f["fehlercode"])
            if s not in codes_idx:
                # Die Bedeutung stammt aus einer Suchzusammenfassung. Sie wird NICHT
                # als offizielle Bedeutung gesetzt, sondern als ungesicherte Angabe
                # vermerkt - dieselbe Linie, die der erste Durchlauf fuer die
                # Viessmann-Codes gewaehlt hat und die die Recherche bestaetigt hat.
                herkunft = f["code_offizielle_bedeutung"]
                knoten = {
                    "hersteller": f["hersteller"], "code": f["fehlercode"],
                    "offizielle_bedeutung": None, "betroffene_baureihen": [],
                    "gefahrenkategorie": f["gefahrenkategorie"],
                    "quelle_url": f["quelle_url"], "quelle_datum": None,
                    "fall_ids": [], "code_typ": "basiscode", "gehoert_zu_code": None,
                    "unsicherheiten": ("Knoten aus dem Sammellauf vom 22.08.2026. Bedeutung nicht "
                                       "gegen Herstellerdokumentation verifiziert. Aus der "
                                       "Suchzusammenfassung abgeleitet und ungesichert: "
                                       + herkunft) if herkunft else
                                      ("Knoten aus dem Sammellauf vom 22.08.2026. Bedeutung nicht "
                                       "belegt."),
                }
                tax["codes"].append(knoten)
                codes_idx[s] = knoten
                neue_codes += 1
            if f["modellreihe"] and f["modellreihe"] not in codes_idx[s]["betroffene_baureihen"]:
                codes_idx[s]["betroffene_baureihen"].append(f["modellreihe"])
            codes_idx[s]["fall_ids"].append(f["fall_id"])
        else:
            kl = f["_klasse"]
            if kl not in klassen_idx:
                gefahr, beschr = NEUE_KLASSEN[kl]
                knoten = {"klasse": kl, "achse": "leitsymptom", "beschreibung": beschr,
                          "gefahrenkategorie": gefahr, "status": "aktiv", "fall_ids": [],
                          "nachfolger": [], "abgrenzung_zu": [],
                          "unsicherheiten": "Klasse aus dem Sammellauf vom 22.08.2026."}
                tax["symptomklassen"].append(knoten)
                klassen_idx[kl] = knoten
            klassen_idx[kl]["fall_ids"].append(f["fall_id"])

    for f in neu:
        del f["_klasse"]

    tax["_meta"]["codes_gesamt"] = len(tax["codes"])
    tax["_meta"]["symptomklassen_gesamt"] = len(tax["symptomklassen"])

    (WURZEL / "faelle.jsonl").write_text(
        "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in faelle + neu), encoding="utf-8")
    (WURZEL / "fehlercode_taxonomie.json").write_text(
        json.dumps(tax, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Kandidaten:              %d" % len(kandidaten))
    print("  Dublette (URL):        %d" % protokoll["dublette_url"])
    print("  ohne Leitsymptom:      %d" % protokoll["kein_leitsymptom"])
    print("  Code normalisiert:     %d" % protokoll["code_normalisiert"])
    print("  Code verworfen:        %d" % protokoll["code_verworfen"])
    print("  AUFGENOMMEN:           %d" % protokoll["aufgenommen"])
    print("Bestand jetzt:           %d Faelle" % (len(faelle) + len(neu)))
    print("Taxonomie:               %d Codes (+%d), %d Klassen"
          % (len(tax["codes"]), neue_codes, len(tax["symptomklassen"])))


if __name__ == "__main__":
    main()
