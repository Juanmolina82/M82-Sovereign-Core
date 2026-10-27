#!/usr/bin/env python3
import sqlite3
import os
import sys

DB_PATH = "m82_database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def run_analytics():
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: {DB_PATH} no existe.")
        return

    conn = get_db()
    cur = conn.cursor()

    # 1. Spreads Energéticos (Brent / WTI / Físico)
    cur.execute("""
        SELECT headline, risk_score, timestamp 
        FROM signals 
        WHERE headline LIKE '%Brent%' OR headline LIKE '%WTI%' 
        ORDER BY id DESC LIMIT 5
    """)
    rows = cur.fetchall()

    print("==================================================")
    print(" 📊 M82 ANALYTICS ENGINE — SPREADS & CURVAS ")
    print("==================================================")

    if rows:
        print("\n🛢️ [COMMODITIES / ENERGY SNAPSHOT]")
        for r in rows:
            print(f"  • {r['headline']} (Risk: {r['risk_score']})")
    else:
        print("\n🛢️ [COMMODITIES] Sin datos suficientes de Brent/WTI en WAL.")

    # 2. Deuda Estructurada y Curvas
    cur.execute("""
        SELECT headline, risk_score, category 
        FROM signals 
        WHERE category = 'FIXED_INCOME' 
        ORDER BY id DESC LIMIT 5
    """)
    fi_rows = cur.fetchall()

    if fi_rows:
        print("\n📈 [FIXED INCOME & STRUCTURED DEBT]")
        for r in fi_rows:
            print(f"  • {r['headline']} | Risk: {r['risk_score']}")

    print("\n==================================================")
    conn.close()

if __name__ == "__main__":
    run_analytics()
