import sqlite3
import pathlib

DB_PATH = pathlib.Path.home() / 'M82' / 'm82_database.db'

def update_telemetry():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=60000;")
    
    # Insertar/Actualizar vector DELL.N con datos Refinitiv Workspace
    cursor.execute("""
        INSERT OR REPLACE INTO m82_live_prices (ticker, spot, fcf, ev_ebitda, forward_pe, updated_at)
        VALUES ('DELL.N', 118.50, 6.49, 10.35, 14.35, CURRENT_TIMESTAMP);
    """)
    
    conn.commit()
    conn.close()
    print("[M82 INGEST OK] ✅ Vectores de Refinitiv Workspace inyectados en SQLite3 WAL Mode.")

if __name__ == '__main__':
    update_telemetry()
