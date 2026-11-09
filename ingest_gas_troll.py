#!/usr/bin/env python3
import sqlite3, os, datetime
DB = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
c = conn.cursor()
now = datetime.datetime.now().isoformat()

c.executescript("""
CREATE TABLE IF NOT EXISTS m82_multi_stream (id INTEGER PRIMARY KEY AUTOINCREMENT, daemon_source TEXT, headline TEXT, status TEXT, timestamp TEXT);
CREATE TABLE IF NOT EXISTS m82_gas_outages (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, facility TEXT, scope_prev TEXT, scope_new TEXT, start TEXT, end TEXT, comment TEXT, impact_ttf TEXT);
CREATE TABLE IF NOT EXISTS m82_calendario_macro (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, evento TEXT, pais TEXT, impacto TEXT, estado TEXT, brent_ref REAL);
""")

# Ingest
facility = "Troll"
prev = "-10.0 mcm"
new = "-20.0 mcm"
start = "2026-09-29T06:00:00+0200"
end = "2026-09-30T06:00:00+0200"
comment = "Uncertain capacity"

signals = [
    f"NORWAY GAS GASSCO 28/09/2026: Troll outage revised -20.0 mcm vs -10.0 mcm prev - START {start} END {end} - Comment: {comment}",
    f"GAS TACTICAL: Troll capacity cut doubled +10 mcm/d incremental - ~3.65 bcm annualized risk if extended - TTF front month bullish bias - Brent 107.2 spread support",
    f"VE vs NORWAY: Sargent 170k bpd 0.16% global vs Troll 20 mcm/d 0.6% EU gas - Troll moves market more than VE pilot"
]

for h in signals:
    c.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES (?,?,?,?)",
              ("NORWAY_GAS_DESK", h, "PENDING", now))

c.execute("INSERT INTO m82_gas_outages VALUES (NULL,?,?,?,?,?,?,?,?)",
          (now, facility, prev, new, start, end, comment,
           "Bullish TTF: +10 mcm cut = 100 GWh/d - EU storage 92% but Troll is 20% Norway - uncertain capacity = extension risk - Brent 107.2 correlation gas-to-oil switching"))

c.execute("INSERT INTO m82_calendario_macro VALUES (NULL,?,?,?,?,?,?)",
          (f"{start} to {end}", f"Gassco Troll outage {new} vs {prev}",
           "NO", "MEDIO-ALTO",
           f"Revised from -10 to -20 mcm/d, 24h outage, comment uncertain - if extends past 30/09, TTF +1.5-2 EUR/MWh - watch Kollsnes",
           107.2))

conn.commit()
print(f"✅ Troll outage {prev} -> {new} ingested")

for row in c.execute("SELECT id, daemon_source, substr(headline,1,90), status FROM m82_multi_stream WHERE daemon_source='NORWAY_GAS_DESK' ORDER BY id DESC LIMIT 3"):
    print(row)

conn.close()
