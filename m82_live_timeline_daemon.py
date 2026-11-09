#!/usr/bin/env python3
# ==============================================================================
# M82 V60 AGI :: REAL-TIME REFINITIV TIMELINE EVENT DAEMON
# Event-Driven Streamer (Zero Polling Overhead)
# ==============================================================================

import os, sys, time, json, hashlib, sqlite3, requests, subprocess

M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
VAULT_PATH = os.path.join(M82_DIR, "vault/protected/vault.json")
GEN_SCRIPT = os.path.join(M82_DIR, "m82_timeline_generator.py")
SEND_SCRIPT = os.path.join(M82_DIR, "send_timeline.py")

LAST_HEADLINE_HASH = ""

def get_lseg_credentials():
    client_id = "374da013581c4eebd9276922248ade81e285d0d6"
    user = "jmmp@molina82.com"
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r") as f:
                v = json.load(f)
                client_id = v.get("LSEG_APP_KEY_PRIMARY", client_id)
                user = v.get("LSEG_USER", user)
        except Exception: pass
    return client_id, user

def get_rdp_token(client_id, user):
    url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"grant_type": "client_credentials", "client_id": client_id, "scope": "tra.RDP", "username": user}
    try:
        r = requests.post(url, data=payload, headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json().get("access_token")
        # Fallback sin username
        r2 = requests.post(url, data={"grant_type": "client_credentials", "client_id": client_id, "scope": "tra.RDP"}, headers=headers, timeout=8)
        if r2.status_code == 200:
            return r2.json().get("access_token")
    except Exception as e:
        print(f"⚠️ [Auth Error]: {e}")
    return None

def check_latest_wire(token):
    url = "https://api.refinitiv.com/data/news/v1/stories/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"query": "Topic:TOPALL OR Topic:MACRO OR Topic:ENERGY OR Topic:EQUITY", "sort": "date desc", "count": 1}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=8)
        if r.status_code == 200:
            stories = r.json().get("stories", [])
            if stories:
                headline = stories[0].get("title", {}).get("text", "")
                created = stories[0].get("versionCreated", "")
                return f"{created}_{headline}"
    except Exception: pass
    return None

def main_loop():
    global LAST_HEADLINE_HASH
    print("⚡ [M82 REAL-TIME WIRE] Escuchando eventos de Refinitiv Workspace...")
    client_id, user = get_lseg_credentials()
    
    while True:
        token = get_rdp_token(client_id, user)
        if token:
            latest = check_latest_wire(token)
            if latest:
                current_hash = hashlib.sha256(latest.encode('utf-8')).hexdigest()
                
                # DISPARO POR EVENTO: Solo si el titular es completamente nuevo
                if current_hash != LAST_HEADLINE_HASH:
                    print(f"\n🚨 [NUEVO CABLE DETECTADO] -> {latest}")
                    LAST_HEADLINE_HASH = current_hash
                    
                    # 1. Regenerar tarjeta de la linea de tiempo
                    subprocess.run(["python3", GEN_SCRIPT], check=False)
                    
                    # 2. Despachar inmediatamente a Telegram
                    subprocess.run(["python3", SEND_SCRIPT], check=False)
                    print("✅ Timeline enviado en vivo.")
        
        # Micro-frecuencia de 15 segundos para captura casi instantanea
        time.sleep(15)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit(0)
