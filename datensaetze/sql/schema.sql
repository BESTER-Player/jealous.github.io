-- Direct Handwork: Datenbankschema für Auftragsdatensätze
-- Dialekt: SQLite (läuft mit minimalen Anpassungen auch unter PostgreSQL)
-- Einspielen:  sqlite3 direct_handwork.db < datensaetze/sql/schema.sql
--              sqlite3 direct_handwork.db < datensaetze/sql/seed.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS auftragsposition;
DROP TABLE IF EXISTS auftrag;
DROP TABLE IF EXISTS handwerker;
DROP TABLE IF EXISTS kunde;

-- ---------------------------------------------------------------- Kunde
CREATE TABLE kunde (
    kunde_id        TEXT PRIMARY KEY,
    typ             TEXT NOT NULL CHECK (typ IN ('privat', 'gewerblich')),
    anrede          TEXT,
    vorname         TEXT,
    nachname        TEXT,
    firma           TEXT,
    strasse         TEXT NOT NULL,
    plz             TEXT NOT NULL CHECK (length(plz) = 5),
    ort             TEXT NOT NULL,
    land            TEXT NOT NULL DEFAULT 'DE',
    telefon         TEXT,
    email           TEXT,
    erstkontakt_am  TEXT NOT NULL,
    newsletter      INTEGER NOT NULL DEFAULT 0 CHECK (newsletter IN (0, 1)),
    notiz           TEXT,
    CHECK (typ = 'privat' OR firma IS NOT NULL)
);

-- ---------------------------------------------------------- Handwerker
CREATE TABLE handwerker (
    handwerker_id    TEXT PRIMARY KEY,
    betrieb          TEXT NOT NULL,
    ansprechpartner  TEXT,
    gewerke          TEXT NOT NULL,   -- kommaseparierte Gewerke-Codes
    strasse          TEXT NOT NULL,
    plz              TEXT NOT NULL CHECK (length(plz) = 5),
    ort              TEXT NOT NULL,
    telefon          TEXT,
    email            TEXT,
    ust_id           TEXT,
    stundensatz_eur  REAL NOT NULL CHECK (stundensatz_eur > 0),
    einsatzradius_km INTEGER NOT NULL CHECK (einsatzradius_km > 0),
    mitarbeiterzahl  INTEGER CHECK (mitarbeiterzahl >= 0),
    notdienst        INTEGER NOT NULL DEFAULT 0 CHECK (notdienst IN (0, 1)),
    bewertung        REAL CHECK (bewertung BETWEEN 1.0 AND 5.0),
    aktiv            INTEGER NOT NULL DEFAULT 1 CHECK (aktiv IN (0, 1)),
    partner_seit     TEXT
);

-- -------------------------------------------------------------- Auftrag
CREATE TABLE auftrag (
    auftrag_id       TEXT PRIMARY KEY,
    kunde_id         TEXT NOT NULL REFERENCES kunde (kunde_id),
    handwerker_id    TEXT REFERENCES handwerker (handwerker_id),
    gewerk           TEXT NOT NULL CHECK (gewerk IN (
                        'sanitaer', 'heizung', 'elektro', 'maler', 'fliesen',
                        'tischler', 'dachdecker', 'trockenbau', 'schlosser', 'garten')),
    titel            TEXT NOT NULL,
    beschreibung     TEXT,

    objekt_strasse   TEXT NOT NULL,
    objekt_plz       TEXT NOT NULL CHECK (length(objekt_plz) = 5),
    objekt_ort       TEXT NOT NULL,
    objekt_etage     INTEGER,
    objekt_zugang    TEXT,

    kanal            TEXT NOT NULL CHECK (kanal IN ('web', 'app', 'telefon', 'email', 'empfehlung')),
    prioritaet       TEXT NOT NULL CHECK (prioritaet IN ('niedrig', 'normal', 'hoch', 'notfall')),
    status           TEXT NOT NULL CHECK (status IN (
                        'neu', 'in_pruefung', 'angebot_erstellt', 'beauftragt',
                        'in_arbeit', 'abgeschlossen', 'abgerechnet', 'storniert')),

    eingegangen_am        TEXT NOT NULL,
    wunschtermin_von      TEXT,
    wunschtermin_bis      TEXT,
    termin_bestaetigt_am  TEXT,
    ausgefuehrt_am        TEXT,
    abgerechnet_am        TEXT,
    storniert_am          TEXT,
    stornogrund           TEXT,

    budget_rahmen_eur      REAL CHECK (budget_rahmen_eur >= 0),
    anfahrt_km             REAL CHECK (anfahrt_km >= 0),
    geschaetzte_dauer_h    REAL CHECK (geschaetzte_dauer_h >= 0),
    tatsaechliche_dauer_h  REAL CHECK (tatsaechliche_dauer_h >= 0),
    zahlungsart            TEXT CHECK (zahlungsart IN ('rechnung', 'lastschrift', 'ec', 'bar')),

    positionsanzahl           INTEGER NOT NULL DEFAULT 0,
    angebotssumme_netto_eur   REAL NOT NULL DEFAULT 0,
    mwst_satz                 REAL NOT NULL DEFAULT 0.19,
    mwst_betrag_eur           REAL NOT NULL DEFAULT 0,
    angebotssumme_brutto_eur  REAL NOT NULL DEFAULT 0,
    notiz                     TEXT,

    -- Ein abgerechneter Auftrag braucht Ausführungs- und Rechnungsdatum
    CHECK (status <> 'abgerechnet' OR (ausgefuehrt_am IS NOT NULL AND abgerechnet_am IS NOT NULL)),
    -- Ein stornierter Auftrag braucht einen Stornogrund
    CHECK (status <> 'storniert' OR storniert_am IS NOT NULL),
    -- Ab Status "beauftragt" muss ein Betrieb zugeordnet sein
    CHECK (status IN ('neu', 'in_pruefung', 'angebot_erstellt', 'storniert') OR handwerker_id IS NOT NULL),
    CHECK (wunschtermin_bis IS NULL OR wunschtermin_von IS NULL OR wunschtermin_bis >= wunschtermin_von)
);

-- ----------------------------------------------------- Auftragsposition
CREATE TABLE auftragsposition (
    position_id            TEXT PRIMARY KEY,
    auftrag_id             TEXT NOT NULL REFERENCES auftrag (auftrag_id) ON DELETE CASCADE,
    pos_nr                 INTEGER NOT NULL,
    leistung               TEXT NOT NULL,
    art                    TEXT NOT NULL CHECK (art IN ('lohn', 'material', 'anfahrt', 'fremdleistung')),
    menge                  REAL NOT NULL CHECK (menge > 0),
    einheit                TEXT NOT NULL CHECK (einheit IN ('h', 'Stk', 'm', 'm2', 'm3', 'psch', 'km')),
    einzelpreis_netto_eur  REAL NOT NULL CHECK (einzelpreis_netto_eur >= 0),
    gesamtpreis_netto_eur  REAL NOT NULL CHECK (gesamtpreis_netto_eur >= 0),
    UNIQUE (auftrag_id, pos_nr)
);

CREATE INDEX idx_auftrag_kunde       ON auftrag (kunde_id);
CREATE INDEX idx_auftrag_handwerker  ON auftrag (handwerker_id);
CREATE INDEX idx_auftrag_status      ON auftrag (status);
CREATE INDEX idx_auftrag_gewerk      ON auftrag (gewerk);
CREATE INDEX idx_auftrag_eingang     ON auftrag (eingegangen_am);
CREATE INDEX idx_position_auftrag    ON auftragsposition (auftrag_id);

-- Offene Aufträge inkl. Kunde und zugeordnetem Betrieb
CREATE VIEW v_offene_auftraege AS
SELECT a.auftrag_id,
       a.status,
       a.prioritaet,
       a.gewerk,
       a.titel,
       COALESCE(k.firma, k.vorname || ' ' || k.nachname) AS kunde,
       h.betrieb                                          AS betrieb,
       a.wunschtermin_von,
       a.wunschtermin_bis,
       a.angebotssumme_brutto_eur
FROM auftrag a
JOIN kunde k       ON k.kunde_id = a.kunde_id
LEFT JOIN handwerker h ON h.handwerker_id = a.handwerker_id
WHERE a.status NOT IN ('abgerechnet', 'storniert');

-- Umsatz je Gewerk über abgerechnete Aufträge
CREATE VIEW v_umsatz_je_gewerk AS
SELECT gewerk,
       COUNT(*)                            AS anzahl_auftraege,
       ROUND(SUM(angebotssumme_netto_eur), 2)  AS umsatz_netto_eur,
       ROUND(SUM(angebotssumme_brutto_eur), 2) AS umsatz_brutto_eur
FROM auftrag
WHERE status = 'abgerechnet'
GROUP BY gewerk;
