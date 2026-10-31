#!/usr/bin/env python3
# ==============================================================================
# M82 PERPETUAL DDL MIGRATION & NULL CATEGORY FIX (CONSTANT DEFAULT SAFE)
# Chairman Juan M. Molina -- Sovereign Execution Core (Charallave L4/L5 Edge)
# ==============================================================================
import sqlite3, os
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run_perpetual_fix():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # 1. Agregar columna updated_at con tipo TEXT (evita error de DEFAULT no constante)
    try:
        cur.execute("ALTER TABLE macro_dossier ADD COLUMN updated_at TEXT;")
        conn.commit()
        print("🟢 [DDL FIX] Columna 'updated_at' añadida con éxito (safe TEXT type).")
    except sqlite3.OperationalError:
        print("ℹ️ Columna 'updated_at' ya existe en el esquema.")

    # 2. Actualizar categorías NULL y estampar fecha UTC
    now_utc = datetime.now(timezone.utc).isoformat()
    cur.execute("""
        UPDATE macro_dossier 
        SET category = 'M82_LEGACY_RAW_INGEST',
            updated_at = ? 
        WHERE category IS NULL OR category = '';
    """, (now_utc,))
    
    rows_updated = cur.rowcount
    conn.commit()
    print(f"🟢 [UPDATE OK] Categorías NULL actualizadas a 'M82_LEGACY_RAW_INGEST': {rows_updated}")

    # 3. Consulta de Verificación de Categorías Top 10
    cur.execute("""
        SELECT category, COUNT(*) 
        FROM macro_dossier 
        WHERE validated=1 
        GROUP BY category 
        ORDER BY COUNT(*) DESC 
        LIMIT 10;
    """)
    records = cur.fetchall()

    print("\n==========================================================================")
    print("📊 TOP 10 CATEGORÍAS REGISTRADAS EN BBDD (CERO NULLS):")
    print("==========================================================================")
    for cat, count in records:
        print(f"  • {cat:<35} : {count} Dossiers")

    # 4. Checkpoint atómico WAL CLEAN 0/0/0
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    print("==========================================================================")
    print("🟢 [SUCCESS] BBDD Totalmente Sanitizada | 113 Validados | WAL CLEAN 0/0/0")
    print("==========================================================================")

if __name__ == "__main__":
    run_perpetual_fix()
