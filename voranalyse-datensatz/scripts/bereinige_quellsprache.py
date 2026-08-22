#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entfernt Faelle aus Quellen ausserhalb der Auftragssprache.

Die Konfiguration des Auftrags nennt als Quellsprache "primaer Deutsch, Englisch
nur ergaenzend". Faelle aus anderssprachigen Quellen liegen ausserhalb dieser
Vorgabe. Hinzu kommt ein inhaltliches Risiko: eine fremdsprachige Ueberschrift,
von einem deutschsprachigen Agenten aus dem Suchergebnis gedeutet, kann still
falsch uebersetzt sein - ohne Seitenabruf ist das nicht pruefbar (Regel 8).

Aufruf: python3 scripts/bereinige_quellsprache.py [projektverzeichnis]
"""
import json
import sys
from pathlib import Path

WURZEL = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
ERLAUBT_TLD = (".de", ".at", ".ch", ".com", ".org", ".net", ".co.uk", ".eu", ".info")

faelle = [json.loads(z) for z in (WURZEL / "faelle.jsonl").read_text(encoding="utf-8").splitlines() if z.strip()]
tax = json.loads((WURZEL / "fehlercode_taxonomie.json").read_text(encoding="utf-8"))

raus = []
for f in faelle:
    host = f["quelle_url"].split("/")[2].lower().split(":")[0]
    if not host.endswith(ERLAUBT_TLD):
        raus.append(f)

ids = {f["fall_id"] for f in raus}
if not ids:
    print("Keine Faelle ausserhalb der Quellsprache gefunden.")
    raise SystemExit(0)

for f in raus:
    print("entfernt: %s  %s" % (f["fall_id"], f["quelle_url"].split("/")[2]))

rest = [f for f in faelle if f["fall_id"] not in ids]
(WURZEL / "faelle.jsonl").write_text(
    "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in rest), encoding="utf-8")

# Verweise in der Taxonomie mitziehen, sonst zeigen sie ins Leere
entfernte_knoten = 0
for c in tax["codes"]:
    c["fall_ids"] = [i for i in c["fall_ids"] if i not in ids]
for k in tax["symptomklassen"]:
    k["fall_ids"] = [i for i in k["fall_ids"] if i not in ids]
# Codeknoten, die nur diese Faelle verankert haben und sonst nichts belegen, entfallen
vorher = len(tax["codes"])
tax["codes"] = [c for c in tax["codes"]
                if c["fall_ids"] or c["offizielle_bedeutung"] or "Sammellauf" not in (c.get("unsicherheiten") or "")]
entfernte_knoten = vorher - len(tax["codes"])
# Leitsymptomklassen ohne jeden Fall aus den Sammellaeufen ebenso
vorher_k = len(tax["symptomklassen"])
tax["symptomklassen"] = [k for k in tax["symptomklassen"]
                         if k["fall_ids"] or "Sammellauf" not in (k.get("unsicherheiten") or "")]
entfernte_klassen = vorher_k - len(tax["symptomklassen"])

tax["_meta"]["codes_gesamt"] = len(tax["codes"])
tax["_meta"]["symptomklassen_gesamt"] = len(tax["symptomklassen"])
(WURZEL / "fehlercode_taxonomie.json").write_text(
    json.dumps(tax, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("\n%d Faelle entfernt, Bestand jetzt %d." % (len(ids), len(rest)))
print("Taxonomie bereinigt: -%d Codeknoten, -%d Symptomklassen (nur solche ohne verbleibende Belege)."
      % (entfernte_knoten, entfernte_klassen))
