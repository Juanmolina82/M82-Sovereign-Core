#!/usr/bin/env python3
import requests, json, sqlite3, os

USER_RDP = "jmmp@molina82.com"
PASS_RDP = "Trader2026****"
APP_KEY  = "a404050A24581e"
DB_PATH  = os.path.expanduser("~/M82/m82_database.db")

print("⚡ [M82 LITE] Autenticando directamente en Refinitiv Cloud...")

# 1. Petición OAuth2 Directa Móvil
auth_url = "https://api.refinitiv.com/auth/oauth2/v1/token"
payload = {
    "grant_type": "password",
    "username": USER_RDP,
    "password": PASS_RDP,
    "client_id": APP_KEY,
    "scope": "tra.RDP",
    "takeExclusiveSignOnControl": "true"
}

headers_auth = {"Content-Type": "application/x-www-form-urlencoded"}

try:
    r = requests.post(auth_url, data=payload, headers=headers_auth, timeout=12)
    if r.status_code == 200:
        token = r.json().get("access_token")
        with open(os.path.expanduser("~/M82/.token"), "w") as f:
            f.write(token)
        print(f"🟢 [AUTH OK] Bearer Token generado y cacheado: {token[:20]}...")
    else:
        print(f"⚠️ Error OAuth2 ({r.status_code}): {r.text[:150]}")
        token = open(os.path.expanduser("~/M82/.token")).read().strip() if os.path.exists(os.path.expanduser("~/M82/.token")) else None
except Exception as e:
    print(f"❌ Error de red: {e}")
    token = open(os.path.expanduser("~/M82/.token")).read().strip() if os.path.exists(os.path.expanduser("~/M82/.token")) else None

if token:
    headers_api = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 2. Jalar Reuters Wire
    print("\n📰 [REUTERS WIRE] Jalando noticias sobre Venezuela / Energy / CPI...")
    news_url = "https://api.refinitiv.com/data/news/v1/stories/search"
    query_payload = {"query": "Venezuela OR ENERGY OR CPI", "sort": "date desc", "count": 10}
    
    try:
        resp_news = requests.post(news_url, headers=headers_api, json=query_payload, timeout=10)
        if resp_news.status_code == 200:
            stories = resp_news.json().get("stories", [])
            print(f"✅ Recibidas {len(stories)} historias desde Refinitiv.")
            
            conn = sqlite3.connect(DB_PATH, timeout=60.0)
            c = conn.cursor()
            c.execute("PRAGMA busy_timeout=60000;")
            
            count = 0
            for s in stories:
                hl = f"[REFINITIV LITE] {s.get('title', {}).get('text', '')}"
                try:
                    c.execute("INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status) VALUES ('LSEG_REST_LITE', ?, 'PENDING')", (hl,))
                    count += 1
                except Exception: pass
            conn.commit()
            conn.close()
            print(f"🟢 Inyectados {count} titulares en m82_database.db")
        else:
            print(f"⚠️ News Error ({resp_news.status_code}): {resp_news.text[:150]}")
    except Exception as ex:
        print(f"⚠️ Exception en News Pull: {ex}")

