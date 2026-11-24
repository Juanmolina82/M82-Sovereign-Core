import sys
sys.path.insert(0, "/data/data/com.termux/files/home/M82/scripts")
from lseg_wal_reader import get_latest_lseg_live, check_lseg_thresholds

#!/usr/bin/env python3
import os, time, sqlite3, random
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

MACRO_EVENT_POOL = [
    ("VENZ34_DEBT", "Venezuela sovereign debt restructured trading range updated", 0.75, "VENZ34"),
    ("LATAM_POLITICS", "LatAm energy corridor bilateral trade agreement signed", 0.45, "WTI"),
    ("SWIFT_FLOWS", "Cross-border settlement volume spikes in energy clearing desk", 0.60, "WTI"),
    ("CITGO_OFAC_DESK", "OFAC extends protection license for Citgo assets", 0.80, "PDVSA26"),
    ("PDVSA26_SWAPS", "PDVSA bond yield curve shifts following crude export report", -0.55, "PDVSA26"),
    ("WTI_FUTURES", "Crude oil futures react to unexpected inventory drawdown", 0.68, "WTI")
]

def daemon_worker():
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            source, headline_text, base_alpha, asset = random.choice(MACRO_EVENT_POOL)
            alpha_score = round(base_alpha + random.uniform(-0.05, 0.05), 2)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            headline = f"[{source} | {now_str}] {headline_text}"
            
            c.execute("""
                INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
                VALUES (?, ?, 'PENDING', ?, ?)
            """, (source, headline, alpha_score, asset))
            
            conn.commit()
            conn.close()
        except Exception:
            pass
        
        time.sleep(random.randint(30, 60))

if __name__ == "__main__":
    daemon_worker()

if __name__ == "__main__":
    _snap = get_latest_lseg_live()
    _alerts = check_lseg_thresholds(_snap)
    print(f"=== [LSEG ALERTS: {len(_alerts)} ACTIVAS] ===")
    for _a in _alerts:
        print(f"[!] ALERTA LSEG: {_a['rule']} (LAST={_a['last_px']}) -> {_a['action']}")
    print(f"\n=== [LSEG LIVE TELEMETRY - WAL MODE | {len(_snap)} RICS] ===")
    for _ric, _v in _snap.items():
        print(f"{_ric:<14} | {_v['dsply_name']:<20} | LAST:{_v['last_px']} | CHG:{_v['net_chg']}")

if __name__ == "__main__":
    _snap = get_latest_lseg_live()
    print(f"\n=== [LSEG LIVE TELEMETRY - WAL MODE | {len(_snap)} RICS] ===")
    for _ric, _v in _snap.items():
        print(f"{_ric:<14} | {_v['dsply_name']:<20} | LAST:{_v['last_px']} | CHG:{_v['net_chg']}")


# === M82 LSEG WAL LIVE 19-RICS HOOK ===
def render_lseg_wal_live_block():
    import sys, os
    scripts_dir = os.path.expanduser("~/M82/scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from lseg_wal_reader import get_latest_lseg_live, check_lseg_thresholds
    snap = get_latest_lseg_live()
    alerts = check_lseg_thresholds(snap)
    print(f"\n=== [LSEG LIVE TELEMETRY - WAL MODE | {len(snap)} RICS | ALERTAS: {len(alerts)}] ===")
    for ric, v in snap.items():
        name = (v.get("dsply_name") or "")[:20]
        last_px = v.get("last_px")
        net_chg = v.get("net_chg")
        print(f"{ric:<14} | {name:<20} | LAST:{str(last_px):<8} | CHG:{net_chg}")
    for a in alerts:
        print(f"[ALERTA UMBRAL] {a['ric']} -> {a['action']}")

if __name__ == "__main__":
    render_lseg_wal_live_block()
