#!/usr/bin/env python3
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def show_pnl():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = """
    SELECT 
        p.asset,
        p.current_qty,
        p.avg_entry_price,
        pt.last_price,
        ROUND((pt.last_price - p.avg_entry_price) * p.current_qty, 2) AS unrealized_pnl_usd,
        ROUND(((pt.last_price - p.avg_entry_price) / p.avg_entry_price) * 100, 2) AS return_pct
    FROM positions p
    LEFT JOIN price_ticks pt ON p.asset = pt.asset
    WHERE p.current_qty != 0 AND p.asset IS NOT NULL AND p.asset != 'NONE';
    """
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    
    print("\n=================== 🏛 M82 QUANT DESK: PnL MONITOR ===================")
    if not rows:
        print("Sin posiciones abiertas en cartera.")
    else:
        print(f"{'ASSET':<10} | {'QTY':<12} | {'ENTRY':<8} | {'LAST':<8} | {'PnL (USD)':<12} | {'RETURN %':<8}")
        print("-" * 72)
        for r in rows:
            asset, qty, entry, last, pnl, ret = r
            last_str = f"{last:.4f}" if last is not None else "N/A"
            pnl_str = f"${pnl:+,.2f}" if pnl is not None else "$0.00"
            ret_str = f"{ret:+.2f}%" if ret is not None else "0.00%"
            print(f"{asset:<10} | {qty:<12.2f} | {entry:<8.4f} | {last_str:<8} | {pnl_str:<12} | {ret_str:<8}")
    print("======================================================================\n")

if __name__ == "__main__":
    show_pnl()
