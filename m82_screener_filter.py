#!/usr/bin/env python3
import datetime
from m82_db import execute_query

def enforce_macro_growth_filter(real_yield_val=3.0):
    now_iso = datetime.datetime.now().isoformat()
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🚨 REVISANDO REGIMEN MACRO (Real Yield = {real_yield_val}%)")
    
    if real_yield_val >= 3.0:
        print("❌ CRITERIO ACTIVO: Bloqueo de compras en Tech/Growth con P/E > 20x.")
        print("✅ ASIGNACIÓN ACEPTADA: Cash/T-Bills (4.8%), Energía Físicamente Respaldada (XLE, CVX, Brent).")
        
        headline = f"{now_iso} | M82 FILTER ACTIVATED: Growth > 20x auto-discarded due to Real Yield >= 3.0%. Target shifted to Physical Energy & Cash."
        query = "INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES ('M82_MACRO_FILTER', ?, 'PROCESSED', ?)"
        try:
            execute_query(query, (headline, now_iso))
            print("✅ Estado de filtro registrado en m82_multi_stream.")
        except Exception as e:
            print(f"⚠️ Error escribiendo registro: {e}")

if __name__ == "__main__":
    enforce_macro_growth_filter(3.0)
