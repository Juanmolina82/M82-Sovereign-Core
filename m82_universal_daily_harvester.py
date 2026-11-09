#!/usr/bin/env python3
"""
M82 Sovereign Core v63.0.01-A - Universal Daily Multi-Asset Harvester Engine (Standalone Core)
Author: Lead Systems Engineer & AGI Orchestrator
Node: Charallave L4/L5 Edge
"""

import os
import sys
import math
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [M82_HARVESTER] - %(levelname)s - %(message)s')

class M82UniversalDailyHarvester:
    def __init__(self):
        self.db_path = os.path.expanduser("~/M82/m82_database.db")
        self._initialize_master_schema()

    def _initialize_master_schema(self):
        try:
            conn = sqlite3.connect(self.db_path, timeout=60.0)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA busy_timeout=60000;")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS m82_daily_macro_dossier (
                dossier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                m82_tag TEXT UNIQUE NOT NULL,
                asset_class TEXT NOT NULL,
                ticker TEXT NOT NULL,
                spot_price REAL NOT NULL,
                fcf_yield REAL,
                ev_ebitda REAL,
                forward_pe REAL,
                rsi_14d REAL,
                c_magnitude REAL NOT NULL,
                kelly_f_star REAL NOT NULL,
                is_irrational INTEGER NOT NULL,
                p_bunker REAL NOT NULL,
                p_expansion REAL NOT NULL,
                harvest_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()
            conn.close()
            logging.info("Schema m82_daily_macro_dossier validated/created successfully.")
        except Exception as e:
            logging.error(f"Error initializing Master Harvester Schema: {str(e)}")

    def _calculate_quantum_vector(self, val_a, bench_b=1.68, alpha_w=0.30, beta_w=0.70):
        # Tensor M82: Hipotenusa de Magnitud c
        c_magnitude = math.sqrt((val_a ** 2) + (bench_b ** 2))
        
        # Kelly Cuántico f* = (alpha - beta) / c
        kelly_f_star = (alpha_w - beta_w) / c_magnitude if c_magnitude != 0 else 0.0
        kelly_f_star = abs(kelly_f_star)
        
        # Superposición de Probabilidad (P_BUNKER / P_EXPANSION)
        p_bunker = round(1.0 / (1.0 + math.exp(-c_magnitude + 3.0)), 4)
        p_expansion = round(1.0 - p_bunker, 4)
        is_irrational = 1 if c_magnitude > 2.0 else 0
        
        return {
            "c_magnitude": c_magnitude,
            "kelly_f_star": kelly_f_star,
            "is_irrational": is_irrational,
            "p_bunker": p_bunker,
            "p_expansion": p_expansion
        }

    def ingest_asset_signal(self, asset_class, ticker, spot, fcf_yield=0.0, ev_ebitda=0.0, fwd_pe=0.0, rsi=0.0):
        today_str = datetime.now().strftime("%Y%m%d")
        tag = f"v63.0.01-A-DOSSIER-{ticker}-{today_str}"
        
        # Normalización Dimensional de Vector val_a
        if fcf_yield and float(fcf_yield) > 0:
            val_a = float(fcf_yield)
        elif ticker in ("XAU", "GOLD", "GC"):
            val_a = 7.79  # Gold/Silver Ratio (77.90 / 10)
        elif ticker in ("WTI", "BRENT", "CL"):
            val_a = 2.78  # Crack Spread normalizado
        elif ticker in ("HG", "COPPER"):
            val_a = 3.25  # Momentum Cobre normalizado
        elif fwd_pe and float(fwd_pe) > 0:
            val_a = 100.0 / float(fwd_pe)  # Earnings Yield Equivalent
        else:
            val_a = 2.78

        meta = self._calculate_quantum_vector(val_a)
        c_mag = meta["c_magnitude"]
        kelly_f = meta["kelly_f_star"]
        is_irr = meta["is_irrational"]
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=60.0)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO m82_daily_macro_dossier 
            (m82_tag, asset_class, ticker, spot_price, fcf_yield, ev_ebitda, forward_pe, rsi_14d, c_magnitude, kelly_f_star, is_irrational, p_bunker, p_expansion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (tag, asset_class, ticker, spot, fcf_yield, ev_ebitda, fwd_pe, rsi, c_mag, kelly_f, is_irr, meta["p_bunker"], meta["p_expansion"]))
            conn.commit()
            conn.close()
            logging.info(f"Asset [{ticker}] ingested successfully (c={c_mag:.4f}, f*={kelly_f:.4f}).")
        except Exception as e:
            logging.error(f"Error inserting asset signal for {ticker}: {str(e)}")
            
        return meta

if __name__ == "__main__":
    harvester = M82UniversalDailyHarvester()
    print("M82 Universal Daily Harvester Engine (Standalone) initialized successfully.")
