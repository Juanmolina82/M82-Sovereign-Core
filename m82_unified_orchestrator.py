#!/usr/bin/env python3
import time
from m82_db import execute_query

def main():
    print("🚀 [M82 SINGLE-CORE ORCHESTRATOR] Operativo en un solo hilo.", flush=True)
    while True:
        try:
            # Procesar tareas
            execute_query("INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status) VALUES ('M82_HEARTBEAT', 'CRON_HEARTBEAT_OK', 'PROCESSED');")
            print(f"[{time.strftime('%H:%M:%S')}] Heartbeat M82 OK", flush=True)
        except Exception as e:
            print(f"⚠️ Error orquestador: {e}", flush=True)
        time.sleep(30)

if __name__ == "__main__":
    main()
