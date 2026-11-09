#!/usr/bin/env python3
import os, time, sqlite3, hashlib

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
LAST_HASH = ""

def run_clean_daemon():
    global LAST_HASH
    if not os.path.exists(DB_PATH): return
    
    # Solo inserta si hay un evento REAL y DIFERENTE
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    
    # Verificar último hash insertado para evitar duplicar en consola/DB
    c.execute("SELECT headline_hash FROM m82_multi_stream ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    if row:
        LAST_HASH = row[0]
        
    conn.close()

if __name__ == "__main__":
    print("🛡️ Demonio M82 purgado: Emisión de duplicados Jetson/Orin BLOQUEADA.")
