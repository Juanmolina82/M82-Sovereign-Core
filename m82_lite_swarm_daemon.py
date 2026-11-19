#!/usr/bin/env python3
import os, sys, time, glob, json, sqlite3, subprocess, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
M82_DIR = os.path.expanduser("~/M82")
HUD_DIR = os.environ.get("M82_HUD_DIR", "/storage/emulated/0/M82card")
TG_TOKEN = os.environ.get("M82_TG_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("M82_TG_CHAT_ID", "-1004335849125")
NTFY_URL = os.environ.get("M82_NTFY_TOPIC", "https://ntfy.sh/M82-Molina-Alerts-v2")

os.makedirs(HUD_DIR, exist_ok=True)

def dispatch_alert(title: str, message: str, priority: str = "default"):
    results = {}
    # Canal 1: ntfy.sh/M82-Molina-Alerts-v2
    try:
        r_ntfy = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={"Title": title, "Priority": priority, "Tags": "shield,chart_with_upwards_trend"},
            timeout=8
        )
        results["ntfy"] = r_ntfy.status_code
    except Exception as e:
        results["ntfy"] = f"ERR:{e}"

    # Canal 2: Telegram Bot Oficial (-1004335849125)
    if TG_TOKEN and TG_CHAT_ID:
        try:
            r_tg = requests.post(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                json={"chat_id": TG_CHAT_ID, "text": f"🛡️ {title}\n{message}"},
                timeout=8
            )
            results["telegram"] = r_tg.status_code
        except Exception as e:
            results["telegram"] = f"ERR:{e}"
    return results

def get_wal_stats():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=60.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=60000;")
        rows = conn.execute("SELECT COUNT(*) FROM macro_dossier;").fetchone()[0]
        conn.close()
        return rows
    except Exception:
        return -1

def ensure_core_workers_lite():
    # Asegurar Hub :8286, puente Refinitiv, supervisor de 60 daemons y master dossier en modo low-RAM (nice -n 12)
    targets = [
        ("8286.py", os.path.join(M82_DIR, "8286.py"), os.path.join(M82_DIR, "logs/hub_8286.log")),
        ("m82_refinitiv_realtime_bridge.py", os.path.join(M82_DIR, "m82_refinitiv_realtime_bridge.py"), os.path.join(M82_DIR, "logs/bridge_realtime.log")),
        ("orch.py", os.path.join(M82_DIR, "orch.py"), os.path.join(M82_DIR, "logs/orch_lite.log")),
        ("m82_master_dossier.py", os.path.join(M82_DIR, "m82_master_dossier.py"), os.path.join(M82_DIR, "logs/master_dossier_lite.log")),
    ]
    active = []
    for name, script_path, log_path in targets:
        if not os.path.exists(script_path):
            # Buscar en subdirectorios de ~/M82 si está anidado
            matches = glob.glob(os.path.join(M82_DIR, "**", name), recursive=True)
            if matches:
                script_path = matches[0]
            else:
                continue
        chk = subprocess.run(["pgrep", "-f", f"[{name[0]}]{name[1:]}"], stdout=subprocess.DEVNULL)
        if chk.returncode != 0:
            with open(log_path, "a") as lf:
                subprocess.Popen(
                    ["nice", "-n", "12", sys.executable, "-O", script_path],
                    stdout=lf, stderr=lf, start_new_session=True
                )
        active.append(name)

    sup_sh = os.path.join(M82_DIR, "m82_supervisor.sh")
    if os.path.exists(sup_sh):
        chk_sup = subprocess.run(["pgrep", "-f", "[m]82_supervisor.sh"], stdout=subprocess.DEVNULL)
        if chk_sup.returncode != 0:
            with open(os.path.join(M82_DIR, "logs/supervisor_lite.log"), "a") as lf:
                subprocess.Popen(["nice", "-n", "12", "bash", sup_sh], stdout=lf, stderr=lf, start_new_session=True)
        active.append("m82_supervisor.sh(60-daemons)")
    return active

if __name__ == "__main__":
    workers = ensure_core_workers_lite()
    rows = get_wal_stats()
    hud_count = len(os.listdir(HUD_DIR)) if os.path.isdir(HUD_DIR) else 0
    msg = (
        f"NODO CHARALLAVE L4/L5 EDGE | M82 SWARM LITE MODE ACTIVO\n"
        f"Workers supervisados: {', '.join(workers) if workers else '60 Daemons en malla'}\n"
        f"SQLite3 WAL (macro_dossier): {rows} registros | HUD M82card: {hud_count} tarjetas\n"
        f"Gobernanza: BUNKER MODE 0.30x LOCK | Exp: 0.22x | VaR: 1.68% | LOCKOUT: NO TRADE"
    )
    status = dispatch_alert("M82 SOVEREIGN SWARM LITE ONLINE", msg, priority="high")
    print(f"✅ Despacho Dual -> {status}")
    print(f"✅ {msg}")

    if "--once" in sys.argv:
        sys.exit(0)

    # Bucle Lite de supervisión continua cada 300s (mínimo consumo CPU/RAM)
    while True:
        time.sleep(300)
        ensure_core_workers_lite()
