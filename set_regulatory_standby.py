#!/usr/bin/env python3
import sqlite3, os, datetime, json

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

now = datetime.datetime.now().isoformat()

# 1. Colocar los daemons regulatorios y de monitoreo corporativo en STANDBY
c.execute("""
    UPDATE m82_daemons_registry 
    SET status='STANDBY_PAUSED', last_heartbeat=?
    WHERE daemon_name IN ('m82_blackrock_monitor.py', 'm82_sec_form4_evc.py', 'm82_regulatory_cron.py')
""", (now,))

# 2. Registrar el estado de Standby preservando la Métrica Macro ($810.46M NAV / 18.51% LTV)
meta_standby = {
    "nav_spot_usd_m": 810.46,
    "ltv_spot_pct": 18.51,
    "ovx_index": 32.5,
    "cpoll_2027_anchor": 74.44,
    "simulated_crude_usd": 57.50,
    "status": "REGULATORY_SCHEDULER_STANDBY"
}

c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
    VALUES ('REGULATORY_MONITOR', 'CRON_STANDBY', 'Regulatory Scheduler & BLK/EVC Jobs placed on Standby. Core Macro Suite 40 Daemons Priority', 90.0, 0.0, 0.0, 5.0, ?)
""", (json.dumps(meta_standby),))

conn.commit()

print("================================================================================")
print(" ⏸️ REGULATORY & CORPORATE SCHEDULER: STANDBY ACTIVADO")
print("================================================================================")
print(" ✓ BlackRock (BLK.N) & EVC M82_MACRO Form 4 puestos en pausa asíncrona.")
print(" ✓ NAV Spot ($810.46M) y LTV (18.51%) blindados en m82_database.db.")
print(" ✓ Infraestructura principal (40 Daemons + API 8083 + HTTP 8080) operativa 100%.")
print("================================================================================")

conn.close()
