#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")

def check_triggers():
    conn = sqlite3.connect(DB, timeout=60.0)
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    # 1. Obtener último precio de Brent en m82_iran_crisis
    c.execute("SELECT brent, wti FROM m82_iran_crisis ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    if row:
        brent, wti = row
        print(f"📊 [M82_WIRE TRIGGER CHECK] Brent actual: {brent} | WTI: {wti}")
        
        # Evaluar ruptura de rangos ($105.00 / $108.00)
        if brent >= 108.00:
            c.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
                VALUES ('TRIGGER_OIL_BREAKOUT', ?, 'PENDING', ?)
            """, (f"ALERT BRENT BREAKOUT > 108.00 ({brent}): Supply disruption risks mounting on Hormuz standoff", now))
            print("🚀 TRIGGER ACTIVADO: Brent > $108.00")
            
        elif brent <= 105.00:
            c.execute("""
                INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
                VALUES ('TRIGGER_OIL_BREAKOUT', ?, 'PENDING', ?)
            """, (f"ALERT BRENT BREAKDOWN < 105.00 ({brent}): Market pricing in Hormuz reopening progress", now))
            print("📉 TRIGGER ACTIVADO: Brent < $105.00")

    # 2. Buscar si hay noticias clave de mediadores en m82_multi_stream
    c.execute("""
        SELECT headline FROM m82_multi_stream 
        WHERE (headline LIKE '%definitive views%' OR headline LIKE '%mediators%') 
        AND status = 'PENDING'
    """)
    headlines = c.fetchall()
    for h in headlines:
        print(f"🔔 TRIGGER NOTICIA DIPLOMÁTICA: {h[0][:80]}...")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    check_triggers()
