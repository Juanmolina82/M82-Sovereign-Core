#!/usr/bin/env python3
import sqlite3, json, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def export_stack():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    # Precios
    c.execute("SELECT asset, last_price, updated_at FROM price_ticks ORDER BY updated_at DESC LIMIT 10")
    prices = [{"asset": r[0], "price": r[1], "ts": r[2]} for r in c.fetchall()]
    
    # Noticias Filtradas
    c.execute("SELECT daemon_source, headline, status FROM m82_multi_stream ORDER BY id DESC LIMIT 15")
    stream = [{"source": r[0], "headline": r[1], "status": r[2]} for r in c.fetchall()]
    
    conn.close()
    
    export_data = {
        "system": "M82 Sovereign Core / Charallave Edge",
        "governance": "BUNKER MODE 0.30x LOCK",
        "market_snapshot": prices,
        "multi_stream": stream
    }
    
    out_file = os.path.expanduser("~/M82/claude_m82_stack.json")
    with open(out_file, "w") as f:
        json.dump(export_data, f, indent=2)
        
    print(f"🟢 [EXPORT OK] Archivo generado en: {out_file}")

if __name__ == "__main__":
    export_stack()
