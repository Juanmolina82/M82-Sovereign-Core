#!/data/data/com.termux/files/usr/bin/bash
DB=~/M82/m82_database.db
NTFY=~/M82/scripts/ntfy.sh
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOCAL=$(date +"%H:%M %Z")

sqlite3 $DB <<SQL
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;
INSERT INTO m82_refinitiv_sentiment (timestamp, entity, sentiment_score, confidence, status, source) VALUES
('$TS','LSEG_MSFT_LUMEN_11B_DATACENTER_FIBER',0.92,0.95,'INGESTED_M&A_AI_INFRA','WORKSPACE_IMG1'),
('$TS','LSEG_INTEL_7.6B_CHIPS_RESHORING',0.88,0.91,'INGESTED_CHIPS_POLICY','WORKSPACE_IMG1'),
('$TS','LSEG_GM_-9PCT_PROFIT_CUT_COSTS',0.25,0.89,'INGESTED_AUTO_BEARISH','WORKSPACE_IMG1'),
('$TS','LSEG_TOYOTA_1.6B_SUPPLY_ENERGY_BOTTLENECK',0.30,0.87,'INGESTED_AUTO_BEARISH','WORKSPACE_IMG1'),
('$TS','LSEG_BRENT_IRAN_PEACE_TALKS_-4.5PCT',0.35,0.94,'INGESTED_COMMODITIES_BEARISH','WORKSPACE_IMG2'),
('$TS','LSEG_US_RUSSIA_GAS_SALES_EUROPE_VIA_UKRAINE',0.78,0.86,'INGESTED_ENERGY_GEOPOL','WORKSPACE_IMG2'),
('$TS','LSEG_MARVELL_SANMINA_10B_ACQUISITION',0.85,0.89,'INGESTED_SEMIS_M&A','WORKSPACE_IMG2'),
('$TS','LSEG_FORM_FACTOR_2B_ADV_PACKAGING',0.84,0.88,'INGESTED_SEMIS_AI','WORKSPACE_IMG2'),
('$TS','LSEG_MICHIGAN_SENATE_BALANCE_MIDTERMS',0.60,0.85,'INGESTED_ELECTIONS','WORKSPACE_IMG1'),
('$TS','LSEG_AI_CAPEX_800B_1.2T_ROI_QUESTIONED',0.40,0.90,'INGESTED_AI_ECONOMICS','WORKSPACE_IMG4');
PRAGMA wal_checkpoint(TRUNCATE);
SQL

$NTFY "M82 LSEG [M&A AI INFRA] MSFT/Lumen \$11B fiber datacenter + Marvell/Sanmina \$10B + Form Factor \$2B adv pkg + Intel \$7.6B chips | $LOCAL | BULLISH AI INFRA | Exp:0.22x"
sleep 1
$NTFY "M82 LSEG [COMMODITIES / ENERGY] BRENT -4.5% Iran peace + US pushes Russia gas via Ukraine to Europe | $LOCAL | BEARISH CRUDE SHORT-TERM | Exp:0.22x VaR:1.68%"
sleep 1
$NTFY "M82 LSEG [AUTO BEARISH] GM -9% profit cut + Toyota \$1.6B bottleneck + EV challenges | $LOCAL | BEARISH AUTO | Exp:0.22x"
sleep 1
$NTFY "M82 LSEG [ELECTIONS/MACRO] Michigan Senate balance + Kashkari recession + Midterms spend control + Fed Winter plan | $LOCAL | VOLATILITY | Exp:0.22x"

echo "$TS Workspace 4 images ingested OK" >> ~/M82/logs/lseg_daemon.log
