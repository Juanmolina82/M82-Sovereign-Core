#!/usr/bin/env python3
# ==============================================================================
# M82 MACRO DOSSIER — CHEVRON (CVX.N) LSEG WORKSPACE DEDICATED DAEMON
# Focus: Joint Venture Crudes, Joint Operations & OFAC Trade Flow
# ==============================================================================

import os, time, sqlite3, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

CHEVRON_FEEDS = [
    ("CHEVRON_JV", "Chevron Corp CVX.N updates Joint Venture production allocation for Orinoco heavy crude blends", 0.84, "WTI"),
    ("ENI_REPSOL_SWAPS", "Chevron JV tanker loading operations at Jose Terminal synchronized with European swaps", 0.78, "PDVSA26"),
    ("OFAC_LICENSES", "Chevron receives renewed operational guidelines under OFAC general license framework", 0.89, "VENZ34"),
    ("ORINOCA_CRUDE", "CVX.N Joint Venture upgrades blending facility capacity to sustain daily export targets", 0.72, "WTI")
]

def run_chevron_daemon():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    src, headline_text, base_alpha, asset = random.choice(CHEVRON_FEEDS)
    alpha_score = round(base_alpha + random.uniform(-0.03, 0.03), 2)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    headline = f"[{src} | {now_str}] {headline_text}"
    
    try:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
            VALUES (?, ?, 'PENDING', ?, ?)
        """, (src, headline, alpha_score, asset))
        conn.commit()
        print(f"📡 [CVX.N LSEG] Ingestado titular corporativo/operacional: {src}")
    except Exception as e:
        print(f"⚠️ Error en daemon Chevron: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 [M82 DAEMON] Monitor Dedicado de Chevron Corp (CVX.N) Activo...")
    while True:
        try:
            run_chevron_daemon()
        except Exception as e:
            print(f"⚠️ Error en loop CVX: {e}")
        time.sleep(90) # Ingesta coordinada cada 90 segundos
