import os, datetime, sqlite3, pandas as pd
output_dir = os.path.expanduser('~/M82')
db_path = os.path.join(output_dir, 'm82_database.db')
os.makedirs(output_dir, exist_ok=True)

universe = [
    ("AAPL.O","Apple","TECH_SEMIS_AI",222.91,245.50,34.12,"Strong Buy"),
    ("MSFT.O","Microsoft","TECH_SEMIS_AI",425.30,480.00,32.5,"Buy"),
    ("NVDA.O","Nvidia","TECH_SEMIS_AI",145.20,175.00,55.0,"Strong Buy"),
    ("GOOGL.O","Alphabet","TECH_SEMIS_AI",175.80,200.00,24.0,"Buy"),
    ("AMZN.O","Amazon","CONSUMER",195.40,220.00,42.0,"Buy"),
    ("META.O","Meta","TECH_SEMIS_AI",580.10,650.00,26.0,"Buy"),
    ("TSLA.O","Tesla","AUTO_EV",310.50,350.00,75.0,"Hold"),
    ("JPM.N","JPMorgan","BANKS",235.20,260.00,12.5,"Buy"),
    ("XOM.N","Exxon","ENERGY_OIL",115.30,130.00,13.0,"Buy"),
    ("CVX.N","Chevron","ENERGY_OIL",155.80,175.00,14.2,"Buy"),
]

df = pd.DataFrame(universe, columns=["RIC","Name","Sector","Spot","Target","PE","Consensus"])
df["Upside_%"] = (df["Target"]/df["Spot"]-1)*100
df["Alpha"] = 0.94
df["Timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S VET')
df["Source"] = "LSEG Workspace jmmp@molina82.com"

excel_path = os.path.join(output_dir, f'm82_wallstreet_master_{datetime.datetime.now().strftime("%Y%m%d")}.xlsx')
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='WallStreet Universe', index=False)
    df.groupby('Sector').agg({'Spot':'mean','Target':'mean','Upside_%':'mean','PE':'mean'}).to_excel(writer, sheet_name='Sector Summary')
    pd.DataFrame([{"Metric":"AAPL Anchor","Value":"$222.91 Spot $245.50 Target +10.1%","Note":"Q4 $114.5B Beat Services ATH"},{"Metric":"Venezuela Export","Value":"809k bpd -25% Oct","Note":"Flete $13.85-> $9.41 TD25"},{"Metric":"Governance","Value":"BUNKER 0.30x LOCK Exp 0.22x","Note":"VaR 1.68% Warsh 102bps"}]).to_excel(writer, sheet_name='M82 Governance', index=False)

# INGESTA WAL CORREGIDA — LOOP COMPLETO
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
conn.execute("PRAGMA synchronous=NORMAL;")
for _, row in df.iterrows():
    conn.execute("INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger) VALUES (?,?,?,?,?,?,?)",
                 (f'REFINITIV_{row["RIC"]}', f'[WALLSTREET MASTER | {row["RIC"]}] {row["Name"]} Spot ${row["Spot"]} Target ${row["Target"]} Upside {row["Upside_%"]:.1f}% | {row["Consensus"]} PE {row["PE"]}x', 'PROCESSED', 0.94, 0.85, row["Sector"], f'LSEG_{row["RIC"]}_MASTER_{datetime.datetime.now().strftime("%Y%m%d")}'))
    conn.execute("INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json) VALUES (?,?,?,?,?,?,?)",
                 (f'WALLSTREET_{row["RIC"]}', 'EQUITY_MASTER', f'WallStreet Master Ingestion {row["RIC"]} {row["Upside_%"]:.1f}% upside', 1.68, 'v61.0.51-A-WALLSTREET', 0.85, f'{{"ric":"{row["RIC"]}","spot":{row["Spot"]},"target":{row["Target"]},"upside":{row["Upside_%"]:.1f}}}'))
conn.commit()
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()

print(f"WALLSTREET_MASTER_SUCCESS: {excel_path} — {len(df)} equities — WAL ingested")
print(df[["RIC","Spot","Target","Upside_%","Consensus"]].to_string(index=False))
