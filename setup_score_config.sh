#!/usr/bin/env bash
DB="$HOME/M82/m82_database.db"

sqlite3 "$DB" << 'SQL'
CREATE TABLE IF NOT EXISTS m82_score_config (
  source TEXT PRIMARY KEY,
  alpha_min INTEGER,
  alpha_max INTEGER,
  asset TEXT,
  action TEXT
);

DELETE FROM m82_score_config;

INSERT INTO m82_score_config VALUES 
('HOUTHI_SAUDI_MISSILE', 85, 100, 'BRENT', 'BUY_BREAKOUT'),
('CENOVUS_BP_DEAL', 70, 85, 'WTI', 'BUY_HEAVY_SPREAD'),
('FED_RATES_HAWK', 60, 80, 'US10Y', 'SELL_DURATION'),
('FED_RATES_DOVISH', -80, -60, 'XAUUSD', 'BUY_GOLD'),
('GLOBAL_BOND_YIELDS', 60, 70, 'XAUUSD', 'BUY_SAFE_HAVEN'),
('CITGO_OFAC_DESK', 75, 90, 'VENZ34', 'BUY_VENZ'),
('BRICS_GOLD_RESERVES', 50, 65, 'XAUUSD', 'HOLD_GOLD');

CREATE TABLE IF NOT EXISTS m82_multi_stream (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  daemon_source TEXT,
  headline TEXT,
  clean_headline TEXT UNIQUE,
  alpha_score INTEGER DEFAULT 0,
  confidence INTEGER DEFAULT 0,
  final_score INTEGER DEFAULT 0,
  asset_impact TEXT,
  status TEXT DEFAULT 'PENDING',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_clean ON m82_multi_stream(clean_headline);
CREATE INDEX IF NOT EXISTS idx_status ON m82_multi_stream(status);

.headers on
.mode column
SELECT * FROM m82_score_config;
SQL

echo "✅ Tabla de score 0-100 lista"
