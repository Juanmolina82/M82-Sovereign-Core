#!/usr/bin/env python3
import os, sqlite3

db_path = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(db_path, timeout=60.0)
cursor = conn.cursor()
cursor.execute("PRAGMA journal_mode=WAL;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS m82_live_prices (
    ticker TEXT PRIMARY KEY,
    spot REAL NOT NULL,
    fcf REAL,
    ev_ebitda REAL,
    forward_pe REAL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()
conn.close()
print("[M82 DATABASE] Tabla 'm82_live_prices' instanciada correctamente en WAL Mode.")
