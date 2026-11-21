#!/usr/bin/env python3
import os, time, sqlite3, random

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
BASE_NOTIONAL_USD = 50000.0

# Umbrales de Gestión de Riesgo
STOP_LOSS_PCT = -0.03   # -3%
TAKE_PROFIT_PCT = 0.08  # +8%

def calculate_slippage(asset, spread):
    if asset in ["VENZ34", "PDVSA26"]: 
        return round(spread * random.uniform(0.3, 0.6), 4)
    elif asset in ["WTI", "BRENT", "XAUUSD"]: 
        return round(spread * random.uniform(0.05, 0.15), 4)
    return round(spread * 0.10, 4)

def check_risk_management():
    """Evalúa posiciones abiertas y ejecuta cierres automáticos por SL/TP"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = """
    SELECT p.asset, p.current_qty, p.avg_entry_price, pt.last_price, pt.bid, pt.ask
    FROM positions p
    JOIN price_ticks pt ON p.asset = pt.asset
    WHERE p.current_qty != 0;
    """
    c.execute(query)
    positions = c.fetchall()
    
    for pos in positions:
        asset, qty, entry_price, last_price, bid, ask = pos
        if not last_price or entry_price == 0: continue
        
        # Calcular retorno % actual
        ret_pct = (last_price - entry_price) / entry_price if qty > 0 else (entry_price - last_price) / entry_price
        
        close_reason = None
        if ret_pct <= STOP_LOSS_PCT:
            close_reason = f"STOP-LOSS TRIGGERED ({ret_pct*100:.2f}%)"
        elif ret_pct >= TAKE_PROFIT_PCT:
            close_reason = f"TAKE-PROFIT TRIGGERED ({ret_pct*100:.2f}%)"
            
        if close_reason:
            close_side = "SELL" if qty > 0 else "BUY"
            close_qty = abs(qty)
            fill_price = bid if close_side == "SELL" else ask
            
            # Registrar orden de cierre
            c.execute("""
                INSERT INTO orders (asset, side, order_type, qty, limit_price, fill_price, slippage, status)
                VALUES (?, ?, 'MARKET_CLOSE', ?, ?, ?, 0.0, 'FILLED')
            """, (asset, close_side, close_qty, last_price, fill_price))
            
            # Resetear posición a 0
            c.execute("UPDATE positions SET current_qty = 0.0, unrealized_pnl = 0.0, updated_at = CURRENT_TIMESTAMP WHERE asset = ?", (asset,))
            conn.commit()
            print(f"🚨 [RISK ENGINE] {close_reason} | Cierre {close_side} {close_qty} {asset} @ {fill_price}")
            
    conn.close()

def execute_signal(stream_id, source, alpha_score, assets_str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    asset_list = [a.strip() for a in assets_str.split(",")]
    target_asset = asset_list[0] if asset_list else "VENZ34"
    
    c.execute("SELECT bid, ask, last_price FROM price_ticks WHERE asset = ?", (target_asset,))
    price_row = c.fetchone()
    
    if not price_row or price_row[2] is None: 
        bid, ask, last_price = 0.4150, 0.4250, 0.4200
    else: 
        bid, ask, last_price = price_row
        
    spread = max(ask - bid, 0.0010) if (ask and bid) else 0.0050
    side = "BUY" if alpha_score > 0 else "SELL"
    
    slippage = calculate_slippage(target_asset, spread)
    fill_price = round(ask + slippage, 4) if side == "BUY" else round(bid - slippage, 4)
    qty = round(BASE_NOTIONAL_USD / fill_price, 2) if fill_price > 0 else 100000.0
    
    c.execute("""
        INSERT INTO orders (stream_id, asset, side, order_type, qty, limit_price, fill_price, slippage, status)
        VALUES (?, ?, ?, 'MARKET', ?, ?, ?, ?, 'FILLED')
    """, (stream_id, target_asset, side, qty, last_price, fill_price, slippage))
    
    c.execute("""
        INSERT INTO positions (asset, current_qty, avg_entry_price, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(asset) DO UPDATE SET
            current_qty = current_qty + excluded.current_qty,
            avg_entry_price = (avg_entry_price + excluded.avg_entry_price) / 2,
            updated_at = CURRENT_TIMESTAMP
    """, (target_asset, qty if side == "BUY" else -qty, fill_price))
    
    conn.commit()
    conn.close()
    print(f"🎯 [EXECUTION ENGINE] FILLED | {side} {qty} {target_asset} @ {fill_price} (Slippage: {slippage:+.4f})")

def run_execution_loop():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT s.id, s.daemon_source, s.alpha_score, s.asset_impact 
        FROM m82_multi_stream s
        LEFT JOIN orders o ON s.id = o.stream_id
        WHERE s.status = 'DISPATCHED' AND o.order_id IS NULL
        LIMIT 1
    """)
    row = c.fetchone()
    conn.close()
    
    if row:
        stream_id, source, score, assets = row
        execute_signal(stream_id, source, score, assets)
        
    # Evaluación constante de Stop-Loss / Take-Profit
    check_risk_management()

if __name__ == "__main__":
    while True:
        try: 
            run_execution_loop()
        except Exception as e: 
            print(f"⚠️ Error Execution Engine: {e}")
        time.sleep(5)
