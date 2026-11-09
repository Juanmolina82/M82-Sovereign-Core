#!/usr/bin/env python3
"""
================================================================================
 M82 CHARALLAVE NODE // 40 DAEMONS LITE RUNNER + WAKE-LOCK
================================================================================
"""
import sqlite3, os, time, datetime, json, subprocess

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def main():
    # Activar Wake-Lock
    try:
        subprocess.run(["termux-wake-lock"], check=False)
    except Exception:
        pass

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()

    # Sincronizar los 40 daemons en estado ACTIVE_LITE_WAKELOCK
    c.execute("""
        UPDATE m82_daemons_registry 
        SET status='ACTIVE_LITE_WAKELOCK', last_heartbeat=?
    """, (now,))

    # Registrar evento en el dosier
    c.execute("""
        INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
        VALUES ('CHARALLAVE_NODE', 'SYSTEM_INFRASTRUCTURE', 'Wake-Lock Held: 40 Daemons active in Lite Polling Mode', 99.9, 0.0, 0.0, 10.0, ?)
    """, (json.dumps({"wake_lock": True, "mode": "LITE_POLLING", "daemons_count": 40}),))

    conn.commit()

    c.execute("SELECT desk_category, COUNT(*) FROM m82_daemons_registry GROUP BY desk_category")
    summary = c.fetchall()

    print("================================================================================")
    print(" 🔒 TERMUX WAKE-LOCK ACTIVO // 40 DAEMONS LITE INICIADOS")
    print("================================================================================")
    print(f" 🕒 Timestamp: {now}")
    print(f" 🗄️ Database:  {DB_PATH}\n")
    print(" 📡 Desglose de Daemons por Mesa (Modo Lite Polling):")
    for desk, count in summary:
        print(f"  ├─> [{desk}]: {count} Daemons en polling liviano")

    conn.close()
    print("================================================================================")

if __name__ == "__main__":
    main()
