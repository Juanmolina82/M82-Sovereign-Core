#!/usr/bin/env python3
import os, json, time, sqlite3, hashlib, urllib.request, urllib.parse
from datetime import datetime, timezone

M82_ROOT = os.path.expanduser("~/M82")
ENV_FILE = os.path.join(M82_ROOT, ".env.refinitiv")
ORCH_DB = os.path.join(M82_ROOT, "m82_orchestrator_wal.db")
WATCHLIST_RICS = ["CLc1", "LCOc1", "RBc1", "HOc1", "US10YT=RR", ".DXY"]

def load_vault():
    creds = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    creds[k.strip()] = v.strip().strip('"').strip("'")
    return creds

def authenticate_rdp(creds):
    user = creds.get("REFINITIV_USERNAME", "")
    pwd = creds.get("REFINITIV_PASSWORD", "")
    app_key = creds.get("REFINITIV_APP_KEY", "")
    if not (user and pwd and app_key) or "<TU_" in pwd or "<TU_" in app_key:
        return {"status": "PENDING_VAULT_KEY", "token": None, "user": user}
    try:
        data = urllib.parse.urlencode({
            "username": user,
            "password": pwd,
            "client_id": app_key,
            "grant_type": "password",
            "scope": "trapi",
            "takeExclusiveSignOnControl": "true"
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.refinitiv.com/auth/oauth2/v1/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return {"status": "RDP_OAUTH2_LIVE", "token": payload.get("access_token"), "user": user}
    except Exception as e:
        return {"status": f"AUTH_ERROR:{type(e).__name__}", "token": None, "user": user}

def fetch_realtime_quotes(auth_res):
    now = datetime.now(timezone.utc).isoformat()
    if auth_res["status"] != "RDP_OAUTH2_LIVE" or not auth_res.get("token"):
        return {"mode": auth_res["status"], "quotes": [], "fetched_at": now}
    try:
        rics_param = ",".join(WATCHLIST_RICS)
        url = f"https://api.refinitiv.com/data/pricing/snapshots/v1/?universe={urllib.parse.quote(rics_param)}&fields=BID,ASK,TRDPRC_1,PCTCHNG"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {auth_res['token']}"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            return {"mode": "LSEG_RDP_STREAMING_LIVE", "quotes": raw, "fetched_at": now}
    except Exception as e:
        return {"mode": f"FEED_ERROR:{type(e).__name__}", "quotes": [], "fetched_at": now}

def persist_telemetry(auth_res, feed):
    now = datetime.now(timezone.utc).isoformat()
    fid = f"REF-{hashlib.sha256(now.encode()).hexdigest()[:14]}"
    conn = sqlite3.connect(ORCH_DB, timeout=30.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    try:
        conn.execute("BEGIN IMMEDIATE;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS m82_refinitiv_feed_ledger (
                feed_id TEXT PRIMARY KEY,
                account_user TEXT NOT NULL,
                session_status TEXT NOT NULL,
                rics_list TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                captured_at TEXT NOT NULL
            );
        """)
        conn.execute("INSERT OR REPLACE INTO m82_mcp_registry VALUES (?, ?, ?, ?, ?);",
                     ("mcp.m82.refinitiv_realtime_bridge", "MARKET_STREAM", "Ingesta streaming LSEG/Refinitiv Workspace EDP para Crack Spreads, UST 10Y y DXY bajo BUNKER 0.30x.", "BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK", now))
        conn.execute("INSERT OR REPLACE INTO m82_refinitiv_feed_ledger VALUES (?, ?, ?, ?, ?, ?);",
                     (fid, auth_res.get("user", "jmmp@molina82.com"), feed["mode"], json.dumps(WATCHLIST_RICS), json.dumps(feed["quotes"])[:32000], now))
        conn.execute("COMMIT;")
        print(f"[M82 REFINITIV BRIDGE] User: {auth_res.get('user')} | Estado: {feed['mode']} | RICs: {len(WATCHLIST_RICS)} | ID: {fid}")
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        conn.close()

def main():
    creds = load_vault()
    auth_res = authenticate_rdp(creds)
    feed = fetch_realtime_quotes(auth_res)
    persist_telemetry(auth_res, feed)

if __name__ == "__main__":
    main()
