import sqlite3, os
DB=os.path.expanduser("~/M82/m82_database.db")
con=sqlite3.connect(DB,timeout=60); cur=con.cursor()
cur.execute("PRAGMA busy_timeout=60000;"); cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("""INSERT OR IGNORE INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment)
VALUES('REUTERS_EXTR_MA_20261106','M&A_NETWORKING_AI',
'Reuters Exclusive: Extreme Networks EXTR explores sale ~$3B mcap — Buyers FTNT CSCO NTAP — Rev +13% FY26 — Platform ONE AI >30% sub bookings — Follows HPE-Juniper $14B 2025',
1.40,'M82_MA_EXTR',0.35)""")
vals=[
 ('EXTR','Extreme Networks','EQUITY',3.0,0,13.0,0,0.85),
 ('FTNT_BID','Fortinet Potential Buyer','EQUITY',0,0,0,0,0.70),
 ('CSCO_BID','Cisco Potential Buyer','EQUITY',0,0,0,0,0.70),
 ('NTAP_BID','NetApp Potential Buyer','EQUITY',0,0,0,0,0.70),
]
for v in vals:
    cur.execute("INSERT OR REPLACE INTO m82_global_derivatives VALUES(?,?,?,?,?,?,?,?)",(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7]))
con.commit(); print(cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone())
print("[M82 EXTR OK] ✅ M&A Networking sellado. Consolidación AI en crash.")
con.close()
