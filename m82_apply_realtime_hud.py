#!/usr/bin/env python3
import re
import sqlite3
import subprocess
from pathlib import Path

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"

# 1. Actualizar DB: filtro anti-ruido ampliado + indexacion del demonio real-time
con = sqlite3.connect(str(DB_PATH), timeout=60.0)
con.execute("PRAGMA journal_mode=WAL;")
con.execute("PRAGMA busy_timeout=60000;")

con.executescript("""
DELETE FROM macro_dossier
WHERE lower(headline) LIKE '%book review:%'
   OR lower(headline) LIKE '%rachel maddow%'
   OR lower(headline) LIKE '%the fed explained - who we are%';

DROP TRIGGER IF EXISTS trg_macro_dossier_noise_guard;
CREATE TRIGGER trg_macro_dossier_noise_guard
BEFORE INSERT ON macro_dossier
BEGIN
    SELECT CASE
        WHEN lower(NEW.headline) LIKE '%book review:%'
          OR lower(NEW.headline) LIKE '%rachel maddow%'
          OR lower(NEW.headline) LIKE '%movie review:%'
          OR lower(NEW.headline) LIKE '%the fed explained - who we are%'
        THEN RAISE(IGNORE)
    END;
END;
""")

cols = {r[1] for r in con.execute("PRAGMA table_info(m82_daemons_registry)")}
name_col = "daemon_name" if "daemon_name" in cols else ("name" if "name" in cols else list(cols)[0])
c = [name_col]
v = ["m82_realtime_energy_feed_daemon.py"]
if "script_path" in cols:
    c.append("script_path"); v.append("/data/data/com.termux/files/home/M82/desks/m82_realtime_energy_feed_daemon.py")
if "desk_category" in cols:
    c.append("desk_category"); v.append("GLOBAL_ENERGY_COMMODITIES_DESK")
if "status" in cols:
    c.append("status"); v.append("ACTIVE")
if "is_running" in cols:
    c.append("is_running"); v.append(1)

con.execute(f"INSERT OR REPLACE INTO m82_daemons_registry ({','.join(c)}) VALUES ({','.join(['?']*len(c))});", v)
con.commit()
con.execute("PRAGMA wal_checkpoint(PASSIVE);")
total_d = con.execute("SELECT COUNT(*) FROM m82_daemons_registry").fetchone()[0]
q = con.execute("SELECT merey16_price, wti_price, wti_chg_pct, brent_price, brent_chg_pct, updated_at FROM m82_live_market_quotes WHERE id=1").fetchone()
con.close()

print(f"[+] DB OK | Daemons={total_d} | Quote={q}")

# 2. Localizar y parchear cualquier script en ~/M82 que aun tenga 114.72 o 83.15
HELPER = '''
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
'''

patched = []
for f in BASE_DIR.rglob("*.py"):
    if "backups" in f.parts or f.name in ("m82_apply_realtime_hud.py", "m82_realtime_energy_feed_daemon.py"):
        continue
    txt = f.read_text(encoding="utf-8", errors="ignore")
    if "114.72" in txt or "83.15" in txt:
        if "_m82_live_banner" not in txt:
            txt = HELPER + "\n" + txt
        txt_new = re.sub(r'f?["\']MEREY 16:[^"\']*114\.72["\']', "_m82_live_banner()", txt)
        if txt_new == txt:
            txt_new = txt.replace("114.72", "{brent}").replace("83.15", "{merey16}")
        f.write_text(txt_new, encoding="utf-8")
        patched.append(str(f.relative_to(BASE_DIR)))

print("[+] SCRIPTS HUD ACTUALIZADOS:", patched)

# 3. Reiniciar procesos HUD / orch.py para que apliquen el nuevo banner en vivo
for target in patched:
    fname = Path(target).name
    subprocess.run(["pkill", "-f", fname], stderr=subprocess.DEVNULL)
    log_p = BASE_DIR / "logs" / f"{fname[:-3]}.log"
    log_p.parent.mkdir(parents=True, exist_ok=True)
    with open(log_p, "a") as lf:
        p = subprocess.Popen(["nohup", "python3", "-u", str(BASE_DIR / target)], stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
    print(f"[+] REINICIADO EN VIVO: {target} | PID={p.pid}")
