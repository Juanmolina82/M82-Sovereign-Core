#!/usr/bin/env python3
import sqlite3, os, time, random

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
BASE_PRICES = {
    "VENZ34": 0.4200,
    "PDVSA26": 0.3100,
    "WTI": 78.50,
    "BRENT": 82.10,
    "XAUUSD": 2650.00,
    "BTCUSD": 63500.00
}

def update_prices():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for asset, base in BASE_PRICES.items():
        c.execute("SELECT last_price FROM price_ticks WHERE asset = ?", (asset,))
        row = c.fetchone()
        curr = row[0] if row and row[0] else base
        delta = curr * random.uniform(-0.002, 0.002)
        new_last = round(curr + delta, 4)
        spread = round(new_last * 0.005, 4)
        bid = round(new_last - (spread / 2), 4)
        ask = round(new_last + (spread / 2), 4)
        c.execute("""
            INSERT INTO price_ticks (asset, bid, ask, last_price, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(asset) DO UPDATE SET
                bid = excluded.bid, ask = excluded.ask, last_price = excluded.last_price, updated_at = CURRENT_TIMESTAMP
        """, (asset, bid, ask, new_last))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        try: update_prices()
        except Exception as e: print(f"⚠️ Error PriceFeeder: {e}")
        time.sleep(5)
