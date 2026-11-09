#!/usr/bin/env python3
import requests, sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")
USER_ID = "jmmp@molina82.com"
USER_PASS = "Trader2026****"
APP_KEY = "612627233d454619b06820ef0545d14"

brent_val, wti_val = 106.77, 93.94
is_live = False

try:
    auth_url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    payload = {
        "username": USER_ID,
        "password": USER_PASS,
        "grant_type": "password",
        "client_id": APP_KEY,
        "takeExclusiveSignOnControl": "true"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    auth_res = requests.post(auth_url, data=payload, headers=headers, timeout=5)
    
    if auth_res.status_code == 200:
        token = auth_res.json().get("access_token")
        pricing_url = "https://api.refinitiv.com/data/pricing/snapshots/v1/views/scores"
        params = {"universe": "LCOc1,CLc1", "fields": "CF_LAST"}
        data_headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        
        data_res = requests.get(pricing_url, headers=data_headers, params=params, timeout=5)
        if data_res.status_code == 200:
            res_json = data_res.json()
            for row in res_json.get("data", []):
                inst = row.get("universe")
                val = row.get("fields", {}).get("CF_LAST")
                if inst == "LCOc1" and val is not None:
                    brent_val = float(val)
                elif inst == "CLc1" and val is not None:
                    wti_val = float(val)
            is_live = True
except Exception:
    pass

tag = "LIVE" if is_live else "SNAPSHOT"
print(f"📊 M82_MACRO {tag}: Brent ${brent_val:.2f} | WTI ${wti_val:.2f}")

conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS m82_multi_stream (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daemon_source TEXT,
        headline TEXT UNIQUE,
        status TEXT,
        timestamp TEXT
    )
""")

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
headline_str = f"M82_MACRO TICK ({tag}): Brent {brent_val:.2f} WTI {wti_val:.2f} - Fisico VE {(brent_val+13.18):.2f} [{now}]"

# Usa INSERT OR REPLACE para ignorar o actualizar si el titular choca con la restricción UNIQUE
c.execute("""
    INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES ('M82_MACRO_LIVE_FEED', ?, 'PENDING', ?)
""", (headline_str, now))

conn.commit()
conn.close()
print("✅ Ingesta M82_MACRO procesada con éxito sin errores de base de datos.")
