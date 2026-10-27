#!/usr/bin/env python3
import os, sqlite3, hashlib

DB = os.path.expanduser("~/M82/m82_database.db")
GRID = [
 ("VE_BANKING","D-01 :: SUDEBAN Daily GLFILE Realtime Scraper","SUDEBAN_CORE",0.98),
 ("VE_BANKING","D-02 :: Banesco Liquidity & Payments Clearing L5","BANESCO_L5",0.97),
 ("VE_BANKING","D-03 :: BNC FX Custody & Mesa Monitor","BNC_L5",0.96),
 ("VE_BANKING","D-04 :: BCV Official Rate & Reserves Telemetry","BCV_FX",0.99),
 ("VE_BANKING","D-05 :: Interbank Overnight & Encaje Legal Guard","LIQUIDITY_VE",0.95),
 ("VE_BANKING","D-06 :: Banco Venezuela Balance & Sovereign Flow","BDV_CORE",0.91),
 ("VE_BANKING","D-07 :: BBVA Provincial Intermediation Tracker","PROVINCIAL_L5",0.90),
 ("VE_BANKING","D-08 :: M2 Money Supply vs USD Velocity","MACRO_M2",0.94),
 ("VE_BANKING","D-09 :: Merchant POS Settlement Pipeline","POS_CLEARING",0.92),
 ("VE_BANKING","D-10 :: VE Banking Health Score Consolidated","HEALTH_INDEX",0.97),
 ("ENERGY","D-11 :: Orinoco Heavy Crude Tanker Departure Scraper","FAJA_CRUDE",0.96),
 ("ENERGY","D-12 :: Merey 16 vs WTI Differential Arb Calculator","CRUDE_SPREAD",0.98),
 ("ENERGY","D-13 :: Tuy III Pumping Station Electrical Monitor","TUY_III_POWER",0.94),
 ("ENERGY","D-14 :: Upgrader Diluent Supply & Import Logistics","DILUENT_FLOW",0.93),
 ("ENERGY","D-15 :: Refinitiv Commodities Realtime Stream","REFINITIV_COMM",0.97),
 ("ENERGY","D-16 :: BP Net Debt $13.5B Tracker & Refining Margins","BP_DEBT",0.96),
 ("ENERGY","D-17 :: PDVSA Joint Venture Cash Call Monitor","PDVSA_JV",0.90),
 ("ENERGY","D-18 :: Jose Terminal Storage & Export Scheduler","JOSE_TERM",0.92),
 ("ENERGY","D-19 :: Global Refinery Utilization vs Crack Spread","CRACK_SPREAD",0.95),
 ("ENERGY","D-20 :: Faja Power Demand vs AI Grid Correlation","FAJA_POWER_AI",0.96),
 ("TECH_AI","D-21 :: Big Tech Cloud Capex Monitor AWS/Azure/GCP","CAPEX_TRACKER",0.99),
 ("TECH_AI","D-22 :: Anthropic Run-Rate $16.8B Q3 -> $100B Predictor","ANTHROPIC_100B",0.98),
 ("TECH_AI","D-23 :: Jetson/Orin Edge VLA Hardware Router","VLA_JETSON",0.95),
 ("TECH_AI","D-24 :: Oasis 3D Physical World Telemetry Synth","OASIS_3D",0.96),
 ("TECH_AI","D-25 :: AI Data Center Power Demand vs Grid Capacity","POWER_BOTTLENECK",0.97),
 ("TECH_AI","D-26 :: ASML/NVDA Chip Supply & HBM Allocation","CHIP_SUPPLY",0.96),
 ("TECH_AI","D-27 :: Hitachi Grid Infra & Michigan Energy Deal","HITACHI_GRID",0.94),
 ("TECH_AI","D-28 :: Walmart AdTech Stack vs Target Margin Model","WMT_ADTECH",0.88),
 ("TECH_AI","D-29 :: Anthropic Profit $3B Q3 Inflection Detector","ANTHROPIC_PROFIT",0.98),
 ("TECH_AI","D-30 :: L5 Edge Node Uptime & Thermal Guard","L5_EDGE",0.97),
 ("TREASURY","D-31 :: US Treasury 2Y/10Y Curve Inversion/Steepening","UST_CURVE",0.99),
 ("TREASURY","D-32 :: SOFR & Fed Funds Expectations Parser","FED_WATCH",0.98),
 ("TREASURY","D-33 :: LPL Institutional Portfolio Risk Compliance","LPL_COMPLIANCE",0.97),
 ("TREASURY","D-34 :: Zero-PII Cross-Border Settlement Firewall","ZERO_PII",0.99),
 ("TREASURY","D-35 :: BAC $1.2B AML Penalty Compliance Validator","BAC_AML",0.96),
 ("TREASURY","D-36 :: JPM/WFC Wealth Management Fee Growth Tracker","JPM_WFC_FEES",0.94),
 ("TREASURY","D-37 :: MS/GS IB Advisory & Equity Underwriting Monitor","MS_GS_IB",0.93),
 ("TREASURY","D-38 :: Repo Market Liquidity & Collateral Squeeze","REPO_LIQ",0.92),
 ("TREASURY","D-39 :: UST Auction Bid-to-Cover Sentiment","UST_AUCTION",0.91),
 ("TREASURY","D-40 :: Sovereign/Corporate Bond Spread Tracker","BOND_SPREAD",0.90),
 ("FX_DESK","D-41 :: BCV vs Parallel vs Zelle Spread Arb Engine","FX_SPREAD_VE",0.98),
 ("FX_DESK","D-42 :: Corp Intl JMM C.A. Local Treasury Clearing","JMM_TREASURY",0.97),
 ("FX_DESK","D-43 :: Molina Holdings LLC US Dollar Collateral Guard","MOLINA_COLL",0.99),
 ("FX_DESK","D-44 :: USDT TRON vs Binance P2P Depth Monitor","USDT_DEPTH",0.96),
 ("FX_DESK","D-45 :: Miami/Caracas Collateral Bridge Reconciler","MIA_CCS_BRIDGE",0.95),
 ("FX_DESK","D-46 :: Zelle Daily Limit & Velocity Guard","ZELLE_GUARD",0.94),
 ("FX_DESK","D-47 :: Gold Pawn Shop vs USD Cash Rate Tracker","GOLD_USD",0.90),
 ("FX_DESK","D-48 :: FX Volatility Breakout Predictor","FX_VOL",0.93),
 ("FX_DESK","D-49 :: Non-PII Invoice Matching Engine","INVOICE_MATCH",0.98),
 ("FX_DESK","D-50 :: BCV Intervention Day Predictor","BCV_INTERV",0.96),
 ("EQUITIES","D-51 :: Citigroup P/B 0.61x Re-Rating Model","CITI_RERATE",0.97),
 ("EQUITIES","D-52 :: Wall St Peers MS/GS/BLK/SCHW Benchmark","PEERS_BENCH",0.96),
 ("EQUITIES","D-53 :: Refinitiv ESG Controversies Score Adjuster","ESG_CONTROV",0.94),
 ("EQUITIES","D-54 :: BAC AML 1.2B vs P/B Discount Model","BAC_DISC",0.92),
 ("EQUITIES","D-55 :: WMT vs TGT Ad Income & Comp Sales Model","WMT_TGT",0.88),
 ("EQUITIES","D-56 :: MS/GS Trading Revenue Momentum Tracker","MS_GS_TRADE",0.93),
 ("EQUITIES","D-57 :: BLK AUM Flow vs SCHW Cash Sorting Monitor","BLK_SCHW",0.91),
 ("EQUITIES","D-58 :: Buyback & Dividend Capital Return Optimizer","BUYBACK_OPT",0.90),
 ("EQUITIES","D-59 :: Combined Alpha 71 Model Signal Validator","ALPHA_71",0.95),
 ("EQUITIES","D-60 :: M82 Citadel Master Orchestrator Daemon","M82_MASTER",0.99)
]

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("PRAGMA journal_mode=WAL;")
c.execute("PRAGMA busy_timeout=60000;")
c.execute("""CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    daemon_source TEXT, headline TEXT, headline_hash TEXT UNIQUE, 
    desk TEXT, status TEXT, alpha_score REAL, asset_impact TEXT, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")

ins = 0
for desk, hl, tag, alpha in GRID:
    hf = f"[{desk}] {hl}"[:120]
    hh = hashlib.sha256(hf.encode()).hexdigest()[:16]
    try:
        c.execute("""INSERT INTO m82_multi_stream 
            (daemon_source, headline, headline_hash, desk, status, alpha_score, asset_impact, created_at) 
            VALUES (?,?,?,?,?,?,?,CURRENT_TIMESTAMP)""", 
            (desk, hf, hh, tag, "VERIFIED", alpha, "MACRO200_GRID_60"))
        ins += 1
    except: pass

conn.commit()
c.execute("SELECT COUNT(*) FROM m82_multi_stream WHERE asset_impact='MACRO200_GRID_60'")
cnt = c.fetchone()[0]
conn.close()
print(f"✅ MACRO 200 Grid: {ins} nuevos inyectados | Total MACRO200 en DB: {cnt}/60")
