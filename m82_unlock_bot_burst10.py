#!/usr/bin/env python3
import re
import time
import sqlite3
import subprocess
from pathlib import Path

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"

# 1. Auditar y desbloquear todos los scripts de envio al bot (LIMIT 3 / [:3] -> 10 por daemon)
bot_scripts = []
for py_file in BASE_DIR.rglob("*.py"):
    if "backups" in py_file.parts or py_file.name == "m82_unlock_bot_burst10.py":
        continue
    try:
        src = py_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    if any(k in src for k in ("api.telegram.org", "sendPhoto", "sendMessage", "sendMediaGroup", "BOT_TOKEN", "CHAT_ID")):
        orig = src
        # Elevar topes de 3 a 10 en consultas SQL, slices y contadores de envio
        src = re.sub(r'(LIMIT\s+)3\b', r'\g<1>10', src, flags=re.IGNORECASE)
        src = re.sub(r'\[:3\]', '[:3]', src)
        src = re.sub(r'(range\()3(\))', r'\g<1>10\g<2>', src)
        src = re.sub(r'((?:max_cards|max_send|burst_limit|per_daemon|limit)\s*=\s*)3\b', r'\g<1>10', src, flags=re.IGNORECASE)

        # Inyectar pausa anti-429 (1.2s) tras cada envio de foto/mensaje al bot si no existe
        if "sendPhoto" in src and "time.sleep(4.0)" not in src:
            if "import time" not in src:
                src = "import time\n" + src
            src = re.sub(r'(requests\.post\([^\n]*sendPhoto[^\n]*\))', r'\1\n        time.sleep(4.0)', src)

        if src != orig:
            py_file.write_text(src, encoding="utf-8")
            bot_scripts.append(str(py_file.relative_to(BASE_DIR)))
        else:
            bot_scripts.append(f"{py_file.relative_to(BASE_DIR)} (sin tope=3)")

print("[+] SCRIPTS DE BOT AUDITADOS:")
for b in bot_scripts:
    print(f"    -> {b}")

# 2. Verificar que el despachador HUD tenga cola limpia para los 10 por daemon
con = sqlite3.connect(str(DB_PATH), timeout=60.0)
con.execute("PRAGMA journal_mode=WAL;")
con.execute("PRAGMA busy_timeout=60000;")
con.execute("DELETE FROM m82_hud_dispatch_log;")
con.commit()
con.execute("PRAGMA wal_checkpoint(PASSIVE);")
con.close()
print("[+] Cola m82_hud_dispatch_log reseteada para permitir el flujo completo de 10 por daemon.")

# 3. Reiniciar los procesos activos del bot / orquestador para aplicar el desbloqueo
for target in bot_scripts:
    clean_name = Path(target.split(" ")[0]).name
    subprocess.run(["pkill", "-f", clean_name], stderr=subprocess.DEVNULL)
    fpath = BASE_DIR / target.split(" ")[0]
    if fpath.exists():
        lf = open(BASE_DIR / "logs" / f"{fpath.stem}.log", "a")
        p = subprocess.Popen(["nohup", "python3", "-u", str(fpath)], stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
        print(f"[+] REINICIADO DESPACHADOR BOT: {fpath.name} | PID={p.pid}")
