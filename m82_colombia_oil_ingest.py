import sqlite3, os
DB=os.path.expanduser("~/M82/m82_database.db")
con=sqlite3.connect(DB,timeout=60); cur=con.cursor()
cur.execute("PRAGMA busy_timeout=60000;"); cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("""INSERT OR IGNORE INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment)
VALUES('REUTERS_COLOMBIA_OIL_20261106','LATAM_ENERGY_COLOMBIA',
'Colombia ANH Sep: Oil 729,593 bopd -2.92% YoY — Gas 705 mpcd -13.39% YoY — Imports 40% gas — De La Espriella reactivates exploration — 19.9M ha reserved — New areas Q1 2027',
1.70,'M82_COLOMBIA_OIL',-0.30)""")
vals=[
 ('CO_OIL_SEP','Colombia Oil Production bopd','ENERGY',729593,0,-2.92,0,0.98),
 ('CO_GAS_SEP','Colombia Gas Production mpcd','ENERGY',705,0,-13.39,0,0.98),
 ('CO_GAS_IMPORT','Colombia Gas Import Share %','ENERGY',40.0,0,0,0,0.95),
 ('CO_EXPLORATION_HA','Colombia New Exploration Hectares','ENERGY',19900000,0,0,0,0.90),
]
for v in vals:
    cur.execute("INSERT OR REPLACE INTO m82_global_derivatives VALUES(?,?,?,?,?,?,?,?)",(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7]))
con.commit(); print(cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone())
print("[M82 COLOMBIA OK] ✅ Oil -2.92% Gas -13.39% sellado. Reactivación Q1 2027 en radar.")
con.close()
