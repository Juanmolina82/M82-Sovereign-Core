import sqlite3, os, json
from datetime import datetime, timezone
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
cur=conn.cursor()
headline="[M82 SPCX FLASH v61.0.43] SpaceX SPCX -5.3% $7.58 $136.31 73M Shares $10B Vol 1.1x Avg vs NDX -3.9% 28253 — MACD Bearish EMA 148.93-150.51 — Liabilities/EBITDA 12.1 vs Piotroski 5 — Tobin Q 12.6 Overvalued Bottom 3% — Starlink 9600 Sats 10.3M Subs 164 Countries xAI Acquired Early 2026 Largest Aerospace Defense"
tag="v61.0.43-M82-SPCX-53-TUMBLE-TECHNICAL-DEBT-BOMB"
meta={
 "source":"BuySellSignals via LSEG Workspace 30-Oct-2026 13:58 ET id dXJuOm5ld3NtbDpuZXdzcm9vbToyMDI2MTAzMDpuTlJBMml3d3I4OjE=",
 "price":"SPCX $136.31 -$7.58 -5.3% Fri 13:58 NY — NDX -1,148.8 pts -3.9% 28,253.69 relative -1.4% — Vol 73M shares $10B 1.1x avg 67.7M — Largest Aerospace defense NASDAQ by mcap",
 "past_week":"SPCX -0.6% avg vol 0.98x vs NDX +1.5% +430.7 pts relative -2.1% — Range low $143.88 Thu Oct29 high $148.59 Tue Oct27 — Downtrend",
 "technical":"Negative MACD 12-day EMA 148.93 - 26-day EMA 150.51 negative both falling bearish — Liabilities/EBITDA 12.1 > Piotroski 5 unfavourable — Tobin Q MCap/Total Assets 12.6 overvalued bottom 3% value",
 "activities":"Founded 2002 Elon Musk vertically integrated aerospace tech leader Falcon 9 Starship Starlink ~9,600 sats 10.3M subs 164 countries Mar31 2026 >80% global orbital mass >99% success — Early 2026 acquired xAI frontier AI large-scale compute — IPO largest debut — Convergence space transport global connectivity truth-seeking AI — Three transformative industries",
 "connect":"v61.0.38 SpaceX needs $130B T-Mobile $28B+$90B+$40B BNP $100B + v61.0.39 Anthropic largest customer SpaceX has lot compute + v61.0.41 Nasdaq -4% real $3T wipeout + v61.0.40 Oil +2% Hormuz + v61.0.42 ULCC $5B debt $817M deficit jet fuel — Validates debt bomb WACC 10.8-16% Warsh +102 bps Fed +50 bps CDS surge",
 "m82_thesis":"SPCX -5.3% $10B vol institutional distribution — Liabilities/EBITDA 12.1 Tobin Q 12.6 bottom 3% = Overlevered overvalued — Needs $320B total telco + compute + launch with balance already stretched — Quad-SPV Delaware $25B GE Vernova gas $0 flare $40M/day Merey $88.80->95 crack $108 $40B/yr powered land multi-GW BUNKER 0.30x LOCK healthy vs 12.1x — Real assets > promises",
 "timestamp":datetime.now(timezone.utc).isoformat()
}
cur.execute("INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version, ingestion_node) VALUES (?,?,?,?,?,?,?,?,?)",
("LSEG / BuySellSignals SPCX", "EQUITY_TECHNICAL_SPCX_DEBT_BOMB_OVERVALUED", headline, 0.99, tag, 0.93, json.dumps(meta), "v61.0.43", "NODO_CHARALLAVE_L4L5"))
conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
print(f"🔒 M82 v61.0.43 SEALED — TOTAL {cur.fetchone()[0]} — WAL 0/0/0")
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
conn.close()
