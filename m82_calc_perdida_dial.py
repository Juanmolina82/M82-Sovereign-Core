#!/usr/bin/env python3
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

conn = sqlite3.connect(DB_PATH, timeout=30.0)
c = conn.cursor()

c.execute("SELECT brent_price, dubai_squeeze, red_day_flag, consecutive_red_days FROM m82_mcn_checklist ORDER BY id DESC LIMIT 1")
row = c.fetchone()

if not row:
    print("❌ No hay registro en m82_mcn_checklist")
    exit()

brent, squeeze, red_flag, consec = row
fisico = brent + squeeze  # $106.14 + $13.14 = $119.28

transferencias = [-40.0, -54.65]

print("=== M82 DIA 1 - " + datetime.now().strftime("%Y-%m-%d") + " ===")
print(f"Brent M82 Wire: ${brent:.2f}")
print(f"Dubai Squeeze: ${squeeze:.2f}")
print(f"Crudo Físico Real: ${fisico:.2f} /bbl")
print(f"Red Day Flag: {red_flag} | Consecutive: {consec}\n")

try:
    c.execute("SELECT SUM(volumen_bbl) FROM m82_volumen_pid22071 WHERE fecha = date('now')")
    vol_row = c.fetchone()
    vol = vol_row[0] if vol_row and vol_row[0] is not None else 400000.0
except Exception:
    vol = 400000.0

now = datetime.now().isoformat()

for pt in transferencias:
    precio_transf = brent + pt if pt < 0 else pt
    perdida_por_bbl = fisico - precio_transf
    
    print(f"Transferencia (Descuento de ${abs(pt):.2f}/bbl vs Brent):")
    print(f"  -> Precio Transferencia: ${precio_transf:.2f}/bbl")
    print(f"  -> Pérdida por bbl: ${perdida_por_bbl:.2f}/bbl")
    
    if vol:
        perdida_total = perdida_por_bbl * vol
        print(f"  -> Volumen hoy: {vol:,.0f} bbl")
        print(f"  -> PÉRDIDA TOTAL DÍA: ${perdida_total:,.2f}\n")
        
    c.execute("""
        INSERT INTO m82_perdida_audit (timestamp, brent, squeeze, fisico, precio_transfer, perdida_bbl, red_day_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (now, brent, squeeze, fisico, precio_transf, perdida_por_bbl, red_flag))

conn.commit()
conn.close()

print("✅ Auditoría guardada exitosamente en m82_perdida_audit")
