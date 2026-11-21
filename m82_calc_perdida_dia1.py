import sqlite3, os

db_path = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(db_path, timeout=30)
c = conn.cursor()

# Valores validados hoy en M82 Wire Workspace
c.execute("SELECT brent_price, dubai_squeeze, red_day_flag, consecutive_red_days FROM m82_mcn_checklist ORDER BY id DESC LIMIT 1")
row = c.fetchone()

if not row:
    print("❌ No hay registro en m82_mcn_checklist")
    exit()

brent, squeeze, red_flag, consec = row
fisico = brent + squeeze # $106.14 + $13.14 = $119.28

# Precios de transferencia del expediente PID 22071
transferencias = [-40.0, -54.65]

print(f"\n=== M82 DIA 1 - 28/09/2026 ===")
print(f"Brent M82 Wire: ${brent:.2f}")
print(f"Dubai Squeeze: ${squeeze:.2f}")
print(f"Crudo Fisico Real: ${fisico:.2f} /bbl")
print(f"Red Day Flag: {red_flag} | Consecutivo: {consec}")
print(f"---------------------------")

# Si tienes tabla de volumenes, la usa. Si no, calcula por barril
try:
    c.execute("SELECT SUM(volumen_bbl) FROM m82_volumen_pid22071 WHERE fecha = date('now')")
    vol = c.fetchone()[0]
except:
    vol = None

for precio_transf in transferencias:
    perdida_por_bbl = fisico - precio_transf
    print(f"\nTransfer a ${precio_transf}/bbl:")
    print(f" Perdida por bbl: ${fisico:.2f} - (${precio_transf}) = ${perdida_por_bbl:.2f}")
    if vol:
        perdida_total = perdida_por_bbl * vol
        print(f" Volumen hoy: {vol:,.0f} bbl")
        print(f" PERDIDA TOTAL DIA 1: ${perdida_total:,.2f}")

# Insertar en log de auditoria
from datetime import datetime
now = datetime.now().isoformat()
for pt in transferencias:
    perdida = fisico - pt
    c.execute("""
        INSERT INTO m82_perdida_audit (timestamp, brent, squeeze, fisico, precio_transfer, perdida_bbl, red_day_flag)
        VALUES (?,?,?,?,?,?,?)
    """, (now, brent, squeeze, fisico, pt, perdida, red_flag))

conn.commit()
conn.close()
print(f"\n✅ Auditoria guardada en m82_perdida_audit")
