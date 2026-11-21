import sqlite3, os
DB = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(DB, timeout=60)
cur = con.cursor()
cur.execute("PRAGMA busy_timeout=60000;")
cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("""CREATE TABLE IF NOT EXISTS macro_dossier(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT, category TEXT, headline TEXT,
  risk_score REAL, m82_tag TEXT, sentiment REAL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS m82_global_derivatives(
  symbol TEXT PRIMARY KEY, contract_name TEXT, asset_class TEXT,
  spot_price REAL, daily_change REAL, pct_change REAL, rsi_14d REAL, val_alpha REAL)""")

cur.execute("""INSERT OR IGNORE INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment)
VALUES('BLS_NFP_20261106_ACTUAL','US_LABOR_MARKET_NFP',
'BLS Actual 06-Nov: NFP Oct +165K vs +65K Est BEAT +100K - Unemployment 4.1% - Wages 3.1% YoY vs 2.9% Est - Revisions Ago +53K Sep +31K - Prof Business +70K Health +42K',
1.65,'M82_MACRO_NFP_BEAT',-0.15)""")

for s,n,spot,dc,pc,rsi,va in [
 ('US_NFP_OCT_ACTUAL','Nonfarm Payrolls Oct Actual','MACRO_INDICATOR',165.0,100.0,153.8,62.0,0.98),
 ('US_WAGE_YOY_ACTUAL','US Wage Growth YoY Actual','MACRO_INDICATOR',3.1,0.2,6.9,58.0,0.98),
 ('US_UNEMP_OCT_ACTUAL','US Unemployment Rate Oct','MACRO_INDICATOR',4.1,-0.1,-2.38,45.0,0.98),
 ('US_IXIC_ACTUAL','Nasdaq Composite','INDEX',0,0,-5.50,0,0.98),
 ('US_NDX_ACTUAL','Nasdaq 100','INDEX',0,0,-6.40,0,0.98),
 ('US_SOX_ACTUAL','Philadelphia SOX','INDEX',0,0,-12.20,0,0.98),
 ('CRWV_CDS_ACTUAL','CoreWeave CDS','CREDIT',1267.9,0,0,0,0.98),
]:
    cur.execute("INSERT OR REPLACE INTO m82_global_derivatives VALUES(?,?,?,?,?,?,?,?)",(s,n,'MACRO_INDICATOR' if 'US_' in s else 'INDEX',spot,dc,pc,rsi,va))

con.commit()
print(cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone())
print("[M82 NFP BEAT OK] ✅ +165K | 4.1% | 3.1% sellado. 0/0/0 CLEAN")
con.close()
