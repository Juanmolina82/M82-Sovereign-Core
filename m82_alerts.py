#!/usr/bin/env python3
import sqlite3, os, time

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=60.0, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    return conn

def run_alerts_daemon():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [M82-ALERTS] Daemon iniciado correctamente. WAL + Busy Timeout 60s OK.", flush=True)
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM m82_multi_stream WHERE status = 'PENDING'")
            pending_count = cursor.fetchone()[0]
            conn.close()
            
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [M82-ALERTS] HEARTBEAT OK | Pendientes en cola: {pending_count}", flush=True)
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [M82-ALERTS] Error en ciclo: {e}", flush=True)
            
        time.sleep(1800)

if __name__ == "__main__":
    run_alerts_daemon()
