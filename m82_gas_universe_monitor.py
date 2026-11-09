#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M82 SOVEREIGN CORE :: GAS UNIVERSE LIVE MONITOR
Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
"""

import sqlite3
import os

DB = os.path.expanduser("~/M82/m82_database.db")
con = sqlite3.connect(DB, timeout=60.0)
cur = con.cursor()

print("\n=========================================================================================")
print("  M82 VENEZUELA GAS UNIVERSE — LSEG WORKSPACE STREAMING (jmmp@molina82.com)")
print("=========================================================================================")
print(f"{'SYMBOL':<14} | {'CONTRACT & PHASE':<46} | {'SPOT PRICE':<10} | {'CHANGE':<8}")
print("-" * 89)

for row in cur.execute("""
    SELECT symbol, contract_name, spot_price, daily_change 
    FROM m82_global_derivatives 
    WHERE asset_class='ENERGY_GAS_VE' 
    ORDER BY symbol ASC
"""):
    print(f"{row[0]:<14} | {row[1]:<46} | {row[2]:<10.2f} | {row[3]:^+7.2f}%")

print("-" * 89)
print("  GOBERNANZA: 🔒 BUNKER MODE / 0.30x LOCK | Exposición ~0.22x | VaR 1.68% | 100% Dry Powder")
print("=========================================================================================\n")

con.close()
