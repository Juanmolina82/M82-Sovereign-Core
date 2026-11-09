#!/usr/bin/env python3
import os, shutil, time, sqlite3

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
BACKUP_DIR = "/sdcard/M82_Backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_sqlite():
    if os.path.exists(DB_PATH):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"m82_database_{timestamp}.db")
        try:
            # Respaldo seguro en caliente con SQLite
            src_conn = sqlite3.connect(DB_PATH)
            dst_conn = sqlite3.connect(backup_file)
            with dst_conn:
                src_conn.backup(dst_conn)
            dst_conn.close()
            src_conn.close()
            print(f"🔒 [PERSISTENCIA] Base de datos respaldada en storage externo: {backup_file}")
        except Exception as e:
            print(f"⚠️ Error respaldando BD: {e}")

if __name__ == "__main__":
    backup_sqlite()
