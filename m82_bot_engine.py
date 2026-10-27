#!/usr/bin/env python3
"""
M82 BOT ENGINE — AGI QUANTUM DISPATCHER
Sovereign Edge Execution Node L4/L5 — Molina Holdings LLC
Chairman: Juan M. Molina
"""

import os, sqlite3, time, json, math, logging
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

logging.basicConfig(
    filename=os.path.expanduser('~/M82/m82_bot.log'),
    level=logging.INFO,
    format='%(asctime)s [%(BOT)s] %(message)s'
)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def run_bot_loop():
    print("⚡ [M82 BOT] Iniciando servicio de escucha y despacho telemétrico...")
    last_processed_id = 0
    
    # Obtener el último ID registrado para no duplicar alertas históricas
    try:
        conn = get_db()
        cur = conn.cursor()
        res = cur.execute("SELECT MAX(id) FROM m82_multi_stream").fetchone()
        if res and res[0]:
            last_processed_id = res[0]
        conn.close()
    except Exception as e:
        print(f"Error al inicializar ID del Bot: {e}")

    while True:
        try:
            conn = get_db()
            cur = conn.cursor()
            rows = cur.execute("""
                SELECT id, daemon_source, headline, alpha_score, sentiment, asset_impact 
                FROM m82_multi_stream 
                WHERE id > ? 
                ORDER BY id ASC LIMIT 10
            """, (last_processed_id,)).fetchall()
            
            for r in rows:
                row_id = r['id']
                daemon = r['daemon_source'] or 'M82_DAEMON'
                headline = r['headline'] or 'Evento detectado'
                alpha = r['alpha_score'] or 0.85
                sentiment = r['sentiment'] or 0.50
                
                # Scoring Cuántico
                q_sig = round(alpha * 0.70 + sentiment * 0.30, 4)
                var_contrib = round((1.0 - alpha) * 1.68, 4)
                
                # Despachar únicamente si cumple el umbral cuantitativo o impacto
                if alpha >= 0.85 or "MEREY16" in headline or "WARSH" in headline:
                    alert_payload = {
                        "bot_status": "DISPATCHED",
                        "id": row_id,
                        "source": daemon,
                        "headline": headline,
                        "quant_signal": q_sig,
                        "alpha": alpha,
                        "var_contrib": f"{var_contrib}%",
                        "node": "SOVEREIGN EDGE L4/L5",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    print(f"\n📲 [BOT ALERT DISPATCH] -> {daemon}")
                    print(f"   Headline: {headline}")
                    print(f"   Quant Sig: {q_sig} | Alpha: {alpha} | VaR: {var_contrib}%")
                    logging.info(f"Alert Dispatched ID {row_id}: {daemon} - {q_sig}")
                
                last_processed_id = row_id
                
            conn.close()
        except Exception as e:
            print(f"Error en bucle del Bot: {e}")
            
        time.sleep(3)

if __name__ == '__main__':
    run_bot_loop()
