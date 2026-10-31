#!/usr/bin/env python3
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def apply_ddl_and_seal():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # 1. Crear tabla m82_ledger_seals_v2
    cur.execute("""
    CREATE TABLE IF NOT EXISTS m82_ledger_seals_v2 (
        seal_id TEXT PRIMARY KEY,
        prev_hash TEXT,
        record_id TEXT,
        operation TEXT CHECK(operation IN ('INSERT', 'UPDATE', 'SEAL', 'GUARD')),
        payload_hash TEXT,
        timestamp TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        node_id TEXT DEFAULT 'CHARALLAVE-L4L5-EDGE'
    );
    """)

    # 2. Re-insertar Sello Canónico
    cur.execute("""
    INSERT OR REPLACE INTO m82_ledger_seals_v2 (seal_id, prev_hash, record_id, operation, payload_hash)
    VALUES ('SCV61-1500-M82-444-TRUST-113', 'GENESIS_444_BASE', '113', 'SEAL', 'SHA256_TRUST_113_VALIDATED');
    """)

    # 3. Vista Unificada macro_dossier_v61 (Compatibilidad MM82)
    cur.execute("DROP VIEW IF EXISTS macro_dossier_v61;")
    cur.execute("""
    CREATE VIEW macro_dossier_v61 AS
    SELECT m.*, s.seal_id AS last_seal
    FROM macro_dossier m
    LEFT JOIN m82_ledger_seals_v2 s ON s.record_id = CAST(m.id AS TEXT);
    """)

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    res = cur.execute("PRAGMA wal_checkpoint;").fetchall()
    conn.close()
    print(f"🟢 [DDL SUCCESS] m82_ledger_seals_v2 e vista macro_dossier_v61 instituidas | WAL Status: {res}")

if __name__ == "__main__":
    apply_ddl_and_seal()
