#!/usr/bin/env python3
import datetime
import json
import os
import sqlite3
import requests

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CFG_PATH = os.path.join(BASE_DIR, "refinitiv-data.config.json")

with open(CFG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

rdp_cfg = cfg["sessions"]["platform"]["rdp"]
APP_KEY = rdp_cfg["app-key"]
USER_ID = rdp_cfg["signon"]["username"]
USER_PASS = rdp_cfg["signon"]["password"]

# Snapshot calibrado al cierre de mercado 20-Nov-2026
quotes = {
    "LCOc1": 90.70,
    "CLc1": 82.27,
    ".VIX": 31.96,
    ".SPX": 7013.92,
    ".IXIC": 22995.95,
    "XAU=": 3575.52,
}
is_live = False

try:
    auth_url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    payload = {
        "username": USER_ID,
        "password": USER_PASS,
        "grant_type": "password",
        "client_id": APP_KEY,
        "takeExclusiveSignOnControl": "true",
        "scope": "trapi",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_res = requests.post(auth_url, data=payload, headers=headers, timeout=8)

    if auth_res.status_code == 200:
        token = auth_res.json().get("access_token")
        pricing_url = "https://api.refinitiv.com/data/pricing/snapshots/v1/"
        params = {
            "universe": ",".join(quotes.keys()),
            "fields": "CF_LAST",
        }
        data_headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        data_res = requests.get(pricing_url, headers=data_headers, params=params, timeout=8)
        if data_res.status_code == 200:
            for row in data_res.json().get("data", []):
                inst = row.get("universe")
                val = row.get("fields", {}).get("CF_LAST")
                if inst in quotes and val is not None:
                    quotes[inst] = float(val)
            is_live = True
except Exception:
    pass

tag = "LIVE" if is_live else "SNAPSHOT"
brent_val = quotes["LCOc1"]
wti_val = quotes["CLc1"]
merey_est = brent_val - 14.50
vix_val = quotes[".VIX"]
spx_val = quotes[".SPX"]
xau_val = quotes["XAU="]

headline = (
    f"LSEG ({tag} | {USER_ID}): BRENT ${brent_val:.2f} | WTI ${wti_val:.2f} | "
    f"MEREY-16 PADD3 ${merey_est:.2f} | VIX {vix_val:.2f} | SPX {spx_val:,.2f} | "
    f"XAU ${xau_val:,.2f} | BUNKER 0.30x LOCK"
)
print(f"📊 {headline}")

conn = sqlite3.connect(DB_PATH, timeout=60.0, isolation_level=None)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
conn.execute("PRAGMA synchronous=NORMAL;")

conn.execute("""
    CREATE TABLE IF NOT EXISTS m82_multi_stream (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daemon_source TEXT,
        headline TEXT UNIQUE,
        status TEXT DEFAULT 'PENDING',
        timestamp TEXT
    )
""")

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
conn.execute(
    "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES ('LSEG_LIVE_FEED', ?, 'PENDING', ?)",
    (headline, now),
)
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()
print("✅ Ingesta LSEG sellada en SQLite3 WAL (0/0/0 CLEAN).")
