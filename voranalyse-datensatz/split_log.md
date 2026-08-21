# Eval-Split-Protokoll

**Status: geplant, NICHT ausgeführt.** `eval_set.jsonl` ist leer.

## Dry-Run vom 22.08.2026

- Seed: 42
- Schichtung: nach Hersteller, Ziehung ohne Zurücklegen
- Grundgesamtheit: 5 Fälle mit `bestaetigungsgrad: bestaetigt`
- Ziehung ergäbe: 1 Fall (20,0 % der bestätigten, 12,5 % aller Fälle)

| Hersteller | bestätigt | gezogen | fall_id |
|---|---|---|---|
| Buderus | 1 | 0 | – |
| Viessmann | 4 | 1 | VIE-0001 |

## Warum nicht ausgeführt

Ein Testset aus einem einzigen Fall misst nichts. Gleichzeitig entzöge der
Split der Wissensbasis 20 % ihres belastbaren Teils und würde Viessmann – den
einzigen halbwegs abgedeckten Hersteller – weiter ausdünnen.

Die Ziehung wird nachgeholt, sobald mindestens rund 50 bestätigte Fälle
vorliegen. Bis dahin bleibt `eval_set.jsonl` leer. Der Ausführungsbefehl:

```bash
python3 scripts/split_eval.py --seed 42
```

Das Skript verweigert die Ausführung, wenn `eval_set.jsonl` bereits befüllt ist –
ein zweiter Zug würde die Trennung aufweichen.
