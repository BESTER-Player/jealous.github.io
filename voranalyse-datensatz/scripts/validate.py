#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate.py - prueft faelle.jsonl und eval_set.jsonl gegen das Schema und
gegen die harten Regeln des Auftrags.

Aufruf:   python3 scripts/validate.py [projektverzeichnis]
Exit 0    keine Fehler (Warnungen moeglich)
Exit 1    mindestens ein Fehler

Nur Standardbibliothek, keine Netzwerkzugriffe.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- Schema-Kern

_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
}


def _check_value(value, spec, path, errors):
    types = spec.get("type")
    if types is not None:
        if isinstance(types, str):
            types = [types]
        if not any(_TYPE_CHECKS[t](value) for t in types):
            errors.append(f"{path}: Typ {type(value).__name__} nicht erlaubt "
                          f"(erwartet: {'|'.join(types)})")
            return
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{path}: Wert {value!r} nicht in {spec['enum']}")
    if "minLength" in spec and isinstance(value, str) \
            and len(value.strip()) < spec["minLength"]:
        errors.append(f"{path}: zu kurz / leer (min. {spec['minLength']} Zeichen)")
    if "items" in spec and isinstance(value, list):
        for i, item in enumerate(value):
            _check_value(item, spec["items"], f"{path}[{i}]", errors)


def validate_schema(rec, schema, path):
    errors = []
    if not isinstance(rec, dict):
        return [f"{path}: kein JSON-Objekt"]
    for key in schema.get("required", []):
        if key not in rec:
            errors.append(f"{path}: Pflichtfeld '{key}' fehlt")
    if schema.get("additionalProperties") is False:
        for key in rec:
            if key not in schema["properties"]:
                errors.append(f"{path}: unerlaubtes Feld '{key}' "
                              f"(Regel 4: kein Feld ausserhalb des Schemas)")
    for key, spec in schema["properties"].items():
        if key in rec:
            _check_value(rec[key], spec, f"{path}.{key}", errors)
    return errors


# ------------------------------------------------------------- Regelpruefungen

RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}")
RE_TELEFON = re.compile(r"(?<!\d)(?:\+49|0)[\s/\-]?\d[\d\s/\-]{7,}")
RE_HANDLE = re.compile(r"(?<!\S)@\w{3,}")
RE_PROFIL_URL = re.compile(r"/(users?|profile?s?|members?|mitglied(er)?)/", re.I)
RE_HAEUFIGKEIT = re.compile(
    r"(?:\bmeistens?\b|\bh[aä]e?ufigste[rn]?\b|\bfast immer\b|\d{1,3}\s?%|"
    r"\bin (?:aller|der) Regel\b|\btypischerweise\b|\bnormalerweise\b|"
    r"\bin den meisten F[aä]e?llen\b)", re.I)

FREITEXTFELDER = ("symptom_laie", "symptom_technisch", "tatsaechliche_ursache",
                  "abweichung_von_doku", "unsicherheiten",
                  "code_offizielle_bedeutung")


def validate_regeln(rec, path):
    """Gibt (errors, warnings) zurueck."""
    errors, warnings = [], []
    g = rec.get("gefahrenkategorie")

    # Regel 6 - Gas/Strom: Fachkraft zwingend, Schritte nur als Fachkraft-Hinweis
    if g in ("gas", "strom"):
        if rec.get("fachkraft_erforderlich") is not True:
            errors.append(f"{path}: gefahrenkategorie='{g}' verlangt "
                          f"fachkraft_erforderlich=true (Regel 6)")
        for i, schritt in enumerate(rec.get("diagnoseschritte") or []):
            if not str(schritt).startswith("[Fachkraft]"):
                errors.append(f"{path}.diagnoseschritte[{i}]: bei '{g}' muss jeder "
                              f"Schritt mit '[Fachkraft]' beginnen (Regel 6)")

    # Regel 1 - keine Bedeutung ohne Code
    if rec.get("fehlercode") is None and rec.get("code_offizielle_bedeutung") is not None:
        errors.append(f"{path}: code_offizielle_bedeutung gesetzt, aber fehlercode=null")
    if rec.get("abweichung_von_doku") is not None and rec.get("fehlercode") is None:
        warnings.append(f"{path}: abweichung_von_doku ohne Fehlercode - "
                        f"pruefen, worauf sich die Abweichung bezieht")

    # Regel 3 - Personenbezug
    for feld in FREITEXTFELDER:
        wert = rec.get(feld)
        if not isinstance(wert, str):
            continue
        if RE_EMAIL.search(wert):
            errors.append(f"{path}.{feld}: E-Mail-Adresse enthalten (Regel 3)")
        if RE_TELEFON.search(wert):
            errors.append(f"{path}.{feld}: moegliche Telefonnummer (Regel 3)")
        if RE_HANDLE.search(wert):
            errors.append(f"{path}.{feld}: moeglicher Nutzername (Regel 3)")
    url = rec.get("quelle_url")
    if isinstance(url, str):
        if not url.startswith(("http://", "https://")):
            errors.append(f"{path}.quelle_url: keine absolute URL")
        if RE_PROFIL_URL.search(url):
            errors.append(f"{path}.quelle_url: zeigt auf ein Nutzerprofil (Regel 3)")

    # Regel 4 - keine Haeufigkeitsaussagen aus Thread-Anzahlen
    for feld in ("tatsaechliche_ursache", "abweichung_von_doku", "symptom_technisch"):
        wert = rec.get(feld)
        if isinstance(wert, str) and RE_HAEUFIGKEIT.search(wert):
            warnings.append(f"{path}.{feld}: Haeufigkeitsformulierung - nur zulaessig, "
                            f"wenn sie aus der Herstellerdoku stammt, nie aus "
                            f"Thread-Anzahlen (Regel 4)")

    # Regel 2 - Laienzitat als Ausdruck, nicht als Textuebernahme
    sl = rec.get("symptom_laie")
    if isinstance(sl, str) and len(sl) > 200:
        warnings.append(f"{path}.symptom_laie: {len(sl)} Zeichen - auf Uebernahme "
                        f"von Originaltext pruefen (Regel 2)")

    return errors, warnings



# --------------------------------------------------------- Querverweispruefung

def _lade_json(pfad):
    if not pfad.exists():
        return None
    try:
        return json.loads(pfad.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"__fehler__": f"{pfad.name}: kein gueltiges JSON ({e.msg})"}


def validate_querverweise(wurzel, saetze):
    """Prueft die Verweise ZWISCHEN den Artefakten.

    Das Skelett des Auftrags (Schritt 2) verlangt, dass jeder Fall an einem
    Code-Knoten oder an einem Symptomknoten haengt. Ein Verweis, der ins Leere
    zeigt, bricht diese Verankerung - schemakonform, aber inhaltlich kaputt.

    Taxonomie und Sprachbruecke sind optional: fehlen sie, wird uebersprungen,
    damit validate.py auch auf einer reinen Fallsammlung laeuft.
    """
    errors, warnings = [], []
    tax = _lade_json(wurzel / "fehlercode_taxonomie.json")
    sb = _lade_json(wurzel / "sprachbruecke.json")

    for obj in (tax, sb):
        if isinstance(obj, dict) and "__fehler__" in obj:
            errors.append(obj["__fehler__"])
            return errors, warnings

    fall_ids = {r.get("fall_id") for _, r in saetze}
    faelle = [r for _, r in saetze]

    # -- Regel: mehrfach_unabhaengig ist laut README unterdefiniert ------------
    for r in faelle:
        if r.get("bestaetigungsgrad") == "mehrfach_unabhaengig":
            warnings.append(f"{r.get('fall_id')}: Grad 'mehrfach_unabhaengig' vergeben, "
                            f"obwohl das Unabhaengigkeitskriterium laut README offen ist")

    # -- Unabhaengigkeitsfalle: mehrere Faelle aus derselben Quelle ------------
    nach_url = {}
    for r in faelle:
        nach_url.setdefault(r.get("quelle_url"), []).append(r.get("fall_id"))
    for url, ids in sorted(nach_url.items()):
        if url and len(ids) > 1:
            warnings.append(f"Quelle mehrfach verwendet ({len(ids)} Faelle: {', '.join(sorted(ids))}) "
                            f"- diese Faelle sind NICHT unabhaengig: {url}")
            for fid in ids:
                rec = next(r for r in faelle if r.get("fall_id") == fid)
                if rec.get("bestaetigungsgrad") == "mehrfach_unabhaengig":
                    errors.append(f"{fid}: Grad 'mehrfach_unabhaengig', aber die Quelle wird "
                                  f"von {len(ids)} Faellen geteilt - das ist eine Quelle, nicht mehrere")

    # ------------------------------------------------------------- Taxonomie --
    if tax is None:
        warnings.append("fehlercode_taxonomie.json fehlt - Querverweise nicht geprueft")
    else:
        codes = tax.get("codes", [])
        klassen = tax.get("symptomklassen", [])
        meta = tax.get("_meta", {})

        if meta.get("codes_gesamt") not in (None, len(codes)):
            errors.append(f"fehlercode_taxonomie.json: _meta.codes_gesamt={meta['codes_gesamt']}, "
                          f"tatsaechlich {len(codes)}")
        if meta.get("symptomklassen_gesamt") not in (None, len(klassen)):
            errors.append(f"fehlercode_taxonomie.json: _meta.symptomklassen_gesamt="
                          f"{meta['symptomklassen_gesamt']}, tatsaechlich {len(klassen)}")

        gesehen = set()
        for c in codes:
            schluessel = (c.get("hersteller"), c.get("code"))
            if schluessel in gesehen:
                errors.append(f"fehlercode_taxonomie.json: Code {schluessel[0]} '{schluessel[1]}' "
                              f"doppelt erfasst")
            gesehen.add(schluessel)

        # tote Verweise Taxonomie -> Faelle
        for c in codes:
            for fid in c.get("fall_ids", []):
                if fid not in fall_ids:
                    errors.append(f"fehlercode_taxonomie.json: Code '{c.get('code')}' verweist auf "
                                  f"unbekannte fall_id '{fid}'")
        for k in klassen:
            for fid in k.get("fall_ids", []):
                if fid not in fall_ids:
                    errors.append(f"fehlercode_taxonomie.json: Symptomklasse '{k.get('klasse')}' "
                                  f"verweist auf unbekannte fall_id '{fid}'")

        # Verankerung Faelle -> Taxonomie
        klasse_je_fall = {}
        for k in klassen:
            for fid in k.get("fall_ids", []):
                klasse_je_fall.setdefault(fid, []).append(k.get("klasse"))

        for r in faelle:
            fid, code, hersteller = r.get("fall_id"), r.get("fehlercode"), r.get("hersteller")
            if code:
                treffer = [c for c in codes
                           if c.get("hersteller") == hersteller and c.get("code") == code]
                if not treffer:
                    errors.append(f"{fid}: fehlercode '{code}' ({hersteller}) hat keinen Knoten in "
                                  f"der Taxonomie - Fall ist nicht verankert")
                for c in treffer:
                    if fid not in c.get("fall_ids", []):
                        errors.append(f"{fid}: haengt an Code '{code}', ist dort aber nicht in "
                                      f"fall_ids eingetragen - Rueckverweis fehlt")
            elif fid not in klasse_je_fall:
                errors.append(f"{fid}: kein Fehlercode UND keine Symptomklasse - der Auftrag "
                              f"verlangt Verankerung an einem Code- oder Symptomknoten")

        # Fall an einem Code eingetragen, den er gar nicht traegt
        for c in codes:
            for fid in c.get("fall_ids", []):
                rec = next((r for r in faelle if r.get("fall_id") == fid), None)
                if rec and rec.get("fehlercode") not in (None, c.get("code")):
                    warnings.append(f"{fid} steht in fall_ids von Code '{c.get('code')}', traegt "
                                    f"aber '{rec.get('fehlercode')}' - Ober-/Zusatzcode oder Fehler?")

    # ---------------------------------------------------------- Sprachbruecke --
    if sb is None:
        warnings.append("sprachbruecke.json fehlt - Querverweise nicht geprueft")
    elif tax is not None:
        eintraege = sb.get("eintraege", [])
        meta = sb.get("_meta", {})
        if meta.get("eintraege_gesamt") not in (None, len(eintraege)):
            errors.append(f"sprachbruecke.json: _meta.eintraege_gesamt={meta['eintraege_gesamt']}, "
                          f"tatsaechlich {len(eintraege)}")

        bekannte = {k.get("klasse") for k in tax.get("symptomklassen", [])}
        benutzt = set()
        for e in eintraege:
            k = e.get("symptomklasse")
            benutzt.add(k)
            if k not in bekannte:
                errors.append(f"sprachbruecke.json: Ausdruck '{e.get('ausdruck')}' bildet auf "
                              f"Symptomklasse '{k}' ab, die in der Taxonomie nicht definiert ist")
            for m in e.get("mehrdeutig_zu", []):
                if m not in bekannte:
                    errors.append(f"sprachbruecke.json: '{e.get('ausdruck')}' verweist in "
                                  f"mehrdeutig_zu auf unbekannte Symptomklasse '{m}'")
        for k in sorted(bekannte - benutzt):
            warnings.append(f"Symptomklasse '{k}' hat keinen Eintrag in der Sprachbruecke - "
                            f"ueber eine Laienschilderung nicht erreichbar")

    return errors, warnings


# ------------------------------------------------------------------ Dateiebene

def lade_jsonl(pfad):
    saetze, fehler = [], []
    if not pfad.exists():
        return saetze, [f"{pfad.name}: Datei fehlt"]
    for nr, zeile in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
        if not zeile.strip():
            continue
        try:
            saetze.append((nr, json.loads(zeile)))
        except json.JSONDecodeError as e:
            fehler.append(f"{pfad.name}:{nr}: kein gueltiges JSON ({e.msg})")
    return saetze, fehler


def main():
    wurzel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    schema = json.loads((wurzel / "schema" / "fall.schema.json").read_text(encoding="utf-8"))

    errors, warnings = [], []
    bestand = {}

    for name in ("faelle.jsonl", "eval_set.jsonl"):
        saetze, ladefehler = lade_jsonl(wurzel / name)
        errors.extend(ladefehler)
        ids, urls = set(), set()
        for nr, rec in saetze:
            path = f"{name}:{nr}"
            errors.extend(validate_schema(rec, schema, path))
            e, w = validate_regeln(rec, path)
            errors.extend(e)
            warnings.extend(w)
            fid = rec.get("fall_id")
            if fid in ids:
                errors.append(f"{path}: fall_id '{fid}' doppelt in {name}")
            ids.add(fid)
            urls.add(rec.get("quelle_url"))
        bestand[name] = {"saetze": saetze, "ids": ids, "urls": urls}

    # Regel 5 - Eval-Faelle nie in der Wissensbasis
    ueberlappung = bestand["faelle.jsonl"]["ids"] & bestand["eval_set.jsonl"]["ids"]
    for fid in sorted(x for x in ueberlappung if x):
        errors.append(f"Regel 5 verletzt: fall_id '{fid}' steht in Wissensbasis UND Eval-Set")
    url_ueberlappung = bestand["faelle.jsonl"]["urls"] & bestand["eval_set.jsonl"]["urls"]
    for u in sorted(x for x in url_ueberlappung if x):
        warnings.append(f"Quelle '{u}' in beiden Dateien - auf Doppelerfassung "
                        f"desselben Threads pruefen (Regel 5)")

    # Querverweise zwischen den Artefakten
    qe, qw = validate_querverweise(wurzel, bestand["faelle.jsonl"]["saetze"]
                                   + bestand["eval_set.jsonl"]["saetze"])
    errors.extend(qe)
    warnings.extend(qw)

    # Kennzahlen
    n_wb = len(bestand["faelle.jsonl"]["saetze"])
    n_ev = len(bestand["eval_set.jsonl"]["saetze"])
    grade = {}
    for _, rec in bestand["faelle.jsonl"]["saetze"] + bestand["eval_set.jsonl"]["saetze"]:
        grade[rec.get("bestaetigungsgrad")] = grade.get(rec.get("bestaetigungsgrad"), 0) + 1

    print(f"Wissensbasis: {n_wb} Faelle | Eval-Set: {n_ev} Faelle")
    if grade:
        print("Bestaetigungsgrade: " + ", ".join(f"{k}={v}" for k, v in sorted(grade.items())))
    if n_wb + n_ev:
        anteil = n_ev / (n_wb + n_ev) * 100
        print(f"Eval-Anteil: {anteil:.1f} %")
    print()

    for w in warnings:
        print(f"WARNUNG  {w}")
    for e in errors:
        print(f"FEHLER   {e}")
    print()
    print(f"{len(errors)} Fehler, {len(warnings)} Warnungen")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
