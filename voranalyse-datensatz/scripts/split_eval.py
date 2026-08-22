#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_eval.py - zieht Schritt 6: ca. 20 % der Faelle mit bestaetigungsgrad
"bestaetigt" wandern ins Eval-Set und werden aus der Wissensbasis entfernt.

Gezogen wird geschichtet nach Hersteller und mit festem Seed, damit der Split
reproduzierbar ist und nicht zufaellig einen ganzen Hersteller aus dem Testset
kippt. Zufaellig heisst zufaellig - es wird nicht nach Einfachheit sortiert.

Aufruf:  python3 scripts/split_eval.py [projektverzeichnis] [--seed 42] [--dry-run]
"""

import argparse
import json
import random
from collections import defaultdict
from datetime import date
from pathlib import Path

ANTEIL = 0.20


def lade(pfad):
    return [json.loads(z) for z in pfad.read_text(encoding="utf-8").splitlines() if z.strip()]


def schreibe(pfad, saetze):
    pfad.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in saetze),
                    encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("wurzel", nargs="?", default=str(Path(__file__).resolve().parent.parent))
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    wurzel = Path(args.wurzel)
    faelle_pfad = wurzel / "faelle.jsonl"
    eval_pfad = wurzel / "eval_set.jsonl"

    alle = lade(faelle_pfad)
    if eval_pfad.exists() and lade(eval_pfad):
        raise SystemExit("eval_set.jsonl ist nicht leer - Split wurde offenbar schon "
                         "gezogen. Erneutes Ziehen wuerde die Trennung aufweichen.")

    kandidaten = [f for f in alle if f.get("bestaetigungsgrad") == "bestaetigt"]
    if not kandidaten:
        raise SystemExit("Keine Faelle mit bestaetigungsgrad='bestaetigt' - nichts zu ziehen.")

    schichten = defaultdict(list)
    for f in kandidaten:
        schichten[f.get("hersteller", "unbekannt")].append(f)

    rng = random.Random(args.seed)
    gezogen, protokoll = [], []
    for hersteller in sorted(schichten):
        gruppe = sorted(schichten[hersteller], key=lambda f: f["fall_id"])
        n = round(ANTEIL * len(gruppe))
        if n == 0 and len(gruppe) >= 5:
            n = 1  # kleine Schicht trotzdem im Testset vertreten
        auswahl = rng.sample(gruppe, n) if n else []
        gezogen.extend(auswahl)
        protokoll.append((hersteller, len(gruppe), n, sorted(f["fall_id"] for f in auswahl)))

    gezogen_ids = {f["fall_id"] for f in gezogen}
    rest = [f for f in alle if f["fall_id"] not in gezogen_ids]

    print(f"Wissensbasis vorher: {len(alle)} | davon 'bestaetigt': {len(kandidaten)}")
    print(f"Gezogen: {len(gezogen)} ({len(gezogen)/len(kandidaten)*100:.1f} % der bestaetigten, "
          f"{len(gezogen)/len(alle)*100:.1f} % aller Faelle)")
    for hersteller, n_gruppe, n, ids in protokoll:
        print(f"  {hersteller:<15} {n}/{n_gruppe}  {', '.join(ids) if ids else '-'}")

    if args.dry_run:
        print("\n--dry-run: nichts geschrieben.")
        return

    schreibe(eval_pfad, gezogen)
    schreibe(faelle_pfad, rest)

    zeilen = [
        "# Eval-Split-Protokoll", "",
        f"- Datum: {date.today().isoformat()}",
        f"- Seed: {args.seed} (gleicher Seed + gleiche Eingabe = gleicher Split)",
        f"- Schichtung: nach Hersteller, Ziehung ohne Zuruecklegen",
        f"- Grundgesamtheit: {len(kandidaten)} Faelle mit bestaetigungsgrad='bestaetigt'",
        f"- Gezogen: {len(gezogen)} Faelle -> eval_set.jsonl",
        f"- Wissensbasis danach: {len(rest)} Faelle", "",
        "| Hersteller | bestaetigt | gezogen | fall_id |",
        "|---|---|---|---|",
    ]
    for hersteller, n_gruppe, n, ids in protokoll:
        zeilen.append(f"| {hersteller} | {n_gruppe} | {n} | {', '.join(ids) if ids else '-'} |")
    (wurzel / "split_log.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print("\nGeschrieben: eval_set.jsonl, faelle.jsonl, split_log.md")


if __name__ == "__main__":
    main()
