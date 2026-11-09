#!/usr/bin/env python3
import sqlite3, os, datetime

DB = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()
now = datetime.datetime.now().isoformat()

analysis_headlines = [
    "ASIMETRIA VE 2026: OFAC 48D/49B + EO14373 le da aire a Delcy (servicios/luz) sin dar elecciones pre-midterms",
    "PERDIDA AUDIT VE $159.95/bbl: Fisico $119.95 vs -$40 WTI 2020 - Arbitraje JP8 +$70 capturado por refino US, no por PDVSA",
    "RESERVAS VE M82_MACRO REAL 5-8%: Faja sin SAGD ni Capex $50B de Majors es fake - 300MMbbl irreales sin Estado de Derecho",
    "VENTANA MCM SEP-OCT: Presion movilizacion 24 Julio es ahora - Post-midterms US pierde interes y Delcy congela cronograma"
]

for h in analysis_headlines:
    c.execute("""
        INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
        VALUES ('STRATEGIC_ANALYSIS_VE', ?, 'PENDING', ?)
    """, (h, now))

conn.commit()
conn.close()
print("✅ Tesis estratégica y auditoría de asimetría inyectadas en m82_database.db")
