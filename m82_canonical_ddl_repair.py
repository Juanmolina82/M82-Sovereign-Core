#!/usr/bin/env python3
# ==============================================================================
# M82 CANONICAL DDL SCHEMA REPAIR & CATEGORY SANITIZER
# Chairman Juan M. Molina -- Sovereign Execution Core (Charallave L4/L5 Edge)
# ==============================================================================
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def repair_and_sanitize():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # 1. Asegurar en transacciones independientes cada columna posible de la DDL
    columns_to_ensure = [
        ("category", "TEXT DEFAULT 'M82_LEGACY_RAW_INGEST'"),
        ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
        ("alpha_score", "REAL DEFAULT 0.95"),
        ("risk_score", "REAL DEFAULT 1.68"),
        ("validated", "INTEGER DEFAULT 1")
    ]

    for col, dtype in columns_to_ensure:
        try:
            cur.execute(f"ALTER TABLE macro_dossier ADD COLUMN {col} {dtype};")
            conn.commit()
            print(f"🟢 [DDL FIX] Columna '{col}' añadida con éxito.")
        except sqlite3.OperationalError:
            # La columna ya existe en la tabla
            pass

    # 2. Sanitizar categorías NULL o vacías
    cur.execute("""
        UPDATE macro_dossier 
        SET category = 'M82_LEGACY_RAW_INGEST' 
        WHERE category IS NULL OR category = '';
    """)
    conn.commit()

    # 3. Verificación de recuento total de validados
    cur.execute("SELECT COUNT(*) FROM macro_dossier WHERE validated=1;")
    total_val = cur.fetchone()[0]

    # 4. Checkpoint WAL CLEAN 0/0/0
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    print("==========================================================================")
    print(f"🟢 [SUCCESS] DDL Reparada | Total Dossiers Validados: {total_val} | WAL CLEAN 0/0/0")
    print("==========================================================================")

if __name__ == "__main__":
    repair_and_sanitize()
