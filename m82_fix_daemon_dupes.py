#!/usr/bin/env python3
import os, sqlite3

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def fix_duplicates():
    if not os.path.exists(DB_PATH):
        print("❌ DB no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    c.execute("PRAGMA journal_mode=WAL;")

    # 1. Limpiar registros idénticos repetidos manteniendo solo el último ID
    c.execute("""
        DELETE FROM m82_multi_stream 
        WHERE id NOT IN (
            SELECT MAX(id) 
            FROM m82_multi_stream 
            GROUP BY headline
        );
    """)
    deleted = c.rowcount
    conn.commit()
    conn.close()
    print(f"🧹 Limpieza completada: {deleted} registros repetidos eliminados de m82_database.db")

if __name__ == "__main__":
    # Matar demonios viejos generando bucles
    os.system("pkill -f m82_refinitiv_chartboard_daemon.py || true")
    fix_duplicates()
