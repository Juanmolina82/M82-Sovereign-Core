import sqlite3, os
DB=os.path.expanduser("~/M82/m82_database.db")
con=sqlite3.connect(DB,timeout=60); cur=con.cursor()
cur.execute("PRAGMA busy_timeout=60000;"); cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("""INSERT OR IGNORE INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment)
VALUES('EIA_NATGAS_WEEKLY_20261105','ENERGY_NATGAS_US',
'EIA Weekly Natgas: +77 BCF vs +81 BCF exp — Total 3,801 BCF — -2.8% YoY vs 3,910 — +1.4% vs 5yr avg 3,747 — South Central +40 BCF — Salt -12.9% YoY',
1.30,'M82_EIA_NATGAS_77BCF',-0.10)""")
vals=[
 ('US_NATGAS_STOCKS','US Natgas Stocks BCF','ENERGY',3801,0,-2.8,0,0.98),
 ('US_NATGAS_INJ','US Natgas Weekly Injection BCF','ENERGY',77,0,0,0,0.98),
 ('US_NATGAS_SALT','South Central Salt Stocks BCF','ENERGY',296,0,-12.9,0,0.95),
 ('US_NATGAS_5YR','US Natgas vs 5yr Avg %','ENERGY',1.4,0,0,0,0.95),
]
for v in vals:
    cur.execute("INSERT OR REPLACE INTO m82_global_derivatives VALUES(?,?,?,?,?,?,?,?)",(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7]))
con.commit(); print(cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone())
print("[M82 NATGAS OK] ✅ +77 BCF vs +81 exp sellado. Stocks -2.8% YoY.")
con.close()
