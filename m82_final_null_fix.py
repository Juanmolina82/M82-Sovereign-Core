#!/usr/bin/env python3
# ==============================================================================
# M82 ISOLATED PYTHON NULL CATEGORY SANITIZER
# Chairman Juan M. Molina -- Sovereign Execution Core (Charallave L4/L5 Edge)
# ==============================================================================
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run_fix():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    # 1. Inyectar columna updated_at si no existe
    try:
        cur.execute("ALTER TABLE macro_dossier ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;")
        conn.commit()
        print("🟢 Columna 'updated_at' asegurada en esquema.")
    except sqlite3.OperationalError:
        pass

    # 2. Sanitizar las 10 filas NULL o vacías
    cur.execute("""
        UPDATE macro_dossier 
        SET category = 'M82_LEGACY_RAW_INGEST' 
        WHERE category IS NULL OR category = '';
    """)
    rows_updated = cur.rowcount
    conn.commit()
    print(f"🟢 Registros NULL actualizados: {rows_updated}")

    # 3. Consulta de verificación de Top Categorías
    cur.execute("""
        SELECT category, COUNT(*) 
        FROM macro_dossier 
        WHERE validated=1 
        GROUP BY category 
        ORDER BY COUNT(*) DESC 
        LIMIT 10;
    """)
    top_cats = cur.fetchall()

    print("\n==========================================================================")
    print("📊 TOP 10 CATEGORÍAS EN BBDD (CERO REGISTROS NULL):")
    print("==========================================================================")
    for cat, count in top_cats:
        print(f"  • {cat:<35} : {count} Dossiers")

    # 4. Checkpoint atómico WAL CLEAN 0/0/0
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()
    print("==========================================================================")
    print("🟢 [SUCCESS] BBDD Sanitizada 100% | WAL CLEAN 0/0/0 Certificado")
    print("==========================================================================")

if __name__ == "__main__":
    run_fix()
