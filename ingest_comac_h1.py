#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()
now = datetime.datetime.now().isoformat()

comac_headlines = [
    "COMAC H1 2026: Brent $75 Jan -> Peak $115-120 por Hormuz standoff - Squeeze freight + insurance + rerouting",
    "COMAC LOGISTICS: Vessel movements -96% + Golfo prod -6.7mbpd explican squeeze $13.18 Dubai sobre Brent base",
    "COMAC PASS-THROUGH: Petrol +19.9% / Diesel +29.4% / LPG +22.9% - Arbitraje JP8 +$70 capturado por refino US (Valero/Citgo)",
    "COMAC-VE BACKFILL: US busca barriles no-Golfo urgentes - OFAC 48D/49B valida piloto Sargent 170k bpd como señal politica",
    "COMAC AUDIT LOSS: Brent $106.77 + squeeze $13.18 = Fisico VE $119.95 - Perdida audit $159.95/bbl vs -$40 WTI 2020"
]

for h in comac_headlines:
    c.execute("""
        INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES ('COMAC_H1_2026', ?, 'PENDING', ?)
    """, (h, now))

conn.commit()
conn.close()
print("✅ Ingesta COMAC H1 2026 completada exitosamente en m82_database.db")
