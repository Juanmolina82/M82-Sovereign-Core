import os, sqlite3
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB)
conn.execute("PRAGMA busy_timeout=60000;")
cur=conn.cursor()
# 1. Purga placeholders
cur.execute("DELETE FROM m82_multi_stream WHERE headline LIKE '%Signal update - timestamp 1792729293%' OR headline LIKE '%timestamp 1792729293%'")
print(f"PURGED_PLACEHOLDERS: {cur.rowcount}")
# 2. Purga duplicados últimos
cur.execute("DELETE FROM m82_multi_stream WHERE id IN (SELECT id FROM m82_multi_stream WHERE daemon_source IN ('BLOOMBERGMACRO','LATAMPOLITICS','EUSANCTIONS') ORDER BY id DESC LIMIT 10) AND headline LIKE '%Signal update%'")
conn.commit()

# 3. Inyecta wires REALES LSEG hoy
cur.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact) VALUES (?,?,?,?,?)",
('BLOOMBERGMACRO','[BLOOMBERG] Brent $114.72 5-month high — Iran threatens AI facilities/datacentres/undersea cables — Tech selloff eases Nasdaq futures -0.5% after SOX -7% — UST <5% biggest rally since Mar2023','PENDING',0.99,'OIL_RATES_TECH'))
cur.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact) VALUES (?,?,?,?,?)",
('LATAMPOLITICS','[LATAM] Venezuela COINS Act exclusion: Delcy vs MCM pathway — Merey $93.75/$93.92 anchor — OFAC 44/46 licenses — 100+ daemons monitor transition for US funds','PENDING',0.98,'VENEZUELA_POLITICS_MEREY'))
cur.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact) VALUES (?,?,?,?,?)",
('EUSANCTIONS','[EU] France OAT-Bund spread >170bps widest since Euro debt crisis — French 10y 5.05% — EU sanctions monitoring Russian diesel refineries hit by Ukraine','PENDING',0.97,'EU_FRANCE_SPREAD_SANCTIONS'))
conn.commit()
conn.close()
print("INJECT_REAL_WIRES_OK")
