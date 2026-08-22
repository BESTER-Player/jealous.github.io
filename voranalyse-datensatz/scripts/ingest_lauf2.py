#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nimmt die Fallkandidaten des zweiten Sammellaufs vom 22.08.2026 auf.

Quelle: die 18 Suchzellen, die im ersten Sammellauf am erschoepften Suchbudget
gescheitert waren. 235 Kandidaten, davon 95 in einer adversarischen
Offline-Gegenpruefung verworfen; 130 bleiben.

Wie im ersten Lauf traegt jeder Fall bestaetigungsgrad "vermutung" - WebFetch ist
blockiert, ausgewertet wurde nur das Suchergebnis.

Aufruf: python3 scripts/ingest_lauf2.py <kandidaten.json> [projektverzeichnis]
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
# Die Agenten liefern teils Aufzaehlungen ("6A / 6L", "004 und 061") oder Codes mit
# Klammerzusatz. Eine Aufzaehlung ist kein Code: das Feld bleibt leer und die Angabe
# wandert nach unsicherheiten (Regel 1). Buderus-Basiscode plus dreistelligem
# Zusatzcode ist dagegen eine echte Hierarchie und wird zusammengefuehrt.
def norm_code(h, c):
    if not c:
        return None, None
    roh = c
    c = re.sub(r"\s*\([^)]*\)", "", c).strip()
    c = re.sub(r"\s*[:,]\s*$", "", c).strip()
    if re.search(r"\bund\b|;|,", c):
        return None, ("Die Quelle nennt mehrere Codes gemeinsam (%s); eine einzelne "
                      "Codeangabe ist daraus nicht ableitbar (Regel 1)." % roh)
    m = re.match(r"^([A-Za-z0-9]{1,3})\s*/\s*([A-Za-z0-9]{1,4})$", c)
    if m:
        a, b = m.group(1), m.group(2)
        if b.isdigit() and len(b) >= 3:
            return "%s %s" % (a.upper(), b), None
        if {a.upper(), b.upper()} == {"H7", "H07"}:
            return "H07", "Die Quelle nennt beide Schreibweisen (%s)." % roh
        return None, ("Die Quelle nennt zwei Codes zugleich (%s); keine einzelne "
                      "Codeangabe ableitbar (Regel 1)." % roh)
    if h == "Wolf" and c.isdigit():
        return c.zfill(3), (None if len(c) == 3 else
                            "Die Quelle schreibt den Code als '%s'; auf die dreistellige "
                            "Normalform gebracht." % roh)
    return c, ("Die Quelle schreibt den Code als '%s'." % roh) if c != roh else None


# Eine aus der Suchzusammenfassung abgeleitete Bedeutung ist keine offizielle
# Bedeutung. Traegt der Text selbst einen Herkunftsvorbehalt, wandert er nach
# unsicherheiten und das Feld wird geleert - dieselbe Linie wie bei den
# Taxonomieknoten.
VORBEHALT = re.compile(r"Zusammenfassung|nicht belegt|nicht gepr[uü]e?ft|Titel|ungesichert|"
                       r"nicht eingesehen|nicht verifiziert", re.I)

# --- Symptomklassen ---------------------------------------------------------
REGELN_NEU = [
 (r"Gasgeruch", "gasgeruch"),
 (r"W[aä]e?rmetauscherschaden", "waermetauscherschaden"),
 (r"Rissbildung|Abgasstutzen|abgasf[uü]e?hrenden Bereich", "abgasweg_undicht"),
 (r"Wasseraustritt am Ger[aä]e?t|W[aä]e?rmetauscherundichtheit", "wasseraustritt_am_geraet"),
 (r"Manometeranzeige|digital angezeigtem Anlagendruck", "druckanzeige_weicht_ab"),
 (r"erh[oö]e?htem Anlagendruck|4,0 bar|[UÜ]e?berdruck", "ueberdruck_abschaltung"),
 (r"Modulation", "modulation_untere_grenze"),
 (r"Pfeifton|pfeifend|sirenenartig", "geraeusch_pfeifen"),
 (r"Polter|Schlagger[aä]e?usch", "geraeusch_poltern_schlagen"),
 (r"R[oö]e?hren|Dr[oö]e?hnen|schnaufend|pulsierend", "geraeusch_droehnen"),
 (r"K[oö]e?rperschall|Kaltwasserzuleitung", "geraeusch_kaltwasserleitung"),
 (r"ohne Anzeige|Keine Anzeige|Displayanzeige ohne Funktion|ohne Funktion",
  "display_ohne_funktion"),
 (r"Zwei Fehlercodes", "mehrere_codes_gleichzeitig"),
 (r"[UÜ]e?bertemperatur|Temperaturbegrenzer", "uebertemperatur_abschaltung"),
 (r"Fl[uü]e?ssiggas|Gasumstellung|Umstellung der Gas", "stoerung_nach_gasumstellung"),
 (r"Ausbleibender (Ger[aä]e?te-?/?)?(Brenner)?start|Kein Anlauf|"
  r"Totalausfall der W[aä]e?rmeerzeugung|Ger[aä]e?teausfall", "kein_brennerstart"),
 (r"Raumsolltemperatur|Vorlauftemperatur|hydraulischen Weiche", "zu_geringe_waermeabgabe"),
]

NEUE_KLASSEN = {
 "gasgeruch": ("gas", "Wahrnehmbarer Gasgeruch am oder um das Geraet. Abzugrenzen von Abgasgeruch: "
                      "Gasgeruch weist auf unverbranntes Brenngas hin und ist die dringlichere Lage."),
 "waermetauscherschaden": ("wasser", "Schaden am Waermetauscher, teils wiederholt am selben Geraet."),
 "abgasweg_undicht": ("gas", "Undichtigkeit im abgasfuehrenden Bereich, etwa Risse am Abgasstutzen "
                             "oder an angrenzenden Blechteilen."),
 "wasseraustritt_am_geraet": ("wasser", "Wasser tritt am Geraet aus, ohne dass eine Kondensatspur "
                                        "erkennbar ist."),
 "druckanzeige_weicht_ab": ("wasser", "Analoge und digitale Druckanzeige zeigen unterschiedliche "
                                      "Werte; welcher stimmt, ist offen."),
 "ueberdruck_abschaltung": ("wasser", "Abschaltung wegen deutlich zu hohem Anlagendruck."),
 "modulation_untere_grenze": ("gas", "Geraet moduliert nicht bis zur erwarteten unteren Grenze "
                                     "herunter oder verhaelt sich am Lastpunkt auffaellig."),
 "geraeusch_pfeifen": ("gas", "Pfeifender oder sirenenartiger Ton im Betrieb."),
 "geraeusch_poltern_schlagen": ("wasser", "Polternde oder schlagende Geraeusche, meist bei Aufnahme "
                                          "des Heizbetriebs."),
 "geraeusch_droehnen": ("gas", "Roehrendes, droehnendes oder pulsierend schnaufendes "
                               "Betriebsgeraeusch."),
 "geraeusch_kaltwasserleitung": ("wasser", "Stroemungs- oder Koerperschallgeraeusch an der "
                                           "Kaltwasserzuleitung."),
 "display_ohne_funktion": ("strom", "Display oder Bedienmodul bleibt dunkel und ohne Funktion; ein "
                                    "Stoercode ist deshalb nicht ablesbar."),
 "mehrere_codes_gleichzeitig": ("gas", "Das Geraet zeigt zwei oder mehr Codes zugleich; welcher der "
                                       "fuehrende ist, geht aus der Schilderung nicht hervor."),
 "stoerung_nach_gasumstellung": ("gas", "Stoerungen treten erst seit einer Umstellung der Gasart "
                                        "oder seit Fluessiggasbetrieb auf."),
}


def lade_bestandsregeln():
    src = (Path(__file__).parent / "ingest_2026-08-22.py").read_text(encoding="utf-8")
    blk = src[src.index("REGELN = ["):src.index("NEUE_KLASSEN")]
    ns = {"re": re}
    exec(blk, ns)
    return ns["REGELN"]


REGELN = REGELN_NEU + lade_bestandsregeln()


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
    alle_klassen = {k["klasse"]: k for k in tax["symptomklassen"]}

    bekannte_urls = {f["quelle_url"] for f in faelle}
    lfd = {}
    for f in faelle:
        p, n = f["fall_id"].split("-")
        lfd[p] = max(lfd.get(p, 0), int(n))

    prot = {"dublette": 0, "kein_leitsymptom": 0, "code_normalisiert": 0,
            "code_entwertet": 0, "bedeutung_entwertet": 0, "aufgenommen": 0}
    neu = []
    for k in kandidaten:
        url = k["quelle_url"]
        if url in bekannte_urls:
            prot["dublette"] += 1
            continue
        bekannte_urls.add(url)

        zusatz = []
        code, hinweis = norm_code(k["hersteller"], k["fehlercode"])
        if hinweis:
            zusatz.append(hinweis)
        if k["fehlercode"] and code is None:
            prot["code_entwertet"] += 1
        elif k["fehlercode"] and code != k["fehlercode"]:
            prot["code_normalisiert"] += 1

        bedeutung = k["code_offizielle_bedeutung"] if code else None
        if bedeutung and VORBEHALT.search(bedeutung):
            zusatz.append("Zur Codebedeutung lag nur eine Angabe aus dem Suchergebnis vor, "
                          "nicht aus der Herstellerdokumentation: " + bedeutung)
            bedeutung = None
            prot["bedeutung_entwertet"] += 1

        klasse = None
        if not code:
            klasse = klasse_fuer(k)
            if klasse is None:
                prot["kein_leitsymptom"] += 1
                continue

        p = PRAEFIX[k["hersteller"]]
        lfd[p] = lfd.get(p, 0) + 1
        fid = "%s-%04d" % (p, lfd[p])
        unsich = ((k["unsicherheiten"] or "") + " " + " ".join(zusatz)).strip()

        neu.append({
            "fall_id": fid, "geraeteart": "Gas-Brennwerttherme",
            "hersteller": k["hersteller"], "modellreihe": k["modellreihe"],
            "baujahr_hinweis": k["baujahr_hinweis"],
            "symptom_laie": k["symptom_laie"], "symptom_technisch": k["symptom_technisch"],
            "fehlercode": code, "code_offizielle_bedeutung": bedeutung,
            "tatsaechliche_ursache": k["tatsaechliche_ursache"],
            "abweichung_von_doku": k["abweichung_von_doku"] if code else None,
            "bestaetigungsgrad": "vermutung",
            "diagnoseschritte": k["diagnoseschritte"], "benoetigte_teile": k["benoetigte_teile"],
            "fachkraft_erforderlich": k["fachkraft_erforderlich"],
            "gefahrenkategorie": k["gefahrenkategorie"], "quelle_url": url,
            "quelle_datum": None, "unsicherheiten": unsich or None, "_klasse": klasse,
        })
        prot["aufgenommen"] += 1

    # ------------------------------------------------------------- Taxonomie --
    codes_idx = {(c["hersteller"], c["code"]): c for c in tax["codes"]}
    neue_codes = neue_klassen = 0
    for f in neu:
        if f["fehlercode"]:
            s = (f["hersteller"], f["fehlercode"])
            if s not in codes_idx:
                knoten = {"hersteller": f["hersteller"], "code": f["fehlercode"],
                          "offizielle_bedeutung": None, "betroffene_baureihen": [],
                          "gefahrenkategorie": f["gefahrenkategorie"],
                          "quelle_url": f["quelle_url"], "quelle_datum": None, "fall_ids": [],
                          "code_typ": "basiscode", "gehoert_zu_code": None,
                          "unsicherheiten": "Knoten aus dem zweiten Sammellauf vom 22.08.2026. "
                                            "Bedeutung nicht gegen Herstellerdokumentation "
                                            "verifiziert."}
                m = re.match(r"^([A-Za-z0-9]{1,3}) (\d{3})$", f["fehlercode"])
                if m:
                    knoten["code_typ"] = "zusatzcode"
                    knoten["gehoert_zu_code"] = m.group(1)
                tax["codes"].append(knoten)
                codes_idx[s] = knoten
                neue_codes += 1
            if f["modellreihe"] not in codes_idx[s]["betroffene_baureihen"]:
                codes_idx[s]["betroffene_baureihen"].append(f["modellreihe"])
            codes_idx[s]["fall_ids"].append(f["fall_id"])
        else:
            kl = f["_klasse"]
            if kl not in alle_klassen:
                gefahr, beschr = NEUE_KLASSEN[kl]
                knoten = {"klasse": kl, "achse": "leitsymptom", "beschreibung": beschr,
                          "gefahrenkategorie": gefahr, "status": "aktiv", "fall_ids": [],
                          "nachfolger": [], "abgrenzung_zu": [],
                          "unsicherheiten": "Klasse aus dem zweiten Sammellauf vom 22.08.2026."}
                tax["symptomklassen"].append(knoten)
                alle_klassen[kl] = knoten
                neue_klassen += 1
            alle_klassen[kl]["fall_ids"].append(f["fall_id"])

    for f in neu:
        del f["_klasse"]

    tax["_meta"]["codes_gesamt"] = len(tax["codes"])
    tax["_meta"]["symptomklassen_gesamt"] = len(tax["symptomklassen"])

    (WURZEL / "faelle.jsonl").write_text(
        "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in faelle + neu), encoding="utf-8")
    (WURZEL / "fehlercode_taxonomie.json").write_text(
        json.dumps(tax, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Kandidaten (nach Gegenpruefung): %d" % len(kandidaten))
    for k, v in prot.items():
        print("  %-22s %d" % (k, v))
    print("Bestand jetzt: %d Faelle" % (len(faelle) + len(neu)))
    print("Taxonomie: %d Codes (+%d), %d Klassen (+%d)"
          % (len(tax["codes"]), neue_codes, len(tax["symptomklassen"]), neue_klassen))


if __name__ == "__main__":
    main()
