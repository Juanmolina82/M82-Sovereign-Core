#!/usr/bin/env python3
# ==============================================================================
# M82 V60.3.2 CITADEL :: LPL DOSSIER REGISTRATION & DATABASE INJECTOR
# ==============================================================================

import os, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def register_dossier():
    if not os.path.exists(DB_PATH):
        print("❌ Base de datos no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("PRAGMA journal_mode=WAL;")

    headline = "[INSTITUTIONAL | Caracas HQ] M82 V60.3.2 LPL Dossier compiled — Anthropic $16.8B + BAC $1.2B AML + Refining Margins"
    h_hash = hashlib.sha256(headline.encode()).hexdigest()[:16]

    try:
        c.execute("""
            INSERT INTO m82_multi_stream 
            (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at)
            VALUES ('INSTITUTIONAL', ?, ?, 'Prime Brokerage Gateway', 'VERIFIED', 0.99, 'LPL_DOSSIER_V6032', CURRENT_TIMESTAMP)
        """, (headline, h_hash))
        conn.commit()
        print("📥 Expediente M82 V60.3.2 LPL registrado como VERIFIED con Alpha Score 0.99.")
    except sqlite3.IntegrityError:
        print("⚠️ Expediente ya se encuentra registrado (Hash Duplicate).")

    conn.close()

if __name__ == "__main__":
    register_dossier()
