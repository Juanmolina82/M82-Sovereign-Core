#!/usr/bin/env python3
import json
import os
import sqlite3
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
ENV_PATH = os.path.expanduser("~/M82/.env")
HUB_8286 = "http://127.0.0.1:8286/api/ingest"

# Universo completo extraído del Terminal LSEG Workspace de jmmp@molina82.com
UNIVERSE_RICS = [
    ".SPX", ".IXIC", ".NDX", ".DJI", ".DJT", ".RUT", ".VIX",
    ".SPLRCS", ".SPLRCL", ".SPXHC", ".SPNY", ".SPLRCT", ".IVX", ".SPXEW",
    ".STOXX50E", ".GDAXI", ".FCHI", ".FTEU3",
    "US2US10=TWEB", "US10YT=RR", "TYcv1", "EScv1", "NQcv1", "YMcv1", "RTYcv1",
    "XAU=", "XAG=", "LCOc1", "CLc1", "HGc1", "BTC=", "EUR=", "GBP=", "JPY=", "CNH=", ".DXY",
    "NVDA.O", "PANW.O", "HPE.N", "PG.N"
]

def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def get_wal_conn():
    conn = sqlite3.connect(DB_PATH, timeout=120.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def get_rdp_token(username: str, password: str, app_key: str) -> str:
    url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    body = urllib.parse.urlencode({
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": app_key,
        "takeExclusiveSignOnControl": "true",
        "scope": "trapi"
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]

def pull_lseg_pricing(token: str):
    rics_param = urllib.parse.quote(",".join(UNIVERSE_RICS))
    url = f"https://api.refinitiv.com/data/pricing/snapshots/v1/?universe={rics_param}&fields=CF_LAST,CF_NETCHNG,PCTCHNG,CF_HIGH,CF_LOW"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def pull_lseg_news(token: str):
    url = "https://api.refinitiv.com/data/news/v1/headlines?query=S%26P%20500%20OR%20AI%20OR%20Oil%20OR%20Fed&limit=10"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def ingest_cycle():
    load_env()
    user = os.getenv("LSEG_USERNAME", "jmmp@molina82.com")
    pwd = os.getenv("LSEG_PASSWORD", "")
    app_key = os.getenv("LSEG_APP_KEY", "")
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    conn = get_wal_conn()
    if not pwd or not app_key:
        msg = f"[{now_utc}] [LSEG_CLOUD_RDP_STANDBY] User {user} listo — configure LSEG_PASSWORD y LSEG_APP_KEY en ~/M82/.env"
        conn.execute(
            "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES ('LSEG_RDP_CLOUD_JMMP', ?, 'PENDING', 0.90, 'LSEG_AUTH_READY', 'AWAITING_ENV_KEY')",
            (msg,),
        )
        conn.close()
        print(msg)
        return

    try:
        token = get_rdp_token(user, pwd, app_key)
        snap = pull_lseg_pricing(token)
        rows = snap.get("data", [])
        summary_ticks = []
        for item in rows[:12]:
            ric = item.get("universe", "")
            f = item.get("fields", {})
            last = f.get("CF_LAST")
            pct = f.get("PCTCHNG")
            if last is not None:
                summary_ticks.append(f"{ric}:{last}({pct}%)")

        headline = f"[{now_utc}] [LSEG_CLOUD_LIVE | {user}] " + " | ".join(summary_ticks) + " | BUNKER 0.30x LOCK"
        conn.execute(
            "INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, alpha_score) VALUES ('LSEG_RDP_CLOUD_LIVE', 'WORKSPACE_STREAM_JMMP', ?, 1.65, 'BUNKER_HOLD_030X', -0.25, ?, 0.97)",
            (headline, json.dumps({"user": user, "rics_count": len(rows), "ts": now_utc})),
        )
        conn.execute(
            "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES ('LSEG_RDP_CLOUD_JMMP', ?, 'VERIFIED', 0.97, 'LSEG_LIVE_UNIVERSE', 'RDP_STREAM_TICK')",
            (headline,),
        )

        # Ingesta de titulares Live Markets / Reuters desde LSEG Cloud
        news_data = pull_lseg_news(token)
        for art in news_data.get("data", [])[:5]:
            ntitle = art.get("newsItem", {}).get("itemMeta", {}).get("title", [{}])[0].get("$", "")
            if ntitle:
                nhl = f"[{now_utc}] [LSEG_MRN_WIRE] {ntitle}"
                conn.execute(
                    "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger) VALUES ('LSEG_NEWS_DAEMON', ?, 'VERIFIED', 0.91, 'LSEG_LIVE_MARKETS', 'MRN_HEADLINE')",
                    (nhl,),
                )

        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        print(f"🟢 [{now_utc}] LSEG CLOUD INGESTED ({len(rows)} RICs) -> {user}")
    except Exception as e:
        print(f"⚠️ [{now_utc}] LSEG RDP Cloud retry: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        ingest_cycle()
        time.sleep(60)
