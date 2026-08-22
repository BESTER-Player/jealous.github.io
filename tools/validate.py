#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prüft die Datensätze auf Konsistenz.

Geprüft werden:
  * JSON-Syntax und, falls das Paket "jsonschema" installiert ist, die Schemas
  * Eindeutigkeit der Schlüssel
  * referenzielle Integrität (Auftrag -> Kunde / Handwerker, Position -> Auftrag)
  * Gewerk-Abdeckung des zugeordneten Betriebs
  * Rechenlogik der Summen (Positionen, Netto, MwSt., Brutto)
  * Status- und Datumslogik
  * Übereinstimmung von auftraege.json und positionen.json
  * Aktualität der CSV-Exporte

Aufruf:  python3 tools/validate.py
Rückgabewert 0 = alles in Ordnung, 1 = mindestens ein Fehler.
"""
import csv
import json
import os
import sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(BASIS, "datensaetze", "json")
REF = os.path.join(BASIS, "datensaetze", "referenz")
CSV_DIR = os.path.join(BASIS, "datensaetze", "csv")
SCHEMA = os.path.join(BASIS, "datensaetze", "schema")

fehler = []
hinweise = []
CENT = 0.005


def pruefe(bedingung, meldung):
    if not bedingung:
        fehler.append(meldung)


def lade(pfad, schluessel):
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)[schluessel]


def main():
    kunden = lade(os.path.join(JSON, "kunden.json"), "kunden")
    handwerker = lade(os.path.join(JSON, "handwerker.json"), "handwerker")
    auftraege = lade(os.path.join(JSON, "auftraege.json"), "auftraege")
    positionen = lade(os.path.join(JSON, "positionen.json"), "positionen")

    gewerk_codes = {g["code"] for g in lade(os.path.join(REF, "gewerke.json"), "gewerke")}
    status_ref = {s["code"]: s for s in lade(os.path.join(REF, "auftragsstatus.json"), "status")}
    einheiten = {e["code"] for e in lade(os.path.join(REF, "einheiten.json"), "einheiten")}

    kunde_ids = {k["kunde_id"] for k in kunden}
    hw_ids = {h["handwerker_id"] for h in handwerker}
    hw_nach_id = {h["handwerker_id"]: h for h in handwerker}

    # --- Eindeutigkeit ---
    pruefe(len(kunde_ids) == len(kunden), "Doppelte kunde_id in kunden.json")
    pruefe(len(hw_ids) == len(handwerker), "Doppelte handwerker_id in handwerker.json")
    auftrag_ids = [a["auftrag_id"] for a in auftraege]
    pruefe(len(set(auftrag_ids)) == len(auftrag_ids), "Doppelte auftrag_id in auftraege.json")
    pos_ids = [p["position_id"] for p in positionen]
    pruefe(len(set(pos_ids)) == len(pos_ids), "Doppelte position_id in positionen.json")

    # --- Handwerker ---
    for h in handwerker:
        for g in h["gewerke"]:
            pruefe(g in gewerk_codes,
                   "%s: unbekanntes Gewerk '%s'" % (h["handwerker_id"], g))
        pruefe(0 < h["stundensatz_eur"] <= 500,
               "%s: unplausibler Stundensatz %s" % (h["handwerker_id"], h["stundensatz_eur"]))

    # --- Kunden ---
    for k in kunden:
        if k["typ"] == "gewerblich":
            pruefe(bool(k.get("firma")),
                   "%s: gewerblicher Kunde ohne Firma" % k["kunde_id"])

    # --- Aufträge ---
    eingebettet = 0
    for a in auftraege:
        aid = a["auftrag_id"]
        pruefe(a["kunde_id"] in kunde_ids, "%s: unbekannte kunde_id %s" % (aid, a["kunde_id"]))
        pruefe(a["gewerk"] in gewerk_codes, "%s: unbekanntes Gewerk '%s'" % (aid, a["gewerk"]))
        pruefe(a["status"] in status_ref, "%s: unbekannter Status '%s'" % (aid, a["status"]))

        hid = a.get("handwerker_id")
        if hid is not None:
            pruefe(hid in hw_ids, "%s: unbekannte handwerker_id %s" % (aid, hid))
            if hid in hw_nach_id:
                pruefe(a["gewerk"] in hw_nach_id[hid]["gewerke"],
                       "%s: Betrieb %s deckt Gewerk '%s' nicht ab" % (aid, hid, a["gewerk"]))
                if not hw_nach_id[hid]["aktiv"]:
                    hinweise.append("%s: zugeordneter Betrieb %s ist inaktiv" % (aid, hid))

        # Statuslogik
        if a["status"] in ("beauftragt", "in_arbeit", "abgeschlossen", "abgerechnet"):
            pruefe(hid is not None, "%s: Status '%s' ohne zugeordneten Betrieb" % (aid, a["status"]))
        if a["status"] == "abgerechnet":
            pruefe(a.get("ausgefuehrt_am") and a.get("abgerechnet_am"),
                   "%s: abgerechnet ohne Ausführungs- oder Rechnungsdatum" % aid)
        if a["status"] == "storniert":
            pruefe(a.get("storniert_am") and a.get("stornogrund"),
                   "%s: storniert ohne Datum oder Grund" % aid)
        if a["status"] in ("neu", "in_pruefung"):
            pruefe(a.get("ausgefuehrt_am") is None,
                   "%s: Ausführungsdatum trotz Status '%s'" % (aid, a["status"]))

        # Datumslogik
        von, bis = a.get("wunschtermin_von"), a.get("wunschtermin_bis")
        if von and bis:
            pruefe(von <= bis, "%s: wunschtermin_von liegt nach wunschtermin_bis" % aid)
        if von:
            pruefe(a["eingegangen_am"][:10] <= von,
                   "%s: Wunschtermin liegt vor dem Auftragseingang" % aid)
        if a.get("ausgefuehrt_am") and a.get("abgerechnet_am"):
            pruefe(a["ausgefuehrt_am"] <= a["abgerechnet_am"],
                   "%s: Rechnungsdatum liegt vor der Ausführung" % aid)

        # Summenlogik
        netto = 0.0
        nummern = set()
        for p in a["positionen"]:
            pruefe(p["einheit"] in einheiten,
                   "%s Pos. %s: unbekannte Einheit '%s'" % (aid, p["pos_nr"], p["einheit"]))
            pruefe(p["pos_nr"] not in nummern,
                   "%s: doppelte Positionsnummer %s" % (aid, p["pos_nr"]))
            nummern.add(p["pos_nr"])
            erwartet = round(p["menge"] * p["einzelpreis_netto_eur"], 2)
            pruefe(abs(erwartet - p["gesamtpreis_netto_eur"]) < CENT,
                   "%s Pos. %s: Gesamtpreis %s statt %s" % (
                       aid, p["pos_nr"], p["gesamtpreis_netto_eur"], erwartet))
            netto += p["gesamtpreis_netto_eur"]
        eingebettet += len(a["positionen"])

        netto = round(netto, 2)
        pruefe(abs(netto - a["angebotssumme_netto_eur"]) < CENT,
               "%s: Nettosumme %s, Positionen ergeben %s" % (aid, a["angebotssumme_netto_eur"], netto))
        mwst = round(a["angebotssumme_netto_eur"] * a["mwst_satz"], 2)
        pruefe(abs(mwst - a["mwst_betrag_eur"]) < CENT,
               "%s: MwSt. %s, erwartet %s" % (aid, a["mwst_betrag_eur"], mwst))
        brutto = round(a["angebotssumme_netto_eur"] + a["mwst_betrag_eur"], 2)
        pruefe(abs(brutto - a["angebotssumme_brutto_eur"]) < CENT,
               "%s: Bruttosumme %s, erwartet %s" % (aid, a["angebotssumme_brutto_eur"], brutto))
        pruefe(a["positionsanzahl"] == len(a["positionen"]),
               "%s: positionsanzahl %s, tatsächlich %s" % (aid, a["positionsanzahl"], len(a["positionen"])))

        if a.get("budget_rahmen_eur") is not None and a["angebotssumme_netto_eur"] > a["budget_rahmen_eur"]:
            hinweise.append("%s: Angebot (%.2f netto) übersteigt den Budgetrahmen (%.2f)" % (
                aid, a["angebotssumme_netto_eur"], a["budget_rahmen_eur"]))

    # --- positionen.json gegen auftraege.json ---
    pruefe(len(positionen) == eingebettet,
           "positionen.json enthält %d Zeilen, auftraege.json %d eingebettete Positionen" % (
               len(positionen), eingebettet))
    auftrag_id_menge = set(auftrag_ids)
    for p in positionen:
        pruefe(p["auftrag_id"] in auftrag_id_menge,
               "%s: verweist auf unbekannten Auftrag %s" % (p["position_id"], p["auftrag_id"]))
        pruefe(p["position_id"] == "%s-%03d" % (p["auftrag_id"], p["pos_nr"]),
               "%s: position_id passt nicht zu auftrag_id/pos_nr" % p["position_id"])

    # --- CSV-Exporte aktuell? ---
    for name, erwartet in (("kunden", len(kunden)), ("handwerker", len(handwerker)),
                           ("auftraege", len(auftraege)), ("positionen", len(positionen))):
        pfad = os.path.join(CSV_DIR, name + ".csv")
        if not os.path.exists(pfad):
            fehler.append("CSV fehlt: datensaetze/csv/%s.csv (tools/build.py ausführen)" % name)
            continue
        with open(pfad, encoding="utf-8", newline="") as f:
            zeilen = sum(1 for _ in csv.DictReader(f, delimiter=";"))
        pruefe(zeilen == erwartet,
               "datensaetze/csv/%s.csv hat %d Zeilen, erwartet %d (tools/build.py ausführen)" % (
                   name, zeilen, erwartet))

    # --- JSON-Schema, falls verfügbar ---
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        hinweise.append("Paket 'jsonschema' nicht installiert, Schemaprüfung übersprungen "
                        "(pip install jsonschema).")
    else:
        def schema(name):
            with open(os.path.join(SCHEMA, name), encoding="utf-8") as f:
                return json.load(f)

        pos_schema = schema("position.schema.json")
        auftrag_schema = schema("auftrag.schema.json")
        # Der einzige externe $ref wird direkt eingesetzt, damit kein Resolver nötig ist.
        auftrag_schema["properties"]["positionen"]["items"] = pos_schema

        for bez, daten, s in (("Kunde", kunden, schema("kunde.schema.json")),
                              ("Handwerker", handwerker, schema("handwerker.schema.json")),
                              ("Auftrag", auftraege, auftrag_schema),
                              ("Position", positionen, pos_schema)):
            v = Draft202012Validator(s)
            for satz in daten:
                kennung = satz.get("auftrag_id") or satz.get("kunde_id") \
                    or satz.get("handwerker_id") or satz.get("position_id")
                for e in sorted(v.iter_errors(satz), key=lambda x: list(x.absolute_path)):
                    fehler.append("%s-Schema %s: %s -> %s" % (
                        bez, kennung, "/".join(str(x) for x in e.absolute_path) or "(Wurzel)", e.message))

    # --- Ergebnis ---
    print("Geprüft: %d Kunden, %d Betriebe, %d Aufträge, %d Positionen"
          % (len(kunden), len(handwerker), len(auftraege), len(positionen)))
    for h in hinweise:
        print("  Hinweis: %s" % h)
    if fehler:
        print("\n%d Fehler:" % len(fehler))
        for f in fehler:
            print("  FEHLER: %s" % f)
        return 1
    print("\nAlle Prüfungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
