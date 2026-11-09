#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def fix_and_run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    c = conn.cursor()

    print("🔧 [M82 SCHEMA REPAIR] Verificando columnas de m82_mcm_checklist...")
    
    # 1. Obtener columnas actuales
    c.execute("PRAGMA table_info(m82_mcm_checklist);")
    cols = [column[1] for column in c.fetchall()]

    # 2. Agregar columna faltante si es necesario
    if "diesel_shortage_active" not in cols and "diesel_shock_active" not in cols:
        c.execute("ALTER TABLE m82_mcm_checklist ADD COLUMN diesel_shortage_active INTEGER DEFAULT 1;")
        print("   -> Columna 'diesel_shortage_active' agregada con éxito.")
    elif "diesel_shock_active" in cols and "diesel_shortage_active" not in cols:
        c.execute("ALTER TABLE m82_mcm_checklist RENAME COLUMN diesel_shock_active TO diesel_shortage_active;")
        print("   -> Columna renombrada a 'diesel_shortage_active' para alineación total.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_and_run()
