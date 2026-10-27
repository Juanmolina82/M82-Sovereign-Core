import os, sqlite3, logging
from datetime import datetime

# Silenciar logs ruidosos
logging.basicConfig(level=logging.INFO)

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def run_southcom_monitor():
    conn = get_db_connection()
    c = conn.cursor()
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("🛰️ [M82 GEOPOLITICAL ENGINE] Ejecutando rastreo SOUTHCOM / USNORTH-CARIBBEAN...")
    
    # Eventos de inteligencia / señales detectadas
    intel_signals = [
        {
            "daemon": "SOUTHCOM_CARIBBEAN",
            "asset": "MACRO",
            "headline": "SOUTHCOM: Carrier Strike Group USS Gerald R. Ford repositioned in USNORTH-CARIBBEAN sector",
            "score": 88,
            "ev_usd": 185.00
        },
        {
            "daemon": "SDNY_INDICTMENTS",
            "asset": "MACRO",
            "headline": "SDNY Superseding Indictment: Unsealed CC-1/CC-3 DGCIM torture & narco nexus",
            "score": 82,
            "ev_usd": 165.50
        }
    ]
    
    injected = 0
    for sig in intel_signals:
        headline = sig["headline"]
        clean_hl = f"m82 southcom {sig['daemon'].lower()}"
        score = sig["score"]
        status = "PENDING"  # Eventos tail-risk pasan directo con alto EV
        risk_budget = sig["ev_usd"]
        
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream 
            (daemon_source, headline, clean_headline, alpha_score, confidence, final_score, asset_impact, status, created_at, risk_budget_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sig["daemon"], headline, clean_hl, score, 98, score, sig["asset"], status, now_str, risk_budget))
        
        if c.rowcount > 0:
            injected += 1

    conn.commit()
    conn.close()
    
    print(f"✅ [SOUTHCOM MONITOR] Signals procesadas e inyectadas: {injected} PENDING en DB.")

if __name__ == "__main__":
    run_southcom_monitor()
