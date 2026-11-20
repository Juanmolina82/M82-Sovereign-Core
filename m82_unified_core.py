#!/usr/bin/env python3
import os, sys, time, gc, sqlite3, subprocess

M82 = os.path.expanduser("~/M82")
DB = os.path.join(M82, "m82_database.db")
LOGS = os.path.join(M82, "logs")
os.makedirs(LOGS, exist_ok=True)

def ensure_hub_8286():
    hub = os.path.join(M82, "8286.py")
    if os.path.exists(hub):
        chk = subprocess.run(["pgrep", "-f", "[8]286.py"], stdout=subprocess.DEVNULL)
        if chk.returncode != 0:
            with open(os.path.join(LOGS, "hub_8286.log"), "a") as lf:
                subprocess.Popen(["nice", "-n", "10", sys.executable, "-O", hub], stdout=lf, stderr=lf, start_new_session=True)

def cycle_76_daemons_lite():
    # Ejecutar telemetria puntual (one-shot) sin dejar subprocesos residentes
    bridge = os.path.join(M82, "m82_refinitiv_realtime_bridge.py")
    if os.path.exists(bridge):
        try:
            subprocess.run([sys.executable, "-O", bridge], timeout=25, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    # Mantenimiento pasivo WAL + FTS5 sin bloquear
    try:
        c = sqlite3.connect(DB, timeout=60.0)
        c.execute("PRAGMA journal_mode=WAL;")
        c.execute("PRAGMA synchronous=NORMAL;")
        c.execute("PRAGMA busy_timeout=60000;")
        c.execute("UPDATE m82_swarm_daemons SET status='ACTIVE_UNIFIED_LITE', updated_at=?;", (time.time(),))
        c.commit()
        c.close()
    except Exception:
        pass
    gc.collect()

if __name__ == "__main__":
    ensure_hub_8286()
    while True:
        ensure_hub_8286()
        cycle_76_daemons_lite()
        time.sleep(120)
