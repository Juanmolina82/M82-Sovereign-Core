import sqlite3, os, json
from datetime import datetime, timezone
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur=conn.cursor()
headline="[M82 INTEL MX FLASH v61.0.37] Intel -20% Cash Burn Obscures Recovery Client Computing -9% Foundry Roadmap Crush FCF vs Guadalajara 1k Engineers Efficient Island 50% AI PCs 2027 80% 2028 Privacy Without Capex"
tag="v61.0.37-M82-INTEL-20-CASH-BURN-GUADALAJARA-1000-ENGINEERS"
meta={
 "source":"ContentEngine USA via LSEG Workspace 30-Oct-2026 id dXJuOm5ld3NtbDpuZXdzcm9vbS5yZWZpbml0aXYuY29tOjIwMjYxMDMwOm5OUkEyaXZxbG06MA==",
 "market":"Intel -20% Q3 2026 cash burn projections guidance down cyclical PC weakness + high foundry spend — Client Computing -9% — Multi-year foundry roadmap reduces free cash flow short term — Institutional investors adjust multiples — Operating cost high — Revenue divergence",
 "mexico_hedge":"Guadalajara Design Center efficient engineering engine ~1,000 specialists enterprise silicon testing — Isolated from high manufacturing costs — Focus cost-effective enterprise AI architectures + hardware validation — North American integration intact — Carlos Rebellon leader Intel MX: adopt AI PCs for privacy + data security without large capex — Enterprise AI-enabled PCs >50% shipments region 2027 80% 2028 — Budgets prioritize cyber defense + systems automation",
 "vs_reuters":"Reuters -30% $130B wiped biggest one-day loss record intraday 30-Oct weak PC bottlenecks memory shortage vs ContentEngine -20% corporate read — Both confirm debt-funded fab model broken FCF crush",
 "m82_thesis":"Guadalajara 1000 = Corniche powered land model — Efficient engineering near market vs Gigafab cash burn $51B/quarter GOOGL $97.5B META $25B MSFT — On-premise Edge AI privacy without capex = powered land Venezuela gas $0 flare $40M/day + Merey $88.80 crack $108/bbl + 50% AI PCs 2027 needs cheap backend — Quad-SPV Delaware 50/50 BUNKER 0.30x LOCK",
 "timestamp":datetime.now(timezone.utc).isoformat()
}
cur.execute("INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node) VALUES (?,?,?,?,?,?,?,?,?)",
("LSEG / ContentEngine Intel MX", "SEMI_SUPPLY_CHAIN_FOUNDRY_CASH_BURN_GUADALAJARA", headline, 0.95, tag, 0.88, json.dumps(meta), "v61.0.37", "NODO_CHARALLAVE_L4L5"))
conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
print(f"🔒 M82 v61.0.37 SEALED — TOTAL {cur.fetchone()[0]} — WAL 0/0/0")
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()
