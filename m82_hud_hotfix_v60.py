
def _m82_live_banner():
    try:
        import sqlite3 as _s
        _c = _s.connect("file:/data/data/com.termux/files/home/M82/m82_database.db?mode=ro", uri=True, timeout=15.0)
        _r = _c.execute("SELECT btc_price, btc_chg_pct, merey16_price, wti_price, wti_chg_pct, brent_price FROM m82_live_market_quotes WHERE id=1").fetchone()
        _c.close()
        if _r and _r[0]:
            return f"BTC: ${_r[0]:,.0f} ({_r[1]:+.2f}%) | MEREY 16: ${_r[2]:.2f} | WTI: ${_r[3]:.2f} | BRENT: ${_r[5]:.2f}"
    except Exception:
        pass
    return "BTC: LIVE | MEREY 16: LIVE | WTI: LIVE | BRENT: LIVE"

#!/usr/bin/env python3
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

ts_tag = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
if (BASE_DIR / "orch.py").exists():
    shutil.copy2(BASE_DIR / "orch.py", BACKUP_DIR / f"orch.py.{ts_tag}.bak")

# 1. Purga de ruido editorial + Trigger anti-ruido + Indexacion del demonio real-time
con = sqlite3.connect(str(DB_PATH), timeout=60.0)
con.execute("PRAGMA journal_mode=WAL;")
con.execute("PRAGMA busy_timeout=60000;")

con.executescript("""
DELETE FROM macro_dossier
WHERE lower(headline) LIKE '%book review:%'
   OR lower(headline) LIKE '%rachel maddow%'
   OR lower(headline) LIKE '%movie review:%'
   OR lower(headline) LIKE '%horoscope%'
   OR lower(headline) LIKE '%crossword%';

DROP TRIGGER IF EXISTS trg_macro_dossier_noise_guard;
CREATE TRIGGER trg_macro_dossier_noise_guard
BEFORE INSERT ON macro_dossier
BEGIN
    SELECT CASE
        WHEN lower(NEW.headline) LIKE '%book review:%'
          OR lower(NEW.headline) LIKE '%rachel maddow%'
          OR lower(NEW.headline) LIKE '%movie review:%'
          OR lower(NEW.headline) LIKE '%horoscope%'
          OR lower(NEW.headline) LIKE '%crossword%'
        THEN RAISE(IGNORE)
    END;
END;
""")

cols = {r[1] for r in con.execute("PRAGMA table_info(m82_daemons_registry)")}
name_col = "daemon_name" if "daemon_name" in cols else ("name" if "name" in cols else list(cols)[0])
c = [name_col]
v = ["m82_realtime_energy_feed_daemon.py"]
if "script_path" in cols:
    c.append("script_path")
    v.append("/data/data/com.termux/files/home/M82/desks/m82_realtime_energy_feed_daemon.py")
if "desk_category" in cols:
    c.append("desk_category")
    v.append("GLOBAL_ENERGY_COMMODITIES_DESK")
if "status" in cols:
    c.append("status")
    v.append("ACTIVE")
if "is_running" in cols:
    c.append("is_running")
    v.append(1)

q_marks = ",".join(["?"] * len(c))
con.execute(f"INSERT OR REPLACE INTO m82_daemons_registry ({','.join(c)}) VALUES ({q_marks});", v)
con.commit()
con.execute("PRAGMA wal_checkpoint(PASSIVE);")

total_daemons = con.execute("SELECT COUNT(*) FROM m82_daemons_registry").fetchone()[0]
live_row = con.execute("SELECT merey16_price, wti_price, wti_chg_pct, brent_price, brent_chg_pct, updated_at FROM m82_live_market_quotes WHERE id=1").fetchone()
con.close()

print(f"[+] REGISTRO MAESTRO ACTUALIZADO: {total_daemons} DAEMONS INDEXADOS")
if live_row:
    print(f"[+] COTIZACION REAL-TIME ACTIVA EN DB: MEREY 16=${live_row[0]:.2f} | WTI=${live_row[1]:.2f} ({live_row[2]:+.2f}%) | BRENT=${live_row[3]:.2f} ({live_row[4]:+.2f}%) | {live_row[5]}")

# 2. Parchear orch.py y generadores HUD para leer m82_live_market_quotes en vivo y eliminar truncamiento
DYNAMIC_HELPER = '''
def _m82_get_live_energy_banner():
    try:
        import sqlite3 as _sq
        _c = _sq.connect("file:/data/data/com.termux/files/home/M82/m82_database.db?mode=ro", uri=True, timeout=15.0)
        _r = _c.execute("SELECT merey16_price, wti_price, wti_chg_pct, brent_price FROM m82_live_market_quotes WHERE id=1").fetchone()
        _c.close()
        if _r:
            return _m82_live_banner()
    except Exception:
        pass
    return _m82_live_banner()
'''

patched_files = []
for py_file in BASE_DIR.rglob("*.py"):
    if "backups" in py_file.parts or py_file.name in ("m82_hud_hotfix_v60.py", "m82_realtime_energy_feed_daemon.py"):
        continue
    try:
        src = py_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    changed = False
    if "{brent}" in src or "{merey16}" in src:
        if "_m82_get_live_energy_banner" not in src:
            src = DYNAMIC_HELPER + "\n" + src
        src_new = re.sub(
            r'f?["\']MEREY 16:\s*\$83\.15[^"\']*114\.72["\']',
            "_m82_get_live_energy_banner()",
            src,
        )
        if src_new != src:
            src = src_new
            changed = True

    if "HUD CARDS" in src or "M82_SOVEREIGN WORKSPACE TELEMETRY WIRE" in src:
        src_new = re.sub(r'\[:(5[0-9]|6[0-9]|7[0-5])\]', "[:210]", src)
        if src_new != src:
            src = src_new
            changed = True

    if changed:
        py_file.write_text(src, encoding="utf-8")
        patched_files.append(str(py_file.relative_to(BASE_DIR)))

print(f"[+] ARCHIVOS HUD PARCHEADOS ({len(patched_files)}):", ", ".join(patched_files) if patched_files else "Ninguno")

# 3. Reiniciar orch.py en limpio
if (BASE_DIR / "orch.py").exists():
    subprocess.run(["pkill", "-f", "orch.py"], stderr=subprocess.DEVNULL)
    log_f = open(BASE_DIR / "orch.log", "a")
    p = subprocess.Popen(["nohup", "python3", "-u", str(BASE_DIR / "orch.py")], stdout=log_f, stderr=subprocess.STDOUT, start_new_session=True)
    print(f"[+] orch.py REINICIADO CON PRECIOS REAL-TIME | PID={p.pid}")
