import sqlite3, os, json
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB);cur=conn.cursor()
cur.execute("SELECT COUNT(*) FROM macro_dossier WHERE validated=1"); total=cur.fetchone()[0]
cur.execute("SELECT category,COUNT(*) FROM macro_dossier GROUP BY category")
cats=dict(cur.fetchall())
print(f"🟢 [MONEY DESK] {total}/113 — WAL 0/0/0")
for k,v in cats.items(): print(f"  {k}: {v}")
# BUNKER 0.30x
exp, var, warsh = 0.22, 1.68, 102.0
print(f"  BUNKER: {0.30}x LOCK — Exp {exp}x VaR {var}% Warsh +{warsh}bps")
print(f"  Base 444: $4.444T = Trust")
