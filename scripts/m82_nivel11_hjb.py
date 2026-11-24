#!/usr/bin/env python3
import os, time, json, sqlite3, math, logging
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
LOG_PATH = os.path.expanduser("~/M82/logs/nivel11_hjb.log")

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def evaluate_hjb_regime(vix=34.0, lambda1=0.5544, p_bunker=0.9859, tsj_verified=False):
    # Matriz de transición Markov 3-Estados (S1: Búnker, S2: Descompresión, S3: Apertura Institucional)
    phi_inv = (math.sqrt(5.0) - 1.0) / 2.0  # 0.6180339887
    dry_powder = 0.78
    friction_bps = 23.2
    cvar_cap = 0.0168

    if vix >= 28.0 or lambda1 >= 0.50 or p_bunker >= 0.40:
        regime = "S1_BUNKER_LOCKOUT"
        target_exposure = 0.22
        deploy_tranche = 0.0
        q_row = [0.965, 0.030, 0.005]
    elif not tsj_verified:
        regime = "S2_DISLOCATION_ARB"
        deploy_tranche = round(dry_powder * (1.0 - phi_inv) * 0.25, 4)  # Primer tramo áureo conservador
        target_exposure = round(min(0.30, 0.22 + deploy_tranche), 4)
        q_row = [0.150, 0.720, 0.130]
    else:
        regime = "S3_INSTITUTIONAL_UNLOCK"
        deploy_tranche = round(dry_powder * (1.0 - phi_inv), 4)
        target_exposure = round(min(0.30, 0.22 + deploy_tranche), 4)
        q_row = [0.050, 0.200, 0.750]

    return {
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regime": regime,
        "vix": vix,
        "jacobi_lambda1": lambda1,
        "p_bunker": p_bunker,
        "tsj_cne_verified": tsj_verified,
        "current_exposure": 0.22,
        "hjb_target_exposure": target_exposure,
        "golden_tranche_release": deploy_tranche,
        "markov_q_transition": q_row,
        "friction_bps": friction_bps,
        "cvar_99_cap": cvar_cap,
        "lockout": "NO_TRADE" if regime == "S1_BUNKER_LOCKOUT" else "STAGED_REVIEW"
    }

def main():
    while True:
        try:
            state = evaluate_hjb_regime()
            conn = sqlite3.connect(DB_PATH, timeout=60)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=60000;")
            cur = conn.cursor()
            cur.execute(
                "UPDATE macro_dossier SET metadata_json = ?, updated_at = CURRENT_TIMESTAMP WHERE m82_tag = 'v60.5-NIVEL-XI-HJB-OPTIMAL-SWITCHING'",
                (json.dumps(state),)
            )
            cur.execute(
                "UPDATE m82_daemons_registry SET last_heartbeat = CURRENT_TIMESTAMP, status = 'ACTIVE' WHERE daemon_name = 'm82_nivel11_hjb.py'"
            )
            conn.commit()
            conn.close()
            logging.info(f"HJB L11 Cycle OK | Regime={state['regime']} | TargetExp={state['hjb_target_exposure']} | Q={state['markov_q_transition']}")
        except Exception as e:
            logging.error(f"HJB L11 Error: {e}")
        time.sleep(900)

if __name__ == "__main__":
    main()
