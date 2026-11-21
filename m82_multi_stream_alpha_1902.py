#!/usr/bin/env python3
# ==============================================================================
# M82 MULTI STREAM --ALPHA ENGINE (AUTOMATIZADO) - 5-STREAM MATRIX MCM EDITION
# Chairman Juan M. Molina — Charallave L4/L5 Edge Node
# ==============================================================================
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run_alpha_stream():
    db_target = DB_PATH if os.path.exists(DB_PATH) else os.path.expanduser("~/M82_Macro/m82_database.db")
    
    conn = sqlite3.connect(db_target)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=60000;")

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S VE")

    alpha_payloads = [
        ("LSEG_WIRE_ALPHA", f"[{timestamp_str}] #BOTTLENECK :: Sweeny Coker 26.2 UPSET - USGC heavy crude capacity constrained. No replacement.", "PENDING", 0.98, "CRUDE_USGC_REFINING"),
        ("RUBIO_STATE_ALPHA", f"[{timestamp_str}] #RUBIO_WIRE :: 60d Russia diesel extension proves market needs Venezuela stable source, not temporary waiver.", "PENDING", 0.97, "GLOBAL_MACRO_DIESEL"),
        ("GPRK_ALPHA", f"[{timestamp_str}] #GPRK_VECTOR :: Hwasong-20 + Abraham Accords 5y stress = Hormuz chokepoint premium permanent. Warsh +102bps.", "PENDING", 0.96, "TAIL_RISK_GEOPOLITICS"),
        ("MCM_GOVERNANCE_ALPHA", f"[{timestamp_str}] #MCM_CORRIDOR :: MCM legitimacy unlocks $200B CAPEX at 2h from Texas. Citi Escrow + Trump + PE Dry Powder $2.008T. Free elections = bankable 10y OFAC license.", "PENDING", 0.99, "LATAM_MACRO_PE"),
        ("OPEC_TELEMETRY_ALPHA", f"[{timestamp_str}] #OPEC_STAGNANT :: +6k b/d OPEC optical illusion. Zulia 400k b/d stranded = real swing capacity.", "PENDING", 0.91, "ENERGY_COMMODITIES")
    ]

    for source, headline, status, alpha, impact in alpha_payloads:
        try:
            c.execute("""
                INSERT OR REPLACE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
                VALUES (?, ?, ?, ?, ?)
            """, (source, headline, status, alpha, impact))
            print(f"[M82-ALPHA] Inyectado 5-Stream: {source} (Alpha: {alpha})")
        except Exception as e:
            print(f"[M82-ALPHA] Error BD: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(f"[M82-ALPHA] Disparo de matriz 5-Stream MCM Edition activado: {datetime.now().strftime('%H:%M:%S VE')}")
    run_alpha_stream()
