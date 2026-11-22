#!/usr/bin/env python3
import re
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"

print("=== [1/4] APLICANDO FRENO DE EMERGENCIA AL DESPACHO DESCONTROLADO ===")
for proc_name in ("orch.py", "m82_hud_burst10_per_daemon.py", "m82_hud_burst5.py"):
    subprocess.run(["pkill", "-f", proc_name], stderr=subprocess.DEVNULL)

# Re-imponer freno seguro en scripts de envio al bot (max 3 por ciclo + pausa 4.0s)
patched_bot = []
for py_file in BASE_DIR.rglob("*.py"):
    if "backups" in py_file.parts or py_file.name in ("m82_emergency_audit_and_control.py", "m82_realtime_energy_feed_daemon.py"):
        continue
    try:
        src = py_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    if any(k in src for k in ("api.telegram.org", "sendMessage_DISABLED_HUD", "sendMessage", "HUD CARDS")):
        orig = src
        src = re.sub(r'(LIMIT\s+)10\b', r'\g<1>3', src, flags=re.IGNORECASE)
        src = re.sub(r'\[:10\]', '[:3]', src)
        src = re.sub(r'(range\()10(\))', r'\g<1>3\g<2>', src)
        src = re.sub(r'((?:max_cards|max_send|burst_limit|per_daemon|limit)\s*=\s*)10\b', r'\g<1>3', src, flags=re.IGNORECASE)
        src = src.replace("time.sleep(1.2)", "time.sleep(4.0)")
        if src != orig:
            py_file.write_text(src, encoding="utf-8")
            patched_bot.append(str(py_file.relative_to(BASE_DIR)))

print(f"[+] Freno aplicado en {len(patched_bot)} scripts:", ", ".join(patched_bot) if patched_bot else "OK")

print("\n=== [2/4] AUDITORIA DE ARQUITECTURA PRINCIPAL macro_dossier (DDL v60) ===")
con = sqlite3.connect(str(DB_PATH), timeout=60.0)
con.execute("PRAGMA journal_mode=WAL;")
con.execute("PRAGMA busy_timeout=60000;")

jmode = con.execute("PRAGMA journal_mode;").fetchone()[0]
integ = con.execute("PRAGMA integrity_check;").fetchone()[0]
md_cols = [r[1] for r in con.execute("PRAGMA table_info(macro_dossier);")]
v60_ok = all(c in md_cols for c in ("validated", "alpha_score", "tail_risk_index", "desk_cluster"))
total_md = con.execute("SELECT COUNT(*) FROM macro_dossier;").fetchone()[0]
total_reg = con.execute("SELECT COUNT(*) FROM m82_daemons_registry;").fetchone()[0]
bad_exp = con.execute("SELECT COUNT(*) FROM macro_dossier WHERE active_exposure > 0.30;").fetchone()[0]
quote = con.execute("SELECT merey16_price, wti_price, wti_chg_pct, brent_price, brent_chg_pct, updated_at FROM m82_live_market_quotes WHERE id=1;").fetchone()

print(f"  - SQLite Journal Mode     : {jmode.upper()} (Requerido: WAL)")
print(f"  - DB Integrity Check      : {integ.upper()}")
print(f"  - Esquema DDL v60         : {'VERIFICADO OK' if v60_ok else 'FALTAN COLUMNAS'} -> {md_cols}")
print(f"  - Registros macro_dossier : {total_md} filas | Daemons Indexados: {total_reg}")
print(f"  - Bloqueo BUNKER 0.30x    : {'RESPETADO (0 violaciones > 0.30x)' if bad_exp == 0 else f'ALERTA ({bad_exp} filas > 0.30x)'}")
if quote:
    print(f"  - Precios Real-Time DB    : MEREY 16=${quote[0]:.2f} | WTI=${quote[1]:.2f} ({quote[2]:+.2f}%) | BRENT=${quote[3]:.2f} ({quote[4]:+.2f}%) | {quote[5]}")

print("\n=== [3/4] AUDITORIA DE LOS ULTIMOS 12 VECTORES EN macro_dossier ===")
for r in con.execute("""
    SELECT rowid, source, COALESCE(desk_cluster,'N/A'), ROUND(COALESCE(alpha_score,0),2),
           ROUND(COALESCE(tail_risk_index,0),2), ROUND(COALESCE(active_exposure,0),2), substr(headline,1,68)
    FROM macro_dossier ORDER BY rowid DESC LIMIT 12
"""):
    print(f"  #{r[0]:3d} | {r[1]:30s} | {r[2]:20s} | A={r[3]:.2f} T={r[4]:.2f} Exp={r[5]:.2f}x | {r[6]}")

con.commit()
con.execute("PRAGMA wal_checkpoint(PASSIVE);")
con.close()

print("\n=== [4/4] REINICIANDO orch.py EN MODO CONTROLADO (MAX 3 / PAUSA 4.0s) ===")
if (BASE_DIR / "orch.py").exists():
    lf = open(BASE_DIR / "logs" / "orch_controlled.log", "a")
    p = subprocess.Popen(["nohup", "python3", "-u", str(BASE_DIR / "orch.py")], stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
    print(f"[+] orch.py REINICIADO BAJO CONTROL | PID={p.pid}")
