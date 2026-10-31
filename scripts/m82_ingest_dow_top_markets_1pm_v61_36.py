import sqlite3, os, json
from datetime import datetime, timezone
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur=conn.cursor()
headline="[M82 DOW 1PM FLASH v61.0.36] Amazon Intel Fuel Tech Selloff Nasdaq -2% + $6.3B Crypto Hack BTC ETH -3% + Oil +2% Hormuz Tanker Attack Houthi Saudi + Eurozone Slows High Energy TTF €100 + France Contraction + UST Yields Fall"
tag="v61.0.36-M82-DOW-1PM-TOP-MARKETS-HORMUZ-OIL-CRYPTO-HACK"
meta={
 "source":"Dow Jones Top Markets Headlines 30-Oct-2026 13:00 ET via LSEG Workspace id dXJuOm5ld3NtbDpuZXdzd2lyZS5yZWZpbml0aXYuY29tOjIwMjYxMDMwOm5ESlIxOGxna0s6MQ==",
 "vectors":{
   "tech_selloff":"Nasdaq comp >2% slump Amazon Intel fuel AI trade worries — confirms v61.0.35 $2T wipeout -5.8% Oct = SpaceX value GOOGL -12.6% $500B META $97.5B INTC -30% $130B",
   "crypto":"$6.3B hack biggest crypto exchange breach BTC ETH -3% tumbling then paring losses — risk off",
   "oil":"Oil +2% Hormuz tanker attack + Houthi claims Saudi energy infra strike + Ukraine hits Russian refinery first in 2 weeks defying Trump — supply fears — WTI $102.80→$105 Merey $88.80→$91 — +$2B annual VZ flow",
   "eurozone":"Eurozone slows high energy prices France contracts debt worries political paralysis — validates TTF €100.37 11.8x divide HH $3 storage DE 61.5% EU 75%",
   "macro":"Canada GDP dipping after 2 flat months contraction Sept — BOJ declares inflation win rate hikes coming hold Friday expected — BOE prices +3.8% vs 3.7% Sept slowing wage growth — UST yields fall Eurozone mixed — flight to quality",
   "m82_thesis":"All 6 vectors converge to Quad-SPV Delaware 50/50 + Citi NY escrow + gas $0 feedstock flare $40M/day €14B/yr + Merey crack $108/bbl $40B/yr diesel + powered land multi-GW + BUNKER 0.30x LOCK vs debt bomb $97.5B $25B $51B/quarter"
 },
 "timestamp":datetime.now(timezone.utc).isoformat()
}
cur.execute("INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node) VALUES (?,?,?,?,?,?,?,?,?)",
("LSEG / Dow Jones 1PM Top Markets", "MULTI_VECTOR_HORMUZ_OIL_CRYPTO_TECH_SELLOFF", headline, 1.00, tag, 0.90, json.dumps(meta), "v61.0.36", "NODO_CHARALLAVE_L4L5"))
conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
print(f"🔒 M82 v61.0.36 SEALED — TOTAL {cur.fetchone()[0]} — WAL 0/0/0")
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()
