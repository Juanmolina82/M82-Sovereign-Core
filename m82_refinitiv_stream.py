#!/usr/bin/env python3
import os, sys, time, json, sqlite3, requests
from datetime import datetime, timezone

M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
VAULT_PATH = os.path.join(M82_DIR, "vault/protected/vault.json")

def get_lseg_credentials():
    client_id = "a404050A11740359473F5E70042D524581e"
    user = "jmmp@molina82.com"
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r") as f:
                data = json.load(f)
                client_id = data.get("LSEG_APP_KEY_PRIMARY", client_id)
                user = data.get("LSEG_USER", user)
        except Exception: pass
    return client_id, user

def get_rdp_token(client_id, user):
    url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "scope": "tra.RDP",
        "username": user
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        res = requests.post(url, data=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json().get("access_token")
        else:
            # Fallback simple sin username si la política de la app key es estricta
            payload_simple = {"grant_type": "client_credentials", "client_id": client_id, "scope": "tra.RDP"}
            res_s = requests.post(url, data=payload_simple, headers=headers, timeout=10)
            if res_s.status_code == 200:
                return res_s.json().get("access_token")
    except Exception as e:
        print(f"⚠️ [M82 LSEG] Auth Error: {e}")
    return None

def fetch_lseg_wire(token):
    url = "https://api.refinitiv.com/data/news/v1/stories/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "query": "Topic:FRENCH_DEBT OR Topic:ICSID OR Venezuela OR Topic:ENERGY OR Topic:EQUITY",
        "sort": "date desc",
        "count": 20
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            stories = res.json().get("stories", [])
            return [{"time": s.get("versionCreated"), "headline": s.get("title", {}).get("text", "")} for s in stories if s.get("title", {}).get("text")]
    except Exception as e:
        print(f"⚠️ [M82 LSEG] Fetch Error: {e}")
    return []

def inject_to_wal(records):
    if not os.path.exists(DB_PATH): return 0
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    new_items = 0
    for r in records:
        headline = f"[M82] {r['headline']}"
        try:
            c.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES (?, ?, 'PENDING')", ("LSEG_RAW_STREAM", headline))
            new_items += 1
        except sqlite3.IntegrityError: pass
    conn.commit()
    conn.close()
    return new_items

if __name__ == "__main__":
    print("⚡ [M82] INICIANDO STREAM EN CRUDO DESDE REFINITIV WORKSPACE (LSEG RDP)")
    client_id, user = get_lseg_credentials()
    while True:
        token = get_rdp_token(client_id, user)
        now_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        if token:
            records = fetch_lseg_wire(token)
            inserted = inject_to_wal(records)
            print(f"[{now_str}] 🟢 LSEG Stream Pull OK :: {len(records)} cables recibidos | {inserted} nuevos inyectados.")
            for rec in records[:3]:
                print(f"   └── 📰 {rec['time']} | {rec['headline']}")
        else:
            print(f"[{now_str}] ⚠️ RDP Auth fallback (usando puente WAL activo). Reintentando en 60s...")
        time.sleep(60)
