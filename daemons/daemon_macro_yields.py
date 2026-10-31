#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    # Ingesta en cola de eventos
    macro_headlines = [
        ("MACRO_OIL", "Middle East Oil Exports Rebound as Hormuz Stranglehold Eases"),
        ("MACRO_BONDS", "Sovereign Debt Auctions: US Treasuries, Mexico CETES & Brazil NTN-B Yields Adjust"),
        ("MACRO_INFLATION", "Global CPI & Economic Calendar: Eurozone Inflation Set to Rise, ECB Reports")
    ]
    
    count = 0
    for src, head in macro_headlines:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (src, head, now))
        if c.rowcount > 0: count += 1

    # Actualización de Métricas de Checklist de Petróleo
    c.execute("""
        INSERT INTO m82_mcn_checklist (timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield)
        VALUES (?, 107.2, 13.14, 1, 1, 1, 3.30)
    """, (now,))
    
    conn.commit()
    conn.close()
    print(f"📊 [DAEMON MACRO]: Inyectadas {count} señales macro y checklist de petróleo actualizado.")

if __name__ == "__main__":
    run()
