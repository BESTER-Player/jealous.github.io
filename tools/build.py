#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt die CSV- und SQL-Exporte aus den JSON-Quelldaten.

Quelle der Wahrheit sind die Dateien unter datensaetze/json/.
Aufruf:  python3 tools/build.py
"""
import csv
import json
import os

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(BASIS, "datensaetze", "json")
CSV_DIR = os.path.join(BASIS, "datensaetze", "csv")
SQL_DIR = os.path.join(BASIS, "datensaetze", "sql")


def lade(name, schluessel):
    with open(os.path.join(JSON, name + ".json"), encoding="utf-8") as f:
        return json.load(f)[schluessel]


def _csv_wert(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return 1 if v else 0
    return v


def schreibe_csv(name, spalten, zeilen):
    pfad = os.path.join(CSV_DIR, name + ".csv")
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=spalten, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for z in zeilen:
            w.writerow({k: _csv_wert(z.get(k)) for k in spalten})
    print("  geschrieben: datensaetze/csv/%s.csv (%d Zeilen)" % (name, len(zeilen)))


def sql_wert(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return repr(v)
    return "'" + str(v).replace("'", "''") + "'"


def schreibe_sql_seed(tabellen):
    pfad = os.path.join(SQL_DIR, "seed.sql")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write("-- Direct Handwork: Beispieldaten\n")
        f.write("-- Automatisch erzeugt von tools/build.py, nicht von Hand bearbeiten.\n")
        f.write("-- Voraussetzung: datensaetze/sql/schema.sql wurde vorher eingespielt.\n\n")
        f.write("BEGIN TRANSACTION;\n\n")
        gesamt = 0
        for tabelle, spalten, zeilen in tabellen:
            f.write("-- %s (%d Datensätze)\n" % (tabelle, len(zeilen)))
            for z in zeilen:
                werte = ", ".join(sql_wert(z.get(s)) for s in spalten)
                f.write("INSERT INTO %s (%s) VALUES (%s);\n" % (tabelle, ", ".join(spalten), werte))
            f.write("\n")
            gesamt += len(zeilen)
        f.write("COMMIT;\n")
    print("  geschrieben: datensaetze/sql/seed.sql (%d INSERTs)" % gesamt)


def main():
    kunden = lade("kunden", "kunden")
    handwerker = lade("handwerker", "handwerker")
    auftraege = lade("auftraege", "auftraege")
    positionen = lade("positionen", "positionen")

    kunden_spalten = ["kunde_id", "typ", "anrede", "vorname", "nachname", "firma", "strasse",
                      "plz", "ort", "land", "telefon", "email", "erstkontakt_am", "newsletter", "notiz"]

    hw_flach = []
    for h in handwerker:
        r = dict(h)
        r["gewerke"] = ",".join(h["gewerke"])
        hw_flach.append(r)
    hw_spalten = ["handwerker_id", "betrieb", "ansprechpartner", "gewerke", "strasse", "plz", "ort",
                  "telefon", "email", "ust_id", "stundensatz_eur", "einsatzradius_km",
                  "mitarbeiterzahl", "notdienst", "bewertung", "aktiv", "partner_seit"]

    auf_flach = []
    for a in auftraege:
        r = {k: v for k, v in a.items() if k != "positionen"}
        o = a.get("objekt") or {}
        r["objekt_strasse"] = o.get("strasse")
        r["objekt_plz"] = o.get("plz")
        r["objekt_ort"] = o.get("ort")
        r["objekt_etage"] = o.get("etage")
        r["objekt_zugang"] = o.get("zugang")
        r.pop("objekt", None)
        auf_flach.append(r)
    auf_spalten = ["auftrag_id", "kunde_id", "handwerker_id", "gewerk", "titel", "beschreibung",
                   "objekt_strasse", "objekt_plz", "objekt_ort", "objekt_etage", "objekt_zugang",
                   "kanal", "prioritaet", "status", "eingegangen_am", "wunschtermin_von",
                   "wunschtermin_bis", "termin_bestaetigt_am", "ausgefuehrt_am", "abgerechnet_am",
                   "storniert_am", "stornogrund", "budget_rahmen_eur", "anfahrt_km",
                   "geschaetzte_dauer_h", "tatsaechliche_dauer_h", "zahlungsart",
                   "positionsanzahl", "angebotssumme_netto_eur", "mwst_satz", "mwst_betrag_eur",
                   "angebotssumme_brutto_eur", "notiz"]

    pos_spalten = ["position_id", "auftrag_id", "pos_nr", "leistung", "art", "menge", "einheit",
                   "einzelpreis_netto_eur", "gesamtpreis_netto_eur"]

    print("CSV-Export:")
    schreibe_csv("kunden", kunden_spalten, kunden)
    schreibe_csv("handwerker", hw_spalten, hw_flach)
    schreibe_csv("auftraege", auf_spalten, auf_flach)
    schreibe_csv("positionen", pos_spalten, positionen)

    print("SQL-Export:")
    schreibe_sql_seed([
        ("kunde", kunden_spalten, kunden),
        ("handwerker", hw_spalten, hw_flach),
        ("auftrag", auf_spalten, auf_flach),
        ("auftragsposition", pos_spalten, positionen),
    ])


if __name__ == "__main__":
    main()
