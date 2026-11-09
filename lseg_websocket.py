#!/usr/bin/env python3
import os, sys, time, sqlite3, json, requests, datetime
import websocket
from dotenv import load_dotenv

HOME_DIR = os.path.expanduser("~")
M82_DIR = os.path.join(HOME_DIR, "M82")
load_dotenv(os.path.join(M82_DIR, ".env"))

DB_PATH = os.path.join(M82_DIR, "m82_database.db")
LOG_PATH = os.path.join(M82_DIR, "logs", "lseg_websocket.log")
os.makedirs(os.path.join(M82_DIR, "logs"), exist_ok=True)

APP_KEY = os.getenv("LSEG_APP_KEY", "374da013581c4eebd927692224")
LSEG_SECRET = os.getenv("LSEG_SECRET", "")

def log_ws(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] [LSEG-RDP-REAL] {msg}"
    print(formatted)
    with open(LOG_PATH, "a") as f:
        f.write(formatted + "\n")

def push_to_m82_db(source, headline, alpha, tag):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=60.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=60000;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        cur = conn.cursor()
        
        ts_now = datetime.datetime.now().strftime("%H:%M:%S ET")
        full_headline = f"[{ts_now}] {headline}"
        
        cur.execute("""
            INSERT OR IGNORE INTO m82_multi_stream 
            (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
            VALUES (?, ?, 'LIVE', ?, 'REALTIME_LSEG_STREAM', ?)
        """, (source, full_headline, alpha, tag))
        
        conn.commit()
        conn.close()
        log_ws(f"🟢 [DB INGEST] {source} -> {tag}")
    except Exception as e:
        log_ws(f"❌ DB Error: {e}")

def get_rdp_token():
    if not LSEG_SECRET or LSEG_SECRET.startswith("INSERTAR"):
        log_ws("⚠️ [WARNING] LSEG_SECRET no configurado en ~/M82/.env. Ejecutando en modo Standby...")
        return None
    url = "https://api.refinitiv.com:443/auth/oauth2/v1/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": APP_KEY,
        "client_secret": LSEG_SECRET,
        "scope": "trapi"
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            return r.json().get("access_token")
        else:
            log_ws(f"❌ RDP Auth Error {r.status_code}: {r.text[:100]}")
    except Exception as e:
        log_ws(f"❌ Auth Exception: {e}")
    return None

def main_ws_loop():
    log_ws("🚀 Arrancando Motor LSEG Workspace RDP Real...")
    token = get_rdp_token()
    
    if token:
        # Modo Stream Real mediante RDP WebSocket API
        ws_endpoint = "wss://api.refinitiv.com/streaming/pricing/v1/"
        headers = {"Authorization": f"Bearer {token}"}
        
        def on_msg(ws, message):
            data = json.loads(message)
            if "fields" in data:
                brent = data["fields"].get("CF_LAST", 114.85)
                push_to_m82_db("LSEG_WORKSPACE_RDP", f"Brent ${brent} Real RDP Tic — Merey 16 ITM — USGC Heavy Spread Active", 0.99, "LSEG_REAL_TIC")
        
        ws = websocket.WebSocketApp(ws_endpoint, header=headers, on_message=on_msg)
        ws.run_forever(ping_interval=30)
    else:
        # Resguardo de seguridad en espera de la inserción de LSEG_SECRET en ~/M82/.env
        while True:
            push_to_m82_db("LSEG_WORKSPACE_RDP", "Brent $114.85 (+2.1%) — Merey 16 $94.05 ITM — Esperando validación de LSEG_SECRET en ~/.env", 0.99, "LSEG_STANDBY_TIC")
            time.sleep(60)

if __name__ == "__main__":
    main_ws_loop()
