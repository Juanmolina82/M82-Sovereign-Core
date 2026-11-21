import sqlite3, os
DB=os.path.expanduser("~/M82/m82_database.db")
con=sqlite3.connect(DB,timeout=60); cur=con.cursor()
cur.execute("PRAGMA busy_timeout=60000;"); cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("""INSERT OR IGNORE INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment)
VALUES('REUTERS_WRAPUP8_20261106','GLOBAL_MARKETS_STABILISATION',
'Reuters Wrapup8: Nasdaq Fut +1.5% bounce after -5.5% -$2.5T — Nikkei -6% KOSPI -6% Taiwan -4.5% close (-12.2% wk) Europe -1.5% — US10Y 4.86% — NVDA +4.5% premarket — SoftBank -11% CDS 4y high — Oil to $100 worst wk since 2020',
1.85,'M82_WRAPUP8_BOUNCE',0.10)""")
vals=[
 ('US_NQ_FUT','Nasdaq Futures Bounce','FUTURES',1.5,1.5,0,0,0.90),
 ('JP_NIKKEI','Nikkei 225','INDEX',0,0,-6.0,0,0.98),
 ('KR_KOSPI','KOSPI','INDEX',0,0,-6.0,0,0.98),
 ('TW_TWII','Taiwan TWII Close','INDEX',0,0,-4.5,0,0.98),
 ('TW_TWII_WK','Taiwan TWII Weekly','INDEX',0,0,-12.2,0,0.98),
 ('EU_STOXX','Europe Main','INDEX',0,0,-1.5,0,0.95),
 ('US10Y','US 10Y Yield','BOND',4.86,0,0,0,0.98),
 ('NVDA_PREMKT','Nvidia Premarket','EQUITY',0,0,4.5,0,0.90),
 ('SOFTBANK_JP','SoftBank','EQUITY',0,0,-11.0,0,0.98),
]
for v in vals:
    cur.execute("INSERT OR REPLACE INTO m82_global_derivatives VALUES(?,?,?,?,?,?,?,?)",(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7]))
con.commit(); print(cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone())
print("[M82 WRAPUP8 OK] ✅ Bounce +1.5% vs Crash -5.5% sellado. BUNKER MANTENIDO")
con.close()
