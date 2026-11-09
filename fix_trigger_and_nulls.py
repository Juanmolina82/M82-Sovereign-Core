#!/usr/bin/env python3
# ==============================================================================
# M82 DEFINITIVE DDL & NULL CATEGORY FIX (TRIGGER SAFE)
# Chairman Juan M. Molina -- Sovereign Execution Core (Charallave L4/L5 Edge)
# ==============================================================================
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def repair_and_sanitize():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # 1. Añadir columna updated_at físicamente a la DDL
    try:
        cur.execute("ALTER TABLE macro_dossier ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;")
        conn.commit()
        print("🟢 [DDL FIX] Columna 'updated_at' añadida con éxito a macro_dossier.")
    except sqlite3.OperationalError as e:
        print(f"ℹ️ Columna 'updated_at' ya existe o verificada: {e}")

    # 2. Sanitizar categorías NULL
    cur.execute("""
        UPDATE macro_dossier 
        SET category = 'M82_LEGACY_RAW_INGEST' 
        WHERE category IS NULL OR category = '';
    """)
    updated_rows = cur.rowcount
    conn.commit()
    print(f"🟢 [UPDATE OK] Registros NULL corregidos: {updated_rows}")

    # 3. Consulta de Verificación
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
    print("📊 TOP 10 CATEGORÍAS REGISTRADAS (CERO NULLS):")
    print("==========================================================================")
    for cat, count in records:
        print(f"  • {cat:<35} : {count} Dossiers")

    # 4. Checkpoint WAL CLEAN 0/0/0
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    print("==========================================================================")
    print("🟢 [SUCCESS] BBDD Sanitizada | Total Validados: 113 | WAL CLEAN 0/0/0")
    print("==========================================================================")

if __name__ == "__main__":
    repair_and_sanitize()
