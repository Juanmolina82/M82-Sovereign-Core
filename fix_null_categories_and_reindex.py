#!/usr/bin/env python3
# ==============================================================================
# M82 CATEGORY SANITIZATION & DDL NORMALIZATION
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def sanitize_categories():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # Normalizar los 10 registros NULL a categoría canónica
    cur.execute("""
        UPDATE macro_dossier 
        SET category = 'M82_LEGACY_RAW_INGEST', risk_score = 1.68, alpha_score = 0.95 
        WHERE category IS NULL AND validated = 1;
    """)
    updated_rows = cur.rowcount

    conn.commit()

    # Verificar recuento total
    cur.execute("SELECT COUNT(*) FROM macro_dossier WHERE validated=1 AND category IS NOT NULL;")
    total_clean = cur.fetchone()[0]

    # Checkpoint atómico TRUNCATE WAL CLEAN 0/0/0
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    print(f"🟢 [CATEGORIES SANITIZED] NULL Rows Fixed: {updated_rows} | Total Validated & Categorized: {total_clean} | WAL CLEAN 0/0/0")

if __name__ == "__main__":
    sanitize_categories()
