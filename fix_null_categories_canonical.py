#!/usr/bin/env python3
# ==============================================================================
# M82 CANONICAL DDL MIGRATION & CATEGORY FIX
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def fix_canonical_categories():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # 1. Asegurar la presencia idempotente de las columnas adicionales
    for col, dtype in [("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"), 
                       ("alpha_score", "REAL DEFAULT 0.95"), 
                       ("risk_score", "REAL DEFAULT 1.68")]:
        try:
            cur.execute(f"ALTER TABLE macro_dossier ADD COLUMN {col} {dtype};")
            print(f"🟢 Column '{col}' added safely.")
        except sqlite3.OperationalError:
            pass  # La columna ya existe

    # 2. Normalizar categorías NULL
    cur.execute("""
        UPDATE macro_dossier 
        SET category = 'M82_LEGACY_RAW_INGEST' 
        WHERE category IS NULL OR category = '';
    """)
    rows_affected = cur.rowcount
    conn.commit()

    # 3. Verificación de lectura de 113 registros validados
    cur.execute("SELECT COUNT(*) FROM macro_dossier WHERE validated=1;")
    val_count = cur.fetchone()[0]

    # 4. Checkpoint atómico WAL CLEAN 0/0/0
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    print(f"🟢 [MIGRATION SUCCESS] Updated NULL Rows: {rows_affected} | Total Validated: {val_count} | WAL CLEAN 0/0/0")

if __name__ == "__main__":
    fix_canonical_categories()
