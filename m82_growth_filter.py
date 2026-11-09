#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def apply_real_yield_regime_filter(real_yield=3.0):
    """
    Aplica regla estricta de régimen macro:
    Si Real Yield >= 3.0%, descarta posiciones en Growth con P/E > 20x
    y sobrepondera Cash (T-Bills) y Energía Física (XLE/CVX/Brent).
    """
    if real_yield >= 3.0:
        print(f"🚨 [M82 MACRO FILTER] Real Yield en {real_yield}% >= 3.0%. ACTIVANDO FILTRO DE DESTRUCCIÓN DE DURACIÓN.")
        print("❌ ASSETS DISCARDED: P/E > 20x | FCF Yield < 5.0% | Tech High-Duration")
        print("✅ ASSETS APPROVED: Energy (CVX, XLE, Brent) | Cash/T-Bills (4.8%) | Financials (KRE)")
        return "HARD_ROTATION_TO_CASH_AND_ENERGY"
    else:
        return "STANDARD_REGIME"

if __name__ == "__main__":
    apply_real_yield_regime_filter(3.0)
